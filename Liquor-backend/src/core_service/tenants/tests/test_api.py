import uuid
import json
from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from common.jwt_auth import MicroserviceUser
from core_service.tenants.models import Tenant, TenantSettings

class TenantAPITest(TestCase):
    """
    Test the tenant API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.admin_id = uuid.uuid4()
        
        self.admin_user = MicroserviceUser({
            'id': str(self.admin_id),
            'email': 'admin@example.com',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
            'role': 'system_admin',
            'permissions': ['view_tenant', 'add_tenant', 'change_tenant', 'delete_tenant']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.admin_user)
        
        # Create tenant
        self.tenant = Tenant.objects.create(
            name="Liquor Enterprises",
            slug="liquor-enterprises",
            address="456 Business Avenue",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10001",
            phone="212-555-1234",
            email="info@liquorenterprises.com",
            website="https://www.liquorenterprises.com",
            business_type="Retail",
            tax_id="TAX-987654321",
            license_number="LIQ-2023-12345",
            license_expiry=date(2024, 12, 31),
            subscription_plan="premium",
            subscription_start_date=date(2023, 1, 1),
            subscription_end_date=date(2023, 12, 31),
            max_shops=10,
            max_users=50,
            contact_person_name="John Smith",
            contact_person_email="john.smith@liquorenterprises.com",
            contact_person_phone="212-555-5678",
            primary_color="#4a6da7",
            secondary_color="#ffffff",
            created_by=self.admin_id
        )
        
        # Create tenant settings
        self.tenant_settings = TenantSettings.objects.create(
            tenant=self.tenant,
            timezone="America/New_York",
            date_format="MM/DD/YYYY",
            time_format="hh:mm A",
            currency="USD",
            language="en-US",
            fiscal_year_start="01-01",
            tax_rate=Decimal('8.875'),
            enable_tax=True,
            require_2fa=True,
            password_expiry_days=60,
            session_timeout_minutes=15,
            enable_email_notifications=True,
            enable_sms_notifications=True,
            require_sales_approval=True,
            require_purchase_approval=True,
            require_expense_approval=True,
            enable_inventory_management=True,
            enable_financial_management=True,
            enable_reports=True,
            enable_analytics=True,
            created_by=self.admin_id
        )
        
        # Create another tenant
        self.tenant2 = Tenant.objects.create(
            name="Wine Distributors",
            slug="wine-distributors",
            address="789 Wine Street",
            city="San Francisco",
            state="CA",
            country="USA",
            postal_code="94107",
            subscription_plan="basic",
            created_by=self.admin_id
        )
    
    def test_list_tenants(self):
        """
        Test listing tenants.
        """
        url = reverse('tenant-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Liquor Enterprises")
        self.assertEqual(response.data['results'][1]['name'], "Wine Distributors")
    
    def test_retrieve_tenant(self):
        """
        Test retrieving a tenant.
        """
        url = reverse('tenant-detail', args=[self.tenant.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Liquor Enterprises")
        self.assertEqual(response.data['slug'], "liquor-enterprises")
        self.assertEqual(response.data['address'], "456 Business Avenue")
        self.assertEqual(response.data['city'], "New York")
        self.assertEqual(response.data['state'], "NY")
        self.assertEqual(response.data['country'], "USA")
        self.assertEqual(response.data['postal_code'], "10001")
        self.assertEqual(response.data['phone'], "212-555-1234")
        self.assertEqual(response.data['email'], "info@liquorenterprises.com")
        self.assertEqual(response.data['website'], "https://www.liquorenterprises.com")
        self.assertEqual(response.data['business_type'], "Retail")
        self.assertEqual(response.data['tax_id'], "TAX-987654321")
        self.assertEqual(response.data['license_number'], "LIQ-2023-12345")
        self.assertEqual(response.data['license_expiry'], "2024-12-31")
        self.assertEqual(response.data['subscription_plan'], "premium")
        self.assertEqual(response.data['subscription_start_date'], "2023-01-01")
        self.assertEqual(response.data['subscription_end_date'], "2023-12-31")
        self.assertEqual(response.data['max_shops'], 10)
        self.assertEqual(response.data['max_users'], 50)
        self.assertEqual(response.data['contact_person_name'], "John Smith")
        self.assertEqual(response.data['contact_person_email'], "john.smith@liquorenterprises.com")
        self.assertEqual(response.data['contact_person_phone'], "212-555-5678")
        self.assertEqual(response.data['primary_color'], "#4a6da7")
        self.assertEqual(response.data['secondary_color'], "#ffffff")
    
    def test_create_tenant(self):
        """
        Test creating a tenant.
        """
        url = reverse('tenant-list')
        data = {
            'name': "Beer Wholesalers",
            'slug': "beer-wholesalers",
            'address': "123 Beer Street",
            'city': "Chicago",
            'state': "IL",
            'country': "USA",
            'postal_code': "60601",
            'phone': "312-555-1234",
            'email': "info@beerwholesalers.com",
            'website': "https://www.beerwholesalers.com",
            'business_type': "Wholesale",
            'tax_id': "TAX-123456789",
            'license_number': "LIQ-2023-67890",
            'license_expiry': "2024-12-31",
            'subscription_plan': "standard",
            'subscription_start_date': "2023-01-01",
            'subscription_end_date': "2023-12-31",
            'max_shops': 5,
            'max_users': 25,
            'contact_person_name': "Jane Doe",
            'contact_person_email': "jane.doe@beerwholesalers.com",
            'contact_person_phone': "312-555-5678",
            'primary_color': "#a76d4a",
            'secondary_color': "#f5f5f5"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Beer Wholesalers")
        self.assertEqual(response.data['slug'], "beer-wholesalers")
        
        # Check that the tenant was created in the database
        tenant = Tenant.objects.get(slug="beer-wholesalers")
        self.assertEqual(tenant.name, "Beer Wholesalers")
        self.assertEqual(tenant.city, "Chicago")
        self.assertEqual(tenant.subscription_plan, "standard")
        self.assertEqual(tenant.created_by, self.admin_id)
        
        # Check that tenant settings were automatically created
        settings = TenantSettings.objects.get(tenant=tenant)
        self.assertEqual(settings.tenant, tenant)
        self.assertEqual(settings.timezone, "UTC")  # Default value
        self.assertEqual(settings.currency, "USD")  # Default value
    
    def test_update_tenant(self):
        """
        Test updating a tenant.
        """
        url = reverse('tenant-detail', args=[self.tenant.id])
        data = {
            'name': "Updated Liquor Enterprises",
            'address': "789 Updated Avenue",
            'subscription_plan': "enterprise",
            'max_shops': 20,
            'max_users': 100
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Liquor Enterprises")
        self.assertEqual(response.data['address'], "789 Updated Avenue")
        self.assertEqual(response.data['subscription_plan'], "enterprise")
        self.assertEqual(response.data['max_shops'], 20)
        self.assertEqual(response.data['max_users'], 100)
        
        # Check that the tenant was updated in the database
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.name, "Updated Liquor Enterprises")
        self.assertEqual(self.tenant.address, "789 Updated Avenue")
        self.assertEqual(self.tenant.subscription_plan, "enterprise")
        self.assertEqual(self.tenant.max_shops, 20)
        self.assertEqual(self.tenant.max_users, 100)
    
    def test_delete_tenant(self):
        """
        Test deleting a tenant.
        """
        url = reverse('tenant-detail', args=[self.tenant2.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the tenant was deleted from the database
        with self.assertRaises(Tenant.DoesNotExist):
            Tenant.objects.get(id=self.tenant2.id)
    
    def test_get_tenant_settings(self):
        """
        Test getting tenant settings.
        """
        url = reverse('tenant-settings', args=[self.tenant.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timezone'], "America/New_York")
        self.assertEqual(response.data['date_format'], "MM/DD/YYYY")
        self.assertEqual(response.data['time_format'], "hh:mm A")
        self.assertEqual(response.data['currency'], "USD")
        self.assertEqual(response.data['language'], "en-US")
        self.assertEqual(response.data['fiscal_year_start'], "01-01")
        self.assertEqual(response.data['tax_rate'], '8.875')
        self.assertTrue(response.data['enable_tax'])
        self.assertTrue(response.data['require_2fa'])
        self.assertEqual(response.data['password_expiry_days'], 60)
        self.assertEqual(response.data['session_timeout_minutes'], 15)
        self.assertTrue(response.data['enable_email_notifications'])
        self.assertTrue(response.data['enable_sms_notifications'])
        self.assertTrue(response.data['require_sales_approval'])
        self.assertTrue(response.data['require_purchase_approval'])
        self.assertTrue(response.data['require_expense_approval'])
        self.assertTrue(response.data['enable_inventory_management'])
        self.assertTrue(response.data['enable_financial_management'])
        self.assertTrue(response.data['enable_reports'])
        self.assertTrue(response.data['enable_analytics'])
    
    def test_update_tenant_settings(self):
        """
        Test updating tenant settings.
        """
        url = reverse('tenant-settings', args=[self.tenant.id])
        data = {
            'timezone': "America/Los_Angeles",
            'tax_rate': '9.5',
            'require_2fa': False,
            'password_expiry_days': 90,
            'enable_sms_notifications': False
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timezone'], "America/Los_Angeles")
        self.assertEqual(response.data['tax_rate'], '9.5')
        self.assertFalse(response.data['require_2fa'])
        self.assertEqual(response.data['password_expiry_days'], 90)
        self.assertFalse(response.data['enable_sms_notifications'])
        
        # Check that the settings were updated in the database
        self.tenant_settings.refresh_from_db()
        self.assertEqual(self.tenant_settings.timezone, "America/Los_Angeles")
        self.assertEqual(self.tenant_settings.tax_rate, Decimal('9.5'))
        self.assertFalse(self.tenant_settings.require_2fa)
        self.assertEqual(self.tenant_settings.password_expiry_days, 90)
        self.assertFalse(self.tenant_settings.enable_sms_notifications)
    
    def test_create_tenant_settings_if_not_exists(self):
        """
        Test that settings are created if they don't exist when updating.
        """
        # Delete existing settings for tenant2
        if hasattr(self.tenant2, 'settings'):
            self.tenant2.settings.delete()
        
        url = reverse('tenant-settings', args=[self.tenant2.id])
        data = {
            'timezone': "America/Chicago",
            'tax_rate': '10.25',
            'currency': 'USD'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timezone'], "America/Chicago")
        self.assertEqual(response.data['tax_rate'], '10.25')
        self.assertEqual(response.data['currency'], 'USD')
        
        # Check that new settings were created in the database
        settings = TenantSettings.objects.get(tenant=self.tenant2)
        self.assertEqual(settings.timezone, "America/Chicago")
        self.assertEqual(settings.tax_rate, Decimal('10.25'))
        self.assertEqual(settings.currency, 'USD')
        self.assertEqual(settings.created_by, self.admin_id)
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to tenant endpoints.
        """
        # Create a user without tenant permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_tenant']  # Only has view permission
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        # Try to create a tenant (should fail)
        url = reverse('tenant-list')
        data = {
            'name': "Test Tenant",
            'slug': "test-tenant"
        }
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to update a tenant (should fail)
        url = reverse('tenant-detail', args=[self.tenant.id])
        data = {
            'name': "Updated Name"
        }
        response = client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to delete a tenant (should fail)
        url = reverse('tenant-detail', args=[self.tenant.id])
        response = client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # View a tenant (should succeed)
        url = reverse('tenant-detail', args=[self.tenant.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_tenants(self):
        """
        Test searching for tenants.
        """
        url = reverse('tenant-list')
        response = self.client.get(url, {'search': 'Liquor'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Liquor Enterprises")
        
        # Search by city
        response = self.client.get(url, {'search': 'San Francisco'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Wine Distributors")
        
        # Search with no results
        response = self.client.get(url, {'search': 'Nonexistent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_filter_tenants(self):
        """
        Test filtering tenants.
        """
        # Filter by subscription_plan
        url = reverse('tenant-list')
        response = self.client.get(url, {'subscription_plan': 'premium'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Liquor Enterprises")
        
        # Filter by country
        response = self.client.get(url, {'country': 'USA'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by state
        response = self.client.get(url, {'state': 'CA'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Wine Distributors")
    
    def test_tenant_slug_validation(self):
        """
        Test validation of tenant slug.
        """
        url = reverse('tenant-list')
        
        # Test with invalid slug (spaces)
        data = {
            'name': "Invalid Slug Tenant",
            'slug': "invalid slug",
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('slug', response.data)
        
        # Test with invalid slug (special characters)
        data = {
            'name': "Invalid Slug Tenant",
            'slug': "invalid@slug",
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('slug', response.data)
        
        # Test with valid slug
        data = {
            'name': "Valid Slug Tenant",
            'slug': "valid-slug",
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['slug'], "valid-slug")
    
    def test_tenant_with_settings_creation(self):
        """
        Test creating a tenant with settings in a single request.
        """
        url = reverse('tenant-list')
        data = {
            'name': "Tenant With Settings",
            'slug': "tenant-with-settings",
            'settings': {
                'timezone': "Europe/London",
                'currency': "GBP",
                'tax_rate': "20.00",
                'language': "en-GB"
            }
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Tenant With Settings")
        self.assertEqual(response.data['slug'], "tenant-with-settings")
        
        # Check that the tenant was created in the database
        tenant = Tenant.objects.get(slug="tenant-with-settings")
        self.assertEqual(tenant.name, "Tenant With Settings")
        
        # Check that tenant settings were created with the specified values
        settings = TenantSettings.objects.get(tenant=tenant)
        self.assertEqual(settings.timezone, "Europe/London")
        self.assertEqual(settings.currency, "GBP")
        self.assertEqual(settings.tax_rate, Decimal('20.00'))
        self.assertEqual(settings.language, "en-GB")