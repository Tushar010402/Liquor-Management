import json
import jwt
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from common.jwt_auth import JWTAuthentication, MicroserviceUser

class JWTAuthenticationTest(TestCase):
    """
    Test the JWT authentication middleware.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.factory = RequestFactory()
        self.auth = JWTAuthentication()
        
        # Create a test payload
        self.payload = {
            'user_id': '123e4567-e89b-12d3-a456-426614174000',
            'email': 'test@example.com',
            'exp': 1716239022  # Some future time
        }
        
        # Create a test token
        self.token = jwt.encode(
            self.payload,
            'test_secret',
            algorithm='HS256'
        )
        
        # Create a test user data
        self.user_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'email': 'test@example.com',
            'tenant_id': '123e4567-e89b-12d3-a456-426614174001',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'manager',
            'permissions': ['view_products', 'edit_products']
        }
    
    def test_authenticate_no_auth_header(self):
        """
        Test authentication with no auth header.
        """
        request = self.factory.get('/')
        result = self.auth.authenticate(request)
        self.assertIsNone(result)
    
    def test_authenticate_invalid_auth_header(self):
        """
        Test authentication with invalid auth header.
        """
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Token abc123'
        
        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)
    
    @patch('common.jwt_auth.JWTAuthentication.verify_token_with_auth_service')
    def test_authenticate_valid_token(self, mock_verify):
        """
        Test authentication with valid token.
        """
        mock_verify.return_value = self.user_data
        
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        
        user, token = self.auth.authenticate(request)
        
        self.assertEqual(token, self.token)
        self.assertIsInstance(user, MicroserviceUser)
        self.assertEqual(user.id, self.user_data['id'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.tenant_id, self.user_data['tenant_id'])
        self.assertEqual(user.role, self.user_data['role'])
        self.assertEqual(user.permissions, self.user_data['permissions'])
    
    @patch('common.jwt_auth.JWTAuthentication.verify_token_with_auth_service')
    def test_authenticate_invalid_token(self, mock_verify):
        """
        Test authentication with invalid token.
        """
        mock_verify.return_value = None
        
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'
        
        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)
    
    @patch('requests.post')
    def test_verify_token_with_auth_service_success(self, mock_post):
        """
        Test token verification with auth service (success).
        """
        # Mock the response from the auth service
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'user': self.user_data
        }
        mock_post.return_value = mock_response
        
        result = self.auth.verify_token_with_auth_service(self.token)
        
        self.assertEqual(result, self.user_data)
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_verify_token_with_auth_service_failure(self, mock_post):
        """
        Test token verification with auth service (failure).
        """
        # Mock the response from the auth service
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        result = self.auth.verify_token_with_auth_service(self.token)
        
        self.assertIsNone(result)
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_verify_token_with_auth_service_exception(self, mock_post):
        """
        Test token verification with auth service (exception).
        """
        # Mock the response from the auth service
        mock_post.side_effect = Exception('Connection error')
        
        result = self.auth.verify_token_with_auth_service(self.token)
        
        self.assertIsNone(result)
        mock_post.assert_called_once()


class MicroserviceUserTest(TestCase):
    """
    Test the MicroserviceUser class.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.user_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'email': 'test@example.com',
            'tenant_id': '123e4567-e89b-12d3-a456-426614174001',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'manager',
            'permissions': ['view_products', 'edit_products']
        }
        
        self.user = MicroserviceUser(self.user_data)
    
    def test_user_properties(self):
        """
        Test user properties.
        """
        self.assertEqual(self.user.id, self.user_data['id'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.tenant_id, self.user_data['tenant_id'])
        self.assertEqual(self.user.is_active, self.user_data['is_active'])
        self.assertEqual(self.user.is_staff, self.user_data['is_staff'])
        self.assertEqual(self.user.is_superuser, self.user_data['is_superuser'])
        self.assertEqual(self.user.role, self.user_data['role'])
        self.assertEqual(self.user.permissions, self.user_data['permissions'])
    
    def test_is_authenticated(self):
        """
        Test is_authenticated method.
        """
        self.assertTrue(self.user.is_authenticated())
    
    def test_has_permission(self):
        """
        Test has_permission method.
        """
        self.assertTrue(self.user.has_permission('view_products'))
        self.assertTrue(self.user.has_permission('edit_products'))
        self.assertFalse(self.user.has_permission('delete_products'))
    
    def test_role_checks(self):
        """
        Test role check methods.
        """
        self.assertFalse(self.user.is_saas_admin())
        self.assertFalse(self.user.is_tenant_admin())
        self.assertTrue(self.user.is_manager())
        self.assertFalse(self.user.is_assistant_manager())
        self.assertFalse(self.user.is_executive())
        
        # Change role and test again
        self.user.role = 'tenant_admin'
        self.assertFalse(self.user.is_saas_admin())
        self.assertTrue(self.user.is_tenant_admin())
        self.assertFalse(self.user.is_manager())
        
        # Test superuser
        self.user.is_superuser = True
        self.assertTrue(self.user.is_saas_admin())