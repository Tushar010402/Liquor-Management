"""
Security test for JWT authentication and authorization in the Liquor Management System.
This test verifies that the JWT authentication and role-based access control mechanisms
are working correctly.
"""

import json
import uuid
import pytest
import jwt
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import requests
from requests.exceptions import RequestException

# Import JWT configuration
from .jwt_config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_DELTA

# Test configuration
AUTH_SERVICE_URL = 'http://localhost:8001'  # Auth service port
INVENTORY_SERVICE_URL = 'http://localhost:8002'  # Inventory service port
SALES_SERVICE_URL = 'http://localhost:8004'  # Sales service port

class TestJWTAuthentication:
    """
    Test JWT authentication and authorization.
    """
    
    def test_generate_valid_token(self):
        """
        Test generating a valid JWT token.
        """
        # Test data
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        role = 'manager'
        
        # Generate token
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Verify token
        decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        assert decoded_payload['user_id'] == user_id
        assert decoded_payload['tenant_id'] == tenant_id
        assert decoded_payload['role'] == role
        assert 'exp' in decoded_payload
    
    def test_expired_token(self):
        """
        Test that an expired token is rejected.
        """
        # Test data
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        role = 'manager'
        
        # Generate expired token
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.utcnow() - timedelta(seconds=10)  # Expired 10 seconds ago
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Verify token is rejected
        with pytest.raises(jwt.ExpiredSignatureError):
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    
    def test_invalid_signature(self):
        """
        Test that a token with an invalid signature is rejected.
        """
        # Test data
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        role = 'manager'
        
        # Generate token with a different secret key
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
        }
        token = jwt.encode(payload, 'wrong_secret_key', algorithm=JWT_ALGORITHM)
        
        # Verify token is rejected
        with pytest.raises(jwt.InvalidSignatureError):
            jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    
    @patch('requests.post')
    def test_login_endpoint(self, mock_post):
        """
        Test the login endpoint.
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'token': 'mock_token',
            'user': {
                'id': str(uuid.uuid4()),
                'email': 'test@example.com',
                'role': 'manager'
            }
        }
        mock_post.return_value = mock_response
        
        # Test data
        email = 'test@example.com'
        password = 'password123'
        
        # Send login request
        response = requests.post(
            f'{AUTH_SERVICE_URL}/api/auth/login',
            json={'email': email, 'password': password}
        )
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == email
    
    @patch('requests.post')
    def test_login_invalid_credentials(self, mock_post):
        """
        Test login with invalid credentials.
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            'error': 'Invalid credentials'
        }
        mock_post.return_value = mock_response
        
        # Test data
        email = 'test@example.com'
        password = 'wrong_password'
        
        # Send login request
        response = requests.post(
            f'{AUTH_SERVICE_URL}/api/auth/login',
            json={'email': email, 'password': password}
        )
        
        # Verify response
        assert response.status_code == 401
        data = response.json()
        assert 'error' in data
        assert data['error'] == 'Invalid credentials'

class TestRoleBasedAccessControl:
    """
    Test role-based access control.
    """
    
    @patch('requests.get')
    def test_manager_access_to_sales_approval(self, mock_get):
        """
        Test that a manager can access the sales approval endpoint.
        """
        # Generate token for manager
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        role = 'manager'
        
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': str(uuid.uuid4()),
            'status': 'pending',
            'items': []
        }
        mock_get.return_value = mock_response
        
        # Send request
        sale_id = str(uuid.uuid4())
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{SALES_SERVICE_URL}/api/sales/{sale_id}',
            headers=headers
        )
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
        assert 'status' in data
    
    @patch('requests.get')
    def test_cashier_no_access_to_inventory_management(self, mock_get):
        """
        Test that a cashier cannot access the inventory management endpoint.
        """
        # Generate token for cashier
        user_id = str(uuid.uuid4())
        tenant_id = str(uuid.uuid4())
        role = 'cashier'
        
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            'error': 'Access denied'
        }
        mock_get.return_value = mock_response
        
        # Send request
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{INVENTORY_SERVICE_URL}/api/inventory/stock/adjust',
            headers=headers
        )
        
        # Verify response
        assert response.status_code == 403
        data = response.json()
        assert 'error' in data
        assert data['error'] == 'Access denied'
    
    @patch('requests.get')
    def test_no_token_access_denied(self, mock_get):
        """
        Test that access is denied when no token is provided.
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            'error': 'Authentication required'
        }
        mock_get.return_value = mock_response
        
        # Send request without token
        response = requests.get(
            f'{SALES_SERVICE_URL}/api/sales'
        )
        
        # Verify response
        assert response.status_code == 401
        data = response.json()
        assert 'error' in data
        assert data['error'] == 'Authentication required'
    
    @patch('requests.get')
    def test_tenant_isolation(self, mock_get):
        """
        Test that a user from one tenant cannot access data from another tenant.
        """
        # Generate token for user in tenant A
        user_id = str(uuid.uuid4())
        tenant_id_a = str(uuid.uuid4())
        role = 'manager'
        
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id_a,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_DELTA)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            'error': 'Shop not found'
        }
        mock_get.return_value = mock_response
        
        # Send request to access shop from tenant B
        tenant_id_b = str(uuid.uuid4())
        shop_id = str(uuid.uuid4())
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{INVENTORY_SERVICE_URL}/api/shops/{shop_id}?tenant_id={tenant_id_b}',
            headers=headers
        )
        
        # Verify response
        assert response.status_code == 404
        data = response.json()
        assert 'error' in data
        assert data['error'] == 'Shop not found'

class TestSecurityHeaders:
    """
    Test security headers in API responses.
    """
    
    @patch('requests.get')
    def test_security_headers(self, mock_get):
        """
        Test that security headers are present in API responses.
        """
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': "default-src 'self'",
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
        }
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        # Send request
        response = requests.get(f'{AUTH_SERVICE_URL}/api/health')
        
        # Verify security headers
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        
        assert 'X-XSS-Protection' in response.headers
        assert response.headers['X-XSS-Protection'] == '1; mode=block'
        
        assert 'Content-Security-Policy' in response.headers
        assert "default-src 'self'" in response.headers['Content-Security-Policy']
        
        assert 'Strict-Transport-Security' in response.headers
        assert 'max-age=31536000' in response.headers['Strict-Transport-Security']
