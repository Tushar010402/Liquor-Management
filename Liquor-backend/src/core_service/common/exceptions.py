from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from rest_framework.exceptions import (
    APIException, NotFound, ValidationError, 
    PermissionDenied as DRFPermissionDenied,
    AuthenticationFailed, NotAuthenticated,
    MethodNotAllowed, Throttled
)
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that formats all exceptions
    in a consistent way.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, Http404):
            data = {
                'success': False,
                'message': 'Resource not found',
                'error': {
                    'code': 'not_found',
                    'detail': str(exc)
                }
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
            
        elif isinstance(exc, PermissionDenied):
            data = {
                'success': False,
                'message': 'Permission denied',
                'error': {
                    'code': 'permission_denied',
                    'detail': str(exc)
                }
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
            
        elif isinstance(exc, IntegrityError):
            data = {
                'success': False,
                'message': 'Database integrity error',
                'error': {
                    'code': 'integrity_error',
                    'detail': str(exc)
                }
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            # Log the error for debugging
            logger.error(f"Unhandled exception: {exc}")
            data = {
                'success': False,
                'message': 'Internal server error',
                'error': {
                    'code': 'server_error',
                    'detail': 'An unexpected error occurred'
                }
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Format the response for known exceptions
    error_data = {
        'success': False,
        'message': response.data.get('detail', 'An error occurred'),
        'error': {
            'code': get_error_code(exc),
            'detail': response.data
        }
    }
    
    # Clean up the error detail if it's just the detail message
    if 'detail' in error_data['error']['detail']:
        error_detail = error_data['error']['detail']['detail']
        error_data['error']['detail'] = error_detail
    
    response.data = error_data
    return response

def get_error_code(exc):
    """
    Get a string error code based on the exception type.
    """
    if isinstance(exc, ValidationError):
        return 'validation_error'
    elif isinstance(exc, NotAuthenticated):
        return 'not_authenticated'
    elif isinstance(exc, AuthenticationFailed):
        return 'authentication_failed'
    elif isinstance(exc, DRFPermissionDenied):
        return 'permission_denied'
    elif isinstance(exc, NotFound):
        return 'not_found'
    elif isinstance(exc, MethodNotAllowed):
        return 'method_not_allowed'
    elif isinstance(exc, Throttled):
        return 'throttled'
    else:
        return 'api_error'


class ServiceUnavailableError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid request.'
    default_code = 'bad_request'


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'conflict'