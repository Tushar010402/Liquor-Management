import uuid
import jwt
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from .kafka_handlers import (
    publish_user_created_event, publish_user_updated_event,
    publish_user_login_event, publish_user_logout_event
)
from .models import PasswordResetToken, RefreshToken as RefreshTokenModel
from .serializers import (
    LoginSerializer, TokenResponseSerializer, RefreshTokenSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)

User = get_user_model()


class LoginView(views.APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Return token response
        response_serializer = TokenResponseSerializer(serializer.validated_data)
        
        return Response({
            'success': True,
            'data': response_serializer.data,
            'timestamp': timezone.now().isoformat()
        })


class LogoutView(views.APIView):
    """
    API endpoint for user logout.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user logout.
        """
        try:
            # Get refresh token from request
            refresh_token = request.data.get('refresh_token')
            
            if not refresh_token:
                return Response({
                    'success': False,
                    'message': 'Refresh token is required',
                    'timestamp': timezone.now().isoformat()
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Store the blacklisted token
            RefreshTokenModel.objects.create(
                user=request.user,
                token=refresh_token,
                expires_at=timezone.now() + timedelta(days=7),
                revoked=True,
                revoked_at=timezone.now()
            )
            
            # Publish logout event
            publish_user_logout_event(request.user)
            
            return Response({
                'success': True,
                'message': 'Logged out successfully',
                'timestamp': timezone.now().isoformat()
            })
            
        except TokenError:
            return Response({
                'success': False,
                'message': 'Invalid token',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(TokenRefreshView):
    """
    API endpoint for refreshing access tokens.
    """
    serializer_class = RefreshTokenSerializer
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for token refresh.
        """
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({
                'success': False,
                'message': str(e),
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'success': True,
            'data': serializer.validated_data,
            'timestamp': timezone.now().isoformat()
        })


class PasswordResetRequestView(views.APIView):
    """
    API endpoint for requesting a password reset.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for password reset requests.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Generate token
            token = str(uuid.uuid4())
            
            # Save token
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            
            # Send email
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            # Prepare email content
            subject = 'Password Reset Request'
            message = f'Click the link below to reset your password:\n\n{reset_url}\n\nThis link will expire in 24 hours.'
            html_message = render_to_string('authentication/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            
            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=False
            )
            
            # Publish password reset request event
            event_data = {
                'event_type': 'password_reset_requested',
                'user_id': str(user.id),
                'email': user.email,
                'timestamp': timezone.now().isoformat()
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
        except User.DoesNotExist:
            # We don't want to reveal that the email doesn't exist
            pass
        
        return Response({
            'success': True,
            'message': 'If your email is registered, you will receive a password reset link shortly.',
            'timestamp': timezone.now().isoformat()
        })


class PasswordResetConfirmView(views.APIView):
    """
    API endpoint for confirming a password reset.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for password reset confirmations.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get token object
        token_obj = serializer.validated_data['token_obj']
        user = token_obj.user
        
        # Set new password
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        # Mark token as used
        token_obj.used = True
        token_obj.used_at = timezone.now()
        token_obj.save()
        
        # Publish password reset event
        event_data = {
            'event_type': 'password_reset_completed',
            'user_id': str(user.id),
            'email': user.email,
            'timestamp': timezone.now().isoformat()
        }
        publish_event('user-events', f'user:{user.id}', event_data)
        
        return Response({
            'success': True,
            'message': 'Password has been reset successfully.',
            'timestamp': timezone.now().isoformat()
        })


class TokenVerificationView(views.APIView):
    """
    API endpoint for token verification.
    Used by other microservices to verify JWT tokens.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for token verification.
        """
        token = request.data.get('token')
        
        if not token:
            return Response({
                'success': False,
                'message': 'Token is required',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Decode the token
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256']
            )
            
            # Get the user
            user_id = payload.get('user_id')
            if not user_id:
                raise jwt.InvalidTokenError('Invalid token payload')
            
            user = User.objects.filter(id=user_id, is_active=True).first()
            if not user:
                raise jwt.InvalidTokenError('User not found or inactive')
            
            # Get user permissions
            permissions = []
            if hasattr(user, 'role') and user.role:
                # Get permissions from role
                if hasattr(user.role, 'permissions'):
                    permissions = [p.code for p in user.role.permissions.all()]
            
            # Return user data
            return Response({
                'success': True,
                'valid': True,
                'user': {
                    'id': str(user.id),
                    'email': user.email,
                    'tenant_id': str(user.tenant_id) if user.tenant_id else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'role': user.role.name if hasattr(user, 'role') and user.role else None,
                    'permissions': permissions
                },
                'timestamp': timezone.now().isoformat()
            })
        except jwt.ExpiredSignatureError:
            return Response({
                'success': False,
                'valid': False,
                'message': 'Token has expired',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            return Response({
                'success': False,
                'valid': False,
                'message': str(e),
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': False,
                'valid': False,
                'message': f'Authentication failed: {str(e)}',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)