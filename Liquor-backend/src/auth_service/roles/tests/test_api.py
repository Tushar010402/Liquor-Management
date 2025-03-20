import uuid
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Role, Permission, Tenant

User = get_user_model()

class RolesAPITest(TestCase):
    """
    Test the roles API endpoints.
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
        self.permission3 = Permission.objects.create(
            name="Delete Products",
            code="delete_products",
            description="Can delete products"
        )
        self.permission4 = Permission.objects.create(
            name="View Orders",
            code="view_orders",
            description="Can view orders"
        )
        self.permission5 = Permission.objects.create(
            name="Edit Orders",
            code="edit_orders",
            description="Can edit orders"
        )
        
        # Create roles
        self.admin_role = Role.objects.create(
            name="Admin",
            description="Tenant Administrator"
        )
        self.admin_role.permissions.add(
            self.permission1, self.permission2, self.permission3,
            self.permission4, self.permission5
        )
        
        self.manager_role = Role.objects.create(
            name="Manager",
            description="Shop Manager"
        )
        self.manager_role.permissions.add(
            self.permission1, self.permission2, self.permission4
        )
        
        self.executive_role = Role.objects.create(
            name="Executive",
            description="Sales Executive"
        )
        self.executive_role.permissions.add(
            self.permission1, self.permission4
        )
        
        # Create users
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="adminpassword",
            full_name="Admin User",
            tenant_id=self.tenant_id,
            role=User.ROLE_TENANT_ADMIN,
            is_active=True
        )
        
        self.manager_user = User.objects.create_user(
            email="manager@test.com",
            password="managerpassword",
            full_name="Manager User",
            tenant_id=self.tenant_id,
            role=User.ROLE_MANAGER,
            is_active=True
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
    
    def test_list_roles(self):
        """
        Test listing roles.
        """
        url = reverse('role-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        
        # Check that the response contains the expected roles
        role_names = [role['name'] for role in response.data['results']]
        self.assertIn('Admin', role_names)
        self.assertIn('Manager', role_names)
        self.assertIn('Executive', role_names)
    
    def test_list_roles_permission_denied(self):
        """
        Test that non-admin users cannot list roles.
        """
        url = reverse('role-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_role(self):
        """
        Test creating a role.
        """
        url = reverse('role-list')
        data = {
            'name': 'Supervisor',
            'description': 'Department Supervisor',
            'permissions': [
                str(self.permission1.id),
                str(self.permission2.id),
                str(self.permission4.id)
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Supervisor')
        self.assertEqual(response.data['description'], 'Department Supervisor')
        self.assertEqual(len(response.data['permissions']), 3)
        
        # Check that the role was created in the database
        role = Role.objects.get(name='Supervisor')
        self.assertEqual(role.description, 'Department Supervisor')
        self.assertEqual(role.permissions.count(), 3)
    
    def test_create_role_permission_denied(self):
        """
        Test that non-admin users cannot create roles.
        """
        url = reverse('role-list')
        data = {
            'name': 'Cashier',
            'description': 'Store Cashier',
            'permissions': [str(self.permission1.id)]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_role(self):
        """
        Test retrieving a role.
        """
        url = reverse('role-detail', args=[self.manager_role.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Manager')
        self.assertEqual(response.data['description'], 'Shop Manager')
        self.assertEqual(len(response.data['permissions']), 3)
        
        # Check that the permissions are correct
        permission_codes = [
            Permission.objects.get(id=uuid.UUID(perm_id)).code
            for perm_id in response.data['permissions']
        ]
        self.assertIn('view_products', permission_codes)
        self.assertIn('edit_products', permission_codes)
        self.assertIn('view_orders', permission_codes)
    
    def test_update_role(self):
        """
        Test updating a role.
        """
        url = reverse('role-detail', args=[self.executive_role.id])
        data = {
            'description': 'Updated Sales Executive',
            'permissions': [
                str(self.permission1.id),
                str(self.permission4.id),
                str(self.permission5.id)
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Executive')
        self.assertEqual(response.data['description'], 'Updated Sales Executive')
        self.assertEqual(len(response.data['permissions']), 3)
        
        # Check that the role was updated in the database
        self.executive_role.refresh_from_db()
        self.assertEqual(self.executive_role.description, 'Updated Sales Executive')
        self.assertEqual(self.executive_role.permissions.count(), 3)
        
        # Check that the permissions were updated
        permission_codes = [perm.code for perm in self.executive_role.permissions.all()]
        self.assertIn('view_products', permission_codes)
        self.assertIn('view_orders', permission_codes)
        self.assertIn('edit_orders', permission_codes)
    
    def test_update_role_permission_denied(self):
        """
        Test that non-admin users cannot update roles.
        """
        url = reverse('role-detail', args=[self.executive_role.id])
        data = {
            'description': 'Should Not Update'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_role(self):
        """
        Test deleting a role.
        """
        # Create a new role to delete
        role_to_delete = Role.objects.create(
            name="Temporary Role",
            description="Role to be deleted"
        )
        
        url = reverse('role-detail', args=[role_to_delete.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the role was deleted from the database
        with self.assertRaises(Role.DoesNotExist):
            Role.objects.get(id=role_to_delete.id)
    
    def test_delete_role_permission_denied(self):
        """
        Test that non-admin users cannot delete roles.
        """
        url = reverse('role-detail', args=[self.executive_role.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_permissions(self):
        """
        Test listing permissions.
        """
        url = reverse('permission-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        # Check that the response contains the expected permissions
        permission_codes = [perm['code'] for perm in response.data['results']]
        self.assertIn('view_products', permission_codes)
        self.assertIn('edit_products', permission_codes)
        self.assertIn('delete_products', permission_codes)
        self.assertIn('view_orders', permission_codes)
        self.assertIn('edit_orders', permission_codes)
    
    def test_create_permission(self):
        """
        Test creating a permission.
        """
        url = reverse('permission-list')
        data = {
            'name': 'Create Orders',
            'code': 'create_orders',
            'description': 'Can create new orders'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Create Orders')
        self.assertEqual(response.data['code'], 'create_orders')
        self.assertEqual(response.data['description'], 'Can create new orders')
        
        # Check that the permission was created in the database
        permission = Permission.objects.get(code='create_orders')
        self.assertEqual(permission.name, 'Create Orders')
        self.assertEqual(permission.description, 'Can create new orders')
    
    def test_retrieve_permission(self):
        """
        Test retrieving a permission.
        """
        url = reverse('permission-detail', args=[self.permission1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'View Products')
        self.assertEqual(response.data['code'], 'view_products')
        self.assertEqual(response.data['description'], 'Can view products')
    
    def test_update_permission(self):
        """
        Test updating a permission.
        """
        url = reverse('permission-detail', args=[self.permission3.id])
        data = {
            'description': 'Updated: Can delete products from inventory'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Delete Products')
        self.assertEqual(response.data['code'], 'delete_products')
        self.assertEqual(response.data['description'], 'Updated: Can delete products from inventory')
        
        # Check that the permission was updated in the database
        self.permission3.refresh_from_db()
        self.assertEqual(self.permission3.description, 'Updated: Can delete products from inventory')
    
    def test_get_role_permissions(self):
        """
        Test getting permissions for a specific role.
        """
        url = reverse('role-permissions', args=[self.manager_role.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Check that the response contains the expected permissions
        permission_codes = [perm['code'] for perm in response.data]
        self.assertIn('view_products', permission_codes)
        self.assertIn('edit_products', permission_codes)
        self.assertIn('view_orders', permission_codes)