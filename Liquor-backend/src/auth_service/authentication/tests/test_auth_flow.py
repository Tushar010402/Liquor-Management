import json
import uuid
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Role, Permission, Tenant

User = get_user_model()

class AuthenticationFlowTest(TestCase):
    """
    Test the authentication flow including login, token refresh, and logout.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            domain="test.com",
            is_active=True
        )
        
        # Create permissions
        self.permission1 = Permission.objects.create(
            name="View Products",
            code="view_products",
            description="Can view products"
        )
        self.permission2 = Permission.objects.create(
            name="Edit Products",
            code="edit_products",
            description="Can edit products"
        )
        
        # Create roles
        self.role = Role.objects.create(
            name="Manager",
            description="Shop Manager"
        )
        self.role.permissions.add(self.permission1, self.permission2)
        
        # Create user
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            tenant=self.tenant,
            role=self.role,
            is_active=True
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_login_success(self):
        """
        Test successful login.
        """
        url = reverse('login')
        data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue(response.data['success'])
        self.assertTrue('data' in response.data)
        self.assertTrue('access_token' in response.data['data'])
        self.assertTrue('refresh_token' in response.data['data'])
        self.assertTrue('user' in response.data['data'])
    
    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        url = reverse('login')
        data = {
            'email': 'test@test.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
    
    def test_token_refresh(self):
        """
        Test token refresh.
        """
        # First login to get tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['data']['refresh_token']
        
        # Now try to refresh the token
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh_token': refresh_token
        }
        response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue(response.data['success'])
        self.assertTrue('data' in response.data)
        self.assertTrue('access_token' in response.data['data'])
    
    def test_token_refresh_invalid(self):
        """
        Test token refresh with invalid token.
        """
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh_token': 'invalid_token'
        }
        response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
    
    def test_logout(self):
        """
        Test logout.
        """
        # First login to get tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        access_token = login_response.data['data']['access_token']
        refresh_token = login_response.data['data']['refresh_token']
        
        # Now try to logout
        logout_url = reverse('logout')
        logout_data = {
            'refresh_token': refresh_token
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(logout_url, logout_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue(response.data['success'])
        
        # Try to use the refresh token again (should fail)
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh_token': refresh_token
        }
        response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
    
    def test_token_verification(self):
        """
        Test token verification.
        """
        # First login to get tokens
        login_url = reverse('login')
        login_data = {
            'email': 'test@test.com',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        access_token = login_response.data['data']['access_token']
        
        # Now try to verify the token
        verify_url = reverse('token_verify')
        verify_data = {
            'token': access_token
        }
        response = self.client.post(verify_url, verify_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('success' in response.data)
        self.assertTrue(response.data['success'])
        self.assertTrue('valid' in response.data)
        self.assertTrue(response.data['valid'])
        self.assertTrue('user' in response.data)
        self.assertEqual(response.data['user']['email'], 'test@test.com')
        self.assertEqual(response.data['user']['role'], 'Manager')
        
        # Verify permissions are included
        self.assertTrue('permissions' in response.data['user'])
        self.assertIn('view_products', response.data['user']['permissions'])
        self.assertIn('edit_products', response.data['user']['permissions'])
    
    def test_token_verification_invalid(self):
        """
        Test token verification with invalid token.
        """
        verify_url = reverse('token_verify')
        verify_data = {
            'token': 'invalid_token'
        }
        response = self.client.post(verify_url, verify_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['success'])
        self.assertFalse(response.data['valid'])