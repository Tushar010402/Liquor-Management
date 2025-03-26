from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from common.utils.kafka_utils import publish_event
from common.utils.redis_utils import rate_limit_check
from users.models import UserShopAssignment
from users.serializers import UserShopAssignmentSerializer
from .models import LoginAttempt, PasswordResetToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Check rate limiting
            request = self.context.get('request')
            ip_address = self._get_client_ip(request)
            
            # Rate limit by IP address (10 attempts per minute)
            ip_allowed, ip_count, ip_ttl = rate_limit_check(
                f'login:ip:{ip_address}', 10, 60
            )
            
            if not ip_allowed:
                # Log failed attempt
                LoginAttempt.objects.create(
                    email=email,
                    ip_address=ip_address,
                    user_agent=self._get_user_agent(request),
                    successful=False
                )
                
                raise serializers.ValidationError({
                    'non_field_errors': [
                        f'Too many login attempts. Please try again in {ip_ttl} seconds.'
                    ]
                })
            
            # Rate limit by email (5 attempts per minute)
            email_allowed, email_count, email_ttl = rate_limit_check(
                f'login:email:{email}', 5, 60
            )
            
            if not email_allowed:
                # Log failed attempt
                LoginAttempt.objects.create(
                    email=email,
                    ip_address=ip_address,
                    user_agent=self._get_user_agent(request),
                    successful=False
                )
                
                raise serializers.ValidationError({
                    'non_field_errors': [
                        f'Too many login attempts for this email. Please try again in {email_ttl} seconds.'
                    ]
                })
            
            # Try to authenticate
            user = authenticate(request=request, email=email, password=password)
            
            if not user:
                # Log failed attempt
                LoginAttempt.objects.create(
                    email=email,
                    ip_address=ip_address,
                    user_agent=self._get_user_agent(request),
                    successful=False
                )
                
                # Increment failed login attempts for the user if they exist
                try:
                    user_obj = User.objects.get(email=email)
                    user_obj.increment_failed_login()
                except User.DoesNotExist:
                    pass
                
                raise serializers.ValidationError({
                    'non_field_errors': ['Unable to log in with provided credentials.']
                })
            
            # Check if user is active
            if not user.is_active:
                # Log failed attempt
                LoginAttempt.objects.create(
                    user=user,
                    email=email,
                    ip_address=ip_address,
                    user_agent=self._get_user_agent(request),
                    successful=False
                )
                
                raise serializers.ValidationError({
                    'non_field_errors': ['User account is disabled.']
                })
            
            # Check if account is locked
            if user.is_account_locked():
                # Log failed attempt
                LoginAttempt.objects.create(
                    user=user,
                    email=email,
                    ip_address=ip_address,
                    user_agent=self._get_user_agent(request),
                    successful=False
                )
                
                # Calculate time until unlock
                lock_time = user.account_locked_until
                if lock_time:
                    seconds_remaining = int((lock_time - timezone.now()).total_seconds())
                    minutes_remaining = max(1, seconds_remaining // 60)
                    
                    raise serializers.ValidationError({
                        'non_field_errors': [
                            f'Account is locked due to too many failed login attempts. '
                            f'Please try again in {minutes_remaining} minutes.'
                        ]
                    })
                else:
                    raise serializers.ValidationError({
                        'non_field_errors': ['Account is locked. Please contact support.']
                    })
            
            # Log successful attempt
            LoginAttempt.objects.create(
                user=user,
                email=email,
                ip_address=ip_address,
                user_agent=self._get_user_agent(request),
                successful=True
            )
            
            # Reset failed login attempts
            user.reset_failed_login()
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Get assigned shops
            assigned_shops = UserShopAssignment.objects.filter(user=user)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            # Publish login event
            event_data = {
                'event_type': 'user_login',
                'user_id': str(user.id),
                'email': user.email,
                'ip_address': ip_address,
                'timestamp': timezone.now().isoformat()
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            # Return validated data
            return {
                'user': user,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'assigned_shops': assigned_shops
            }
        
        raise serializers.ValidationError({
            'non_field_errors': ['Must include "email" and "password".']
        })
    
    def _get_client_ip(self, request):
        """
        Get client IP address from request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_user_agent(self, request):
        """
        Get user agent from request.
        """
        return request.META.get('HTTP_USER_AGENT', '')


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializer for token response.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()
    assigned_shops = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        """
        Get user data.
        """
        user = obj['user']
        return {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
        }
    
    def get_assigned_shops(self, obj):
        """
        Get assigned shops data.
        """
        return UserShopAssignmentSerializer(obj['assigned_shops'], many=True).data


class RefreshTokenSerializer(serializers.Serializer):
    """
    Serializer for refreshing access token.
    """
    refresh = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """
        Validate that the email exists.
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            # We don't want to reveal that the email doesn't exist
            pass
        
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        """
        Validate that the passwords match and the token is valid.
        """
        # Check that passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': ['Passwords do not match.']
            })
        
        # Check that token exists and is valid
        try:
            token_obj = PasswordResetToken.objects.get(
                token=attrs['token'],
                expires_at__gt=timezone.now(),
                used=False,
                is_active=True
            )
            attrs['token_obj'] = token_obj
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({
                'token': ['Invalid or expired token.']
            })
        
        return attrs