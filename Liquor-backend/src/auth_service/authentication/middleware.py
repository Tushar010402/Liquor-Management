import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for the auth service.
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
                algorithms=['HS256']
            )
            
            # Get the user
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')
            
            user = User.objects.filter(id=user_id, is_active=True).first()
            if not user:
                raise AuthenticationFailed('User not found or inactive')
            
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