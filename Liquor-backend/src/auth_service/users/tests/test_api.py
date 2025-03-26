import uuid
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserShopAssignment, UserPermission
from authentication.models import Role, Permission, Tenant

User = get_user_model()

class UsersAPITest(TestCase):
    """
    Test the users API endpoints.
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
        self.tenant_id = self.tenant.id
        
        # Create shop ID
        self.shop_id = uuid.uuid4()
        
        # Create permissions
        self.permission1 = Permission.objects.create(
            name="View Users",
            code="view_users",
            description="Can view users"
        )
        self.permission2 = Permission.objects.create(
            name="Edit Users",
            code="edit_users",
            description="Can edit users"
        )
        self.permission3 = Permission.objects.create(
            name="Delete Users",
            code="delete_users",
            description="Can delete users"
        )
        
        # Create roles
        self.admin_role = Role.objects.create(
            name="Admin",
            description="Tenant Administrator"
        )
        self.admin_role.permissions.add(self.permission1, self.permission2, self.permission3)
        
        self.manager_role = Role.objects.create(
            name="Manager",
            description="Shop Manager"
        )
        self.manager_role.permissions.add(self.permission1, self.permission2)
        
        # Create users
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="adminpassword",
            full_name="Admin User",
            phone="1234567890",
            tenant_id=self.tenant_id,
            role=User.ROLE_TENANT_ADMIN,
            is_active=True
        )
        
        self.manager_user = User.objects.create_user(
            email="manager@test.com",
            password="managerpassword",
            full_name="Manager User",
            phone="1234567891",
            tenant_id=self.tenant_id,
            role=User.ROLE_MANAGER,
            is_active=True
        )
        
        self.executive_user = User.objects.create_user(
            email="executive@test.com",
            password="executivepassword",
            full_name="Executive User",
            phone="1234567892",
            tenant_id=self.tenant_id,
            role=User.ROLE_EXECUTIVE,
            is_active=True
        )
        
        # Create shop assignment
        self.shop_assignment = UserShopAssignment.objects.create(
            tenant_id=self.tenant_id,
            user=self.manager_user,
            shop_id=self.shop_id,
            is_primary=True,
            created_by=self.admin_user.id
        )
        
        # Create custom permission
        self.user_permission = UserPermission.objects.create(
            tenant_id=self.tenant_id,
            user=self.executive_user,
            permission_key="can_view_reports",
            created_by=self.admin_user.id
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Login as admin user
        login_url = reverse('login')
        login_data = {
            'email': 'admin@test.com',
            'password': 'adminpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.admin_token = login_response.data['data']['access_token']
        
        # Login as manager user
        login_data = {
            'email': 'manager@test.com',
            'password': 'managerpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.manager_token = login_response.data['data']['access_token']
    
    def test_list_users(self):
        """
        Test listing users.
        """
        url = reverse('user-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        
        # Check that the response contains the expected users
        emails = [user['email'] for user in response.data['results']]
        self.assertIn('admin@test.com', emails)
        self.assertIn('manager@test.com', emails)
        self.assertIn('executive@test.com', emails)
    
    def test_list_users_permission_denied(self):
        """
        Test that non-admin users cannot list all users.
        """
        url = reverse('user-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.get(url)
        
        # Managers should only see users in their shops, not all users
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_user(self):
        """
        Test creating a user.
        """
        url = reverse('user-list')
        data = {
            'email': 'newuser@test.com',
            'password': 'newuserpassword',
            'full_name': 'New User',
            'phone': '9876543210',
            'role': User.ROLE_EXECUTIVE,
            'tenant_id': str(self.tenant_id)
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@test.com')
        self.assertEqual(response.data['full_name'], 'New User')
        self.assertEqual(response.data['phone'], '9876543210')
        self.assertEqual(response.data['role'], User.ROLE_EXECUTIVE)
        self.assertEqual(response.data['tenant_id'], str(self.tenant_id))
        
        # Check that the user was created in the database
        user = User.objects.get(email='newuser@test.com')
        self.assertEqual(user.full_name, 'New User')
        self.assertEqual(user.tenant_id, self.tenant_id)
    
    def test_create_user_permission_denied(self):
        """
        Test that non-admin users cannot create users.
        """
        url = reverse('user-list')
        data = {
            'email': 'anotheruser@test.com',
            'password': 'anotherpassword',
            'full_name': 'Another User',
            'phone': '5555555555',
            'role': User.ROLE_EXECUTIVE,
            'tenant_id': str(self.tenant_id)
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_user(self):
        """
        Test retrieving a user.
        """
        url = reverse('user-detail', args=[self.executive_user.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'executive@test.com')
        self.assertEqual(response.data['full_name'], 'Executive User')
        self.assertEqual(response.data['phone'], '1234567892')
        self.assertEqual(response.data['role'], User.ROLE_EXECUTIVE)
        self.assertEqual(response.data['tenant_id'], str(self.tenant_id))
    
    def test_update_user(self):
        """
        Test updating a user.
        """
        url = reverse('user-detail', args=[self.executive_user.id])
        data = {
            'full_name': 'Updated Executive User',
            'phone': '9999999999'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Updated Executive User')
        self.assertEqual(response.data['phone'], '9999999999')
        
        # Check that the user was updated in the database
        self.executive_user.refresh_from_db()
        self.assertEqual(self.executive_user.full_name, 'Updated Executive User')
        self.assertEqual(self.executive_user.phone, '9999999999')
    
    def test_update_user_permission_denied(self):
        """
        Test that non-admin users cannot update other users.
        """
        url = reverse('user-detail', args=[self.executive_user.id])
        data = {
            'full_name': 'Should Not Update',
            'phone': '1111111111'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_deactivate_user(self):
        """
        Test deactivating a user.
        """
        url = reverse('user-deactivate', args=[self.executive_user.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])
        
        # Check that the user was deactivated in the database
        self.executive_user.refresh_from_db()
        self.assertFalse(self.executive_user.is_active)
    
    def test_activate_user(self):
        """
        Test activating a user.
        """
        # First deactivate the user
        self.executive_user.is_active = False
        self.executive_user.save()
        
        url = reverse('user-activate', args=[self.executive_user.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_active'])
        
        # Check that the user was activated in the database
        self.executive_user.refresh_from_db()
        self.assertTrue(self.executive_user.is_active)
    
    def test_change_user_password(self):
        """
        Test changing a user's password.
        """
        url = reverse('user-change-password', args=[self.executive_user.id])
        data = {
            'new_password': 'newexecutivepassword'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Check that the password was changed by trying to login
        login_url = reverse('login')
        login_data = {
            'email': 'executive@test.com',
            'password': 'newexecutivepassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
    
    def test_list_user_shop_assignments(self):
        """
        Test listing user shop assignments.
        """
        url = reverse('usershopassignment-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user'], str(self.manager_user.id))
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
        self.assertTrue(response.data['results'][0]['is_primary'])
    
    def test_create_user_shop_assignment(self):
        """
        Test creating a user shop assignment.
        """
        new_shop_id = uuid.uuid4()
        url = reverse('usershopassignment-list')
        data = {
            'user': str(self.executive_user.id),
            'shop_id': str(new_shop_id),
            'is_primary': True
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], str(self.executive_user.id))
        self.assertEqual(response.data['shop_id'], str(new_shop_id))
        self.assertTrue(response.data['is_primary'])
        
        # Check that the assignment was created in the database
        assignment = UserShopAssignment.objects.get(user=self.executive_user, shop_id=new_shop_id)
        self.assertTrue(assignment.is_primary)
    
    def test_delete_user_shop_assignment(self):
        """
        Test deleting a user shop assignment.
        """
        url = reverse('usershopassignment-detail', args=[self.shop_assignment.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the assignment was deleted from the database
        with self.assertRaises(UserShopAssignment.DoesNotExist):
            UserShopAssignment.objects.get(id=self.shop_assignment.id)
    
    def test_list_user_permissions(self):
        """
        Test listing user permissions.
        """
        url = reverse('userpermission-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['user'], str(self.executive_user.id))
        self.assertEqual(response.data['results'][0]['permission_key'], 'can_view_reports')
    
    def test_create_user_permission(self):
        """
        Test creating a user permission.
        """
        url = reverse('userpermission-list')
        data = {
            'user': str(self.manager_user.id),
            'permission_key': 'can_approve_orders'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], str(self.manager_user.id))
        self.assertEqual(response.data['permission_key'], 'can_approve_orders')
        
        # Check that the permission was created in the database
        permission = UserPermission.objects.get(user=self.manager_user, permission_key='can_approve_orders')
        self.assertEqual(permission.permission_key, 'can_approve_orders')
    
    def test_delete_user_permission(self):
        """
        Test deleting a user permission.
        """
        url = reverse('userpermission-detail', args=[self.user_permission.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the permission was deleted from the database
        with self.assertRaises(UserPermission.DoesNotExist):
            UserPermission.objects.get(id=self.user_permission.id)