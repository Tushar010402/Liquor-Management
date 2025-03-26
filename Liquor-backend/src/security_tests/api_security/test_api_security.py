"""
Security tests for API endpoints in the Liquor Management System.
These tests verify the security of the API endpoints, including authentication,
authorization, input validation, rate limiting, and CSRF protection.
"""

import json
import uuid
import pytest
import requests
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

# Import JWT utilities
from common.jwt_auth import generate_jwt_token, decode_jwt_token

# Import models
from auth_service.users.models import User as AuthUser
from auth_service.roles.models import Role, Permission
from auth_service.tenants.models import Tenant
from auth_service.shops.models import Shop as AuthShop

# Test configuration
API_BASE_URL = "http://localhost:8000/api"
AUTH_SERVICE_URL = f"{API_BASE_URL}/auth"
INVENTORY_SERVICE_URL = f"{API_BASE_URL}/inventory"
SALES_SERVICE_URL = f"{API_BASE_URL}/sales"
PURCHASE_SERVICE_URL = f"{API_BASE_URL}/purchase"

class TestAuthenticationSecurity(TestCase):
    """
    Test the authentication security of the API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            status="active"
        )
        
        # Create test shop
        self.shop = AuthShop.objects.create(
            name="Test Shop",
            tenant_id=self.tenant.id,
            code="TST01",
            shop_type="retail",
            status="active",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            phone="1234567890",
            license_number="LIC123456",
            license_type="Retail",
            license_expiry="2025-12-31",
            opening_time="09:00:00",
            closing_time="21:00:00"
        )
        
        # Create test roles
        self.admin_role = Role.objects.create(
            name="Admin",
            tenant=self.tenant
        )
        
        self.manager_role = Role.objects.create(
            name="Manager",
            tenant=self.tenant
        )
        
        self.cashier_role = Role.objects.create(
            name="Cashier",
            tenant=self.tenant
        )
        
        # Create test users
        self.admin_user = AuthUser.objects.create_user(
            username="admin@test.com",
            email="admin@test.com",
            password="Admin@123",
            first_name="Admin",
            last_name="User",
            tenant=self.tenant,
            role=self.admin_role
        )
        
        self.manager_user = AuthUser.objects.create_user(
            username="manager@test.com",
            email="manager@test.com",
            password="Manager@123",
            first_name="Manager",
            last_name="User",
            tenant=self.tenant,
            role=self.manager_role
        )
        
        self.cashier_user = AuthUser.objects.create_user(
            username="cashier@test.com",
            email="cashier@test.com",
            password="Cashier@123",
            first_name="Cashier",
            last_name="User",
            tenant=self.tenant,
            role=self.cashier_role
        )
        
        # Create API client
        self.client = APIClient()
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        login_url = reverse('auth:login')
        
        # Test login with valid credentials
        response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'Admin@123'
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'admin@test.com')
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_url = reverse('auth:login')
        
        # Test login with invalid password
        response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'WrongPassword'
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        
        # Test login with non-existent user
        response = self.client.post(
            login_url,
            {
                'username': 'nonexistent@test.com',
                'password': 'Password@123'
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_access_protected_endpoint_without_token(self):
        """Test accessing a protected endpoint without a token."""
        user_profile_url = reverse('auth:user-profile')
        
        # Test accessing protected endpoint without token
        response = self.client.get(user_profile_url)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_access_protected_endpoint_with_invalid_token(self):
        """Test accessing a protected endpoint with an invalid token."""
        user_profile_url = reverse('auth:user-profile')
        
        # Set invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        # Test accessing protected endpoint with invalid token
        response = self.client.get(user_profile_url)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_access_protected_endpoint_with_expired_token(self):
        """Test accessing a protected endpoint with an expired token."""
        user_profile_url = reverse('auth:user-profile')
        
        # Generate expired token
        from datetime import datetime, timedelta
        
        expired_token = generate_jwt_token(
            user_id=str(self.admin_user.id),
            tenant_id=str(self.tenant.id),
            role=self.admin_user.role.name,
            exp=(datetime.utcnow() - timedelta(hours=1)).timestamp()
        )
        
        # Set expired token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        
        # Test accessing protected endpoint with expired token
        response = self.client.get(user_profile_url)
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh(self):
        """Test refreshing an access token."""
        login_url = reverse('auth:login')
        refresh_url = reverse('auth:token-refresh')
        
        # Login to get tokens
        login_response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'Admin@123'
            },
            format='json'
        )
        
        # Get refresh token
        refresh_token = login_response.data['refresh_token']
        
        # Test refreshing token
        response = self.client.post(
            refresh_url,
            {
                'refresh_token': refresh_token
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        
        # Test accessing protected endpoint with new token
        user_profile_url = reverse('auth:user-profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["token"]}')
        profile_response = self.client.get(user_profile_url)
        
        # Verify response
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['email'], 'admin@test.com')

class TestAuthorizationSecurity(TestCase):
    """
    Test the authorization security of the API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            status="active"
        )
        
        # Create test shop
        self.shop = AuthShop.objects.create(
            name="Test Shop",
            tenant_id=self.tenant.id,
            code="TST01",
            shop_type="retail",
            status="active",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            phone="1234567890",
            license_number="LIC123456",
            license_type="Retail",
            license_expiry="2025-12-31",
            opening_time="09:00:00",
            closing_time="21:00:00"
        )
        
        # Create test roles with permissions
        self.admin_role = Role.objects.create(
            name="Admin",
            tenant=self.tenant
        )
        
        self.manager_role = Role.objects.create(
            name="Manager",
            tenant=self.tenant
        )
        
        self.cashier_role = Role.objects.create(
            name="Cashier",
            tenant=self.tenant
        )
        
        # Create permissions
        self.view_sales_permission = Permission.objects.create(
            name="view_sales",
            description="Can view sales"
        )
        
        self.create_sales_permission = Permission.objects.create(
            name="create_sales",
            description="Can create sales"
        )
        
        self.approve_sales_permission = Permission.objects.create(
            name="approve_sales",
            description="Can approve sales"
        )
        
        self.view_inventory_permission = Permission.objects.create(
            name="view_inventory",
            description="Can view inventory"
        )
        
        self.manage_inventory_permission = Permission.objects.create(
            name="manage_inventory",
            description="Can manage inventory"
        )
        
        # Assign permissions to roles
        self.admin_role.permissions.add(
            self.view_sales_permission,
            self.create_sales_permission,
            self.approve_sales_permission,
            self.view_inventory_permission,
            self.manage_inventory_permission
        )
        
        self.manager_role.permissions.add(
            self.view_sales_permission,
            self.create_sales_permission,
            self.approve_sales_permission,
            self.view_inventory_permission
        )
        
        self.cashier_role.permissions.add(
            self.view_sales_permission,
            self.create_sales_permission,
            self.view_inventory_permission
        )
        
        # Create test users
        self.admin_user = AuthUser.objects.create_user(
            username="admin@test.com",
            email="admin@test.com",
            password="Admin@123",
            first_name="Admin",
            last_name="User",
            tenant=self.tenant,
            role=self.admin_role
        )
        
        self.manager_user = AuthUser.objects.create_user(
            username="manager@test.com",
            email="manager@test.com",
            password="Manager@123",
            first_name="Manager",
            last_name="User",
            tenant=self.tenant,
            role=self.manager_role
        )
        
        self.cashier_user = AuthUser.objects.create_user(
            username="cashier@test.com",
            email="cashier@test.com",
            password="Cashier@123",
            first_name="Cashier",
            last_name="User",
            tenant=self.tenant,
            role=self.cashier_role
        )
        
        # Create API client
        self.client = APIClient()
    
    def test_admin_access_to_all_endpoints(self):
        """Test admin access to all endpoints."""
        # Login as admin
        login_url = reverse('auth:login')
        login_response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'Admin@123'
            },
            format='json'
        )
        
        # Set token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["token"]}')
        
        # Test access to sales endpoints
        sales_url = reverse('sales:list')
        sales_response = self.client.get(sales_url)
        self.assertEqual(sales_response.status_code, status.HTTP_200_OK)
        
        # Test access to inventory endpoints
        inventory_url = reverse('inventory:list')
        inventory_response = self.client.get(inventory_url)
        self.assertEqual(inventory_response.status_code, status.HTTP_200_OK)
        
        # Test access to inventory management endpoints
        inventory_management_url = reverse('inventory:manage')
        inventory_management_response = self.client.post(
            inventory_management_url,
            {
                'action': 'adjust',
                'brand_id': str(uuid.uuid4()),
                'quantity': 10,
                'reason': 'Test adjustment'
            },
            format='json'
        )
        self.assertEqual(inventory_management_response.status_code, status.HTTP_200_OK)
    
    def test_manager_access_restrictions(self):
        """Test manager access restrictions."""
        # Login as manager
        login_url = reverse('auth:login')
        login_response = self.client.post(
            login_url,
            {
                'username': 'manager@test.com',
                'password': 'Manager@123'
            },
            format='json'
        )
        
        # Set token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["token"]}')
        
        # Test access to sales endpoints
        sales_url = reverse('sales:list')
        sales_response = self.client.get(sales_url)
        self.assertEqual(sales_response.status_code, status.HTTP_200_OK)
        
        # Test access to inventory endpoints
        inventory_url = reverse('inventory:list')
        inventory_response = self.client.get(inventory_url)
        self.assertEqual(inventory_response.status_code, status.HTTP_200_OK)
        
        # Test access to inventory management endpoints (should be restricted)
        inventory_management_url = reverse('inventory:manage')
        inventory_management_response = self.client.post(
            inventory_management_url,
            {
                'action': 'adjust',
                'brand_id': str(uuid.uuid4()),
                'quantity': 10,
                'reason': 'Test adjustment'
            },
            format='json'
        )
        self.assertEqual(inventory_management_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_cashier_access_restrictions(self):
        """Test cashier access restrictions."""
        # Login as cashier
        login_url = reverse('auth:login')
        login_response = self.client.post(
            login_url,
            {
                'username': 'cashier@test.com',
                'password': 'Cashier@123'
            },
            format='json'
        )
        
        # Set token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["token"]}')
        
        # Test access to sales endpoints
        sales_url = reverse('sales:list')
        sales_response = self.client.get(sales_url)
        self.assertEqual(sales_response.status_code, status.HTTP_200_OK)
        
        # Test access to sales approval endpoints (should be restricted)
        sales_approval_url = reverse('sales:approve', args=[str(uuid.uuid4())])
        sales_approval_response = self.client.post(
            sales_approval_url,
            {},
            format='json'
        )
        self.assertEqual(sales_approval_response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test access to inventory endpoints
        inventory_url = reverse('inventory:list')
        inventory_response = self.client.get(inventory_url)
        self.assertEqual(inventory_response.status_code, status.HTTP_200_OK)
        
        # Test access to inventory management endpoints (should be restricted)
        inventory_management_url = reverse('inventory:manage')
        inventory_management_response = self.client.post(
            inventory_management_url,
            {
                'action': 'adjust',
                'brand_id': str(uuid.uuid4()),
                'quantity': 10,
                'reason': 'Test adjustment'
            },
            format='json'
        )
        self.assertEqual(inventory_management_response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_tenant_isolation(self):
        """Test tenant isolation in API endpoints."""
        # Create another tenant
        another_tenant = Tenant.objects.create(
            name="Another Tenant",
            status="active"
        )
        
        # Create shop for another tenant
        another_shop = AuthShop.objects.create(
            name="Another Shop",
            tenant_id=another_tenant.id,
            code="ANT01",
            shop_type="retail",
            status="active",
            address="456 Another St",
            city="Another City",
            state="Another State",
            country="Another Country",
            postal_code="54321",
            phone="9876543210",
            license_number="LIC654321",
            license_type="Retail",
            license_expiry="2025-12-31",
            opening_time="09:00:00",
            closing_time="21:00:00"
        )
        
        # Create user for another tenant
        another_user = AuthUser.objects.create_user(
            username="another@test.com",
            email="another@test.com",
            password="Another@123",
            first_name="Another",
            last_name="User",
            tenant=another_tenant,
            role=self.admin_role
        )
        
        # Login as admin from first tenant
        login_url = reverse('auth:login')
        login_response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'Admin@123'
            },
            format='json'
        )
        
        # Set token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["token"]}')
        
        # Try to access shop from another tenant
        shop_url = reverse('auth:shop-detail', args=[str(another_shop.id)])
        shop_response = self.client.get(shop_url)
        
        # Verify response (should be 404 Not Found)
        self.assertEqual(shop_response.status_code, status.HTTP_404_NOT_FOUND)

class TestInputValidationSecurity(TestCase):
    """
    Test the input validation security of the API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            status="active"
        )
        
        # Create test shop
        self.shop = AuthShop.objects.create(
            name="Test Shop",
            tenant_id=self.tenant.id,
            code="TST01",
            shop_type="retail",
            status="active",
            address="123 Test St",
            city="Test City",
            state="Test State",
            country="Test Country",
            postal_code="12345",
            phone="1234567890",
            license_number="LIC123456",
            license_type="Retail",
            license_expiry="2025-12-31",
            opening_time="09:00:00",
            closing_time="21:00:00"
        )
        
        # Create test role
        self.admin_role = Role.objects.create(
            name="Admin",
            tenant=self.tenant
        )
        
        # Create test user
        self.admin_user = AuthUser.objects.create_user(
            username="admin@test.com",
            email="admin@test.com",
            password="Admin@123",
            first_name="Admin",
            last_name="User",
            tenant=self.tenant,
            role=self.admin_role
        )
        
        # Create API client
        self.client = APIClient()
        
        # Login and set token
        login_url = reverse('auth:login')
        login_response = self.client.post(
            login_url,
            {
                'username': 'admin@test.com',
                'password': 'Admin@123'
            },
            format='json'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["token"]}')
    
    def test_sql_injection_prevention(self):
        """Test prevention of SQL injection attacks."""
        # Test SQL injection in query parameters
        users_url = reverse('auth:users-list')
        sql_injection_url = f"{users_url}?search=admin'; DROP TABLE users; --"
        
        response = self.client.get(sql_injection_url)
        
        # Verify response (should not cause a 500 error)
        self.assertNotEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def test_xss_prevention(self):
        """Test prevention of Cross-Site Scripting (XSS) attacks."""
        # Create user with XSS payload in name
        xss_payload = '<script>alert("XSS")</script>'
        
        user_create_url = reverse('auth:users-create')
        response = self.client.post(
            user_create_url,
            {
                'username': 'xss@test.com',
                'email': 'xss@test.com',
                'password': 'Xss@123',
                'first_name': xss_payload,
                'last_name': 'User',
                'role_id': str(self.admin_role.id),
                'shop_id': str(self.shop.id)
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Get user details
        user_id = response.data['id']
        user_detail_url = reverse('auth:users-detail', args=[user_id])
        detail_response = self.client.get(user_detail_url)
        
        # Verify that XSS payload is escaped
        self.assertNotEqual(detail_response.data['first_name'], xss_payload)
        self.assertIn('&lt;script&gt;', detail_response.data['first_name'])
    
    def test_input_validation(self):
        """Test input validation for API endpoints."""
        # Test with missing required fields
        user_create_url = reverse('auth:users-create')
        response = self.client.post(
            user_create_url,
            {
                'email': 'missing@test.com',
                # Missing username, password, etc.
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        
        # Test with invalid email format
        response = self.client.post(
            user_create_url,
            {
                'username': 'invalid',
                'email': 'invalid-email',
                'password': 'Invalid@123',
                'first_name': 'Invalid',
                'last_name': 'User',
                'role_id': str(self.admin_role.id),
                'shop_id': str(self.shop.id)
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        
        # Test with weak password
        response = self.client.post(
            user_create_url,
            {
                'username': 'weak@test.com',
                'email': 'weak@test.com',
                'password': 'weak',  # Too short and simple
                'first_name': 'Weak',
                'last_name': 'User',
                'role_id': str(self.admin_role.id),
                'shop_id': str(self.shop.id)
            },
            format='json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

class TestRateLimitingSecurity(TestCase):
    """
    Test the rate limiting security of the API endpoints.
    """
    
    @override_settings(
        REST_FRAMEWORK={
            'DEFAULT_THROTTLE_CLASSES': [
                'rest_framework.throttling.UserRateThrottle',
                'rest_framework.throttling.AnonRateThrottle',
            ],
            'DEFAULT_THROTTLE_RATES': {
                'user': '100/hour',
                'anon': '20/hour',
            }
        }
    )
    def test_login_rate_limiting(self):
        """Test rate limiting for login attempts."""
        login_url = reverse('auth:login')
        
        # Make multiple login attempts
        for i in range(25):  # More than the anonymous rate limit
            response = self.client.post(
                login_url,
                {
                    'username': f'user{i}@test.com',
                    'password': 'WrongPassword'
                },
                format='json'
            )
            
            # If we hit the rate limit, break
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        
        # Verify that we hit the rate limit
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn('detail', response.data)

class TestCSRFProtection(TestCase):
    """
    Test the CSRF protection of the API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        # Create test client
        self.client = Client(enforce_csrf_checks=True)
    
    def test_csrf_protection(self):
        """Test CSRF protection for non-API endpoints."""
        # Get CSRF token
        response = self.client.get('/admin/login/')
        csrf_token = response.cookies['csrftoken'].value
        
        # Test login without CSRF token
        login_response = self.client.post(
            '/admin/login/',
            {
                'username': 'admin',
                'password': 'admin'
            }
        )
        
        # Verify response (should be 403 Forbidden due to CSRF protection)
        self.assertEqual(login_response.status_code, 403)
        
        # Test login with CSRF token
        login_response = self.client.post(
            '/admin/login/',
            {
                'username': 'admin',
                'password': 'admin',
                'csrfmiddlewaretoken': csrf_token
            }
        )
        
        # Verify response (should not be 403 Forbidden)
        self.assertNotEqual(login_response.status_code, 403)
