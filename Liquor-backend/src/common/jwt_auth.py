import jwt
import requests
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)

class MicroserviceUser:
    """
    A simple class to represent a user authenticated via JWT token.
    This is used by microservices that don't have direct access to the User model.
    """
    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.email = user_data.get('email')
        self.tenant_id = user_data.get('tenant_id')
        self.is_active = user_data.get('is_active', True)
        self.is_staff = user_data.get('is_staff', False)
        self.is_superuser = user_data.get('is_superuser', False)
        self.role = user_data.get('role')
        self.permissions = user_data.get('permissions', [])
        self._user_data = user_data  # Store the original data
    
    def __str__(self):
        return self.email
    
    def is_authenticated(self):
        return True
    
    def has_permission(self, permission_code):
        """Check if user has a specific permission."""
        return permission_code in self.permissions
    
    def is_saas_admin(self):
        """Check if user is a SaaS admin."""
        return self.is_superuser or self.role == 'saas_admin'
    
    def is_tenant_admin(self):
        """Check if user is a tenant admin."""
        return self.role == 'tenant_admin'
    
    def is_manager(self):
        """Check if user is a manager."""
        return self.role == 'manager'
    
    def is_assistant_manager(self):
        """Check if user is an assistant manager."""
        return self.role == 'assistant_manager'
    
    def is_executive(self):
        """Check if user is an executive."""
        return self.role == 'executive'


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for microservices.
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        # Get the token from the request
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None
        
        try:
            # Extract the token
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'bearer':
                raise AuthenticationFailed('Invalid token header')
            
            token = auth_parts[1]
            
            # Decode the token
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256'],
                options={"verify_signature": False}  # We'll verify with the auth service
            )
            
            # Verify token with auth service
            user_data = self.verify_token_with_auth_service(token)
            if not user_data:
                raise AuthenticationFailed('Invalid token')
            
            # Create a user object
            user = MicroserviceUser(user_data)
            
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise AuthenticationFailed('Authentication failed')
    
    def authenticate_header(self, request):
        return 'Bearer'
    
    def verify_token_with_auth_service(self, token):
        """
        Verify the token with the auth service.
        
        Args:
            token (str): JWT token to verify.
            
        Returns:
            dict: User data if token is valid, None otherwise.
        """
        try:
            # Call the auth service to verify the token
            response = requests.post(
                f"{settings.AUTH_SERVICE_URL}/api/auth/verify-token/",
                json={"token": token},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json().get('user')
            
            return None
        except Exception as e:
            logger.error(f"Error verifying token with auth service: {str(e)}")
            return None