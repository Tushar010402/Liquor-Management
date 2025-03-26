import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.exceptions import APIException, NotFound, ValidationError, PermissionDenied, AuthenticationFailed
from rest_framework.views import Response
from rest_framework import status
from common.exceptions import (
    custom_exception_handler, ServiceUnavailableException,
    ResourceNotFoundException, ValidationException,
    AuthorizationException, AuthenticationException
)

class CustomExceptionHandlerTest(TestCase):
    """
    Test the custom exception handler.
    """
    
    def test_api_exception(self):
        """
        Test handling of APIException.
        """
        # Create an APIException
        exc = APIException('Test API exception')
        exc.default_code = 'api_error'
        
        # Create a mock context
        context = {}
        
        # Call the handler
        response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['code'], 'api_error')
        self.assertEqual(response.data['messages'], ['Test API exception'])
    
    def test_not_found_exception(self):
        """
        Test handling of NotFound exception.
        """
        # Create a NotFound exception
        exc = NotFound('Resource not found')
        
        # Create a mock context
        context = {}
        
        # Call the handler
        response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['code'], 'not_found')
        self.assertEqual(response.data['messages'], ['Resource not found'])
    
    def test_validation_error(self):
        """
        Test handling of ValidationError.
        """
        # Create a ValidationError
        exc = ValidationError({
            'field1': ['Error 1', 'Error 2'],
            'field2': 'Error 3'
        })
        
        # Create a mock context
        context = {}
        
        # Call the handler
        response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 'invalid')
    
    def test_permission_denied(self):
        """
        Test handling of PermissionDenied exception.
        """
        # Create a PermissionDenied exception
        exc = PermissionDenied('Permission denied')
        
        # Create a mock context
        context = {}
        
        # Call the handler
        response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['code'], 'permission_denied')
        self.assertEqual(response.data['messages'], ['Permission denied'])
    
    def test_authentication_failed(self):
        """
        Test handling of AuthenticationFailed exception.
        """
        # Create an AuthenticationFailed exception
        exc = AuthenticationFailed('Authentication failed')
        
        # Create a mock context
        context = {}
        
        # Call the handler
        response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['code'], 'authentication_failed')
        self.assertEqual(response.data['messages'], ['Authentication failed'])
    
    def test_unhandled_exception(self):
        """
        Test handling of unhandled exception.
        """
        # Create an unhandled exception
        exc = Exception('Unhandled exception')
        
        # Create a mock context
        context = {}
        
        # Call the handler
        with self.assertLogs(level='ERROR') as cm:
            response = custom_exception_handler(exc, context)
        
        # Assertions
        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['detail'], 'An unexpected error occurred.')
        self.assertIn('Unhandled exception: Unhandled exception', cm.output[0])


class CustomExceptionsTest(TestCase):
    """
    Test the custom exceptions.
    """
    
    def test_service_unavailable_exception(self):
        """
        Test ServiceUnavailableException.
        """
        exc = ServiceUnavailableException()
        self.assertEqual(exc.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(exc.default_detail, 'Service temporarily unavailable, try again later.')
        self.assertEqual(exc.default_code, 'service_unavailable')
    
    def test_resource_not_found_exception(self):
        """
        Test ResourceNotFoundException.
        """
        exc = ResourceNotFoundException()
        self.assertEqual(exc.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exc.default_detail, 'The requested resource was not found.')
        self.assertEqual(exc.default_code, 'resource_not_found')
    
    def test_validation_exception(self):
        """
        Test ValidationException.
        """
        exc = ValidationException()
        self.assertEqual(exc.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(exc.default_detail, 'Invalid data provided.')
        self.assertEqual(exc.default_code, 'validation_error')
    
    def test_authorization_exception(self):
        """
        Test AuthorizationException.
        """
        exc = AuthorizationException()
        self.assertEqual(exc.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(exc.default_detail, 'You do not have permission to perform this action.')
        self.assertEqual(exc.default_code, 'permission_denied')
    
    def test_authentication_exception(self):
        """
        Test AuthenticationException.
        """
        exc = AuthenticationException()
        self.assertEqual(exc.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(exc.default_detail, 'Authentication credentials were not provided or are invalid.')
        self.assertEqual(exc.default_code, 'authentication_failed')