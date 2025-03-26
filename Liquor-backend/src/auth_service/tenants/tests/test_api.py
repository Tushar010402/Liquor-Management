import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from tenants.models import BillingPlan, Tenant, TenantBillingHistory, TenantActivity

User = get_user_model()

class TenantsAPITest(TestCase):
    """
    Test the tenants API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create billing plans
        self.basic_plan = BillingPlan.objects.create(
            name="Basic Plan",
            description="Basic plan for small businesses",
            price_monthly=Decimal('49.99'),
            price_yearly=Decimal('499.99'),
            max_shops=1,
            max_users=5,
            features={
                'inventory_management': True,
                'sales_analytics': True,
                'multi_shop': False,
                'advanced_reporting': False
            },
            is_active=True
        )
        
        self.standard_plan = BillingPlan.objects.create(
            name="Standard Plan",
            description="Standard plan for growing businesses",
            price_monthly=Decimal('99.99'),
            price_yearly=Decimal('999.99'),
            max_shops=3,
            max_users=10,
            features={
                'inventory_management': True,
                'sales_analytics': True,
                'multi_shop': True,
                'advanced_reporting': False
            },
            is_active=True
        )
        
        self.premium_plan = BillingPlan.objects.create(
            name="Premium Plan",
            description="Premium plan for large businesses",
            price_monthly=Decimal('199.99'),
            price_yearly=Decimal('1999.99'),
            max_shops=10,
            max_users=50,
            features={
                'inventory_management': True,
                'sales_analytics': True,
                'multi_shop': True,
                'advanced_reporting': True
            },
            is_active=True
        )
        
        # Create tenants
        self.tenant1 = Tenant.objects.create(
            name="Liquor Shop 1",
            slug="liquor-shop-1",
            domain="liquorshop1.com",
            status=Tenant.STATUS_ACTIVE,
            business_name="Liquor Enterprises 1",
            business_address="123 Main St, City, State, 12345",
            business_phone="1234567890",
            business_email="contact@liquorshop1.com",
            tax_id="TAX123456",
            registration_number="REG123456",
            contact_name="John Doe",
            contact_email="john.doe@liquorshop1.com",
            contact_phone="9876543210",
            billing_plan=self.standard_plan,
            billing_cycle=Tenant.BILLING_MONTHLY,
            billing_address="123 Main St, City, State, 12345",
            billing_email="billing@liquorshop1.com",
            subscription_start_date=date.today(),
            subscription_end_date=date.today() + timedelta(days=30),
            is_trial=False
        )
        
        self.tenant2 = Tenant.objects.create(
            name="Liquor Shop 2",
            slug="liquor-shop-2",
            domain="liquorshop2.com",
            status=Tenant.STATUS_ACTIVE,
            business_name="Liquor Enterprises 2",
            business_address="456 Oak St, City, State, 12345",
            business_phone="2345678901",
            business_email="contact@liquorshop2.com",
            tax_id="TAX234567",
            registration_number="REG234567",
            contact_name="Jane Smith",
            contact_email="jane.smith@liquorshop2.com",
            contact_phone="8765432109",
            billing_plan=self.basic_plan,
            billing_cycle=Tenant.BILLING_YEARLY,
            billing_address="456 Oak St, City, State, 12345",
            billing_email="billing@liquorshop2.com",
            subscription_start_date=date.today() - timedelta(days=30),
            subscription_end_date=date.today() + timedelta(days=335),
            is_trial=False
        )
        
        # Create tenant billing history
        self.billing_history1 = TenantBillingHistory.objects.create(
            tenant=self.tenant1,
            billing_plan=self.standard_plan,
            amount=Decimal('99.99'),
            status=TenantBillingHistory.STATUS_PAID,
            invoice_number="INV-2023-001",
            invoice_date=date.today(),
            due_date=date.today() + timedelta(days=15),
            payment_date=date.today(),
            payment_method="Credit Card",
            payment_reference="PAYMENT123456",
            billing_period_start=date.today(),
            billing_period_end=date.today() + timedelta(days=30),
            notes="Monthly billing"
        )
        
        # Create users
        self.saas_admin = User.objects.create_user(
            email="saas_admin@example.com",
            password="adminpassword",
            full_name="SaaS Admin",
            role=User.ROLE_SAAS_ADMIN,
            is_staff=True,
            is_superuser=True
        )
        
        self.tenant_admin1 = User.objects.create_user(
            email="admin@liquorshop1.com",
            password="password123",
            full_name="Tenant Admin 1",
            tenant_id=self.tenant1.id,
            role=User.ROLE_TENANT_ADMIN
        )
        
        self.tenant_admin2 = User.objects.create_user(
            email="admin@liquorshop2.com",
            password="password123",
            full_name="Tenant Admin 2",
            tenant_id=self.tenant2.id,
            role=User.ROLE_TENANT_ADMIN
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Login as SaaS admin
        login_url = reverse('login')
        login_data = {
            'email': 'saas_admin@example.com',
            'password': 'adminpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.saas_admin_token = login_response.data['data']['access_token']
        
        # Login as tenant admin
        login_data = {
            'email': 'admin@liquorshop1.com',
            'password': 'password123'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.tenant_admin_token = login_response.data['data']['access_token']
    
    def test_list_billing_plans(self):
        """
        Test listing billing plans.
        """
        url = reverse('billingplan-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        
        # Check that the response contains the expected plans
        plan_names = [plan['name'] for plan in response.data['results']]
        self.assertIn('Basic Plan', plan_names)
        self.assertIn('Standard Plan', plan_names)
        self.assertIn('Premium Plan', plan_names)
    
    def test_create_billing_plan(self):
        """
        Test creating a billing plan.
        """
        url = reverse('billingplan-list')
        data = {
            'name': 'Enterprise Plan',
            'description': 'Enterprise plan for large chains',
            'price_monthly': '299.99',
            'price_yearly': '2999.99',
            'max_shops': 20,
            'max_users': 100,
            'features': {
                'inventory_management': True,
                'sales_analytics': True,
                'multi_shop': True,
                'advanced_reporting': True,
                'api_access': True,
                'white_label': True
            },
            'is_active': True
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Enterprise Plan')
        self.assertEqual(response.data['price_monthly'], '299.99')
        self.assertEqual(response.data['max_shops'], 20)
        self.assertTrue(response.data['features']['api_access'])
        
        # Check that the plan was created in the database
        plan = BillingPlan.objects.get(name='Enterprise Plan')
        self.assertEqual(plan.price_yearly, Decimal('2999.99'))
        self.assertEqual(plan.max_users, 100)
    
    def test_retrieve_billing_plan(self):
        """
        Test retrieving a billing plan.
        """
        url = reverse('billingplan-detail', args=[self.standard_plan.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Standard Plan')
        self.assertEqual(response.data['price_monthly'], '99.99')
        self.assertEqual(response.data['max_shops'], 3)
        self.assertTrue(response.data['features']['multi_shop'])
    
    def test_update_billing_plan(self):
        """
        Test updating a billing plan.
        """
        url = reverse('billingplan-detail', args=[self.basic_plan.id])
        data = {
            'price_monthly': '59.99',
            'price_yearly': '599.99',
            'max_users': 8,
            'features': {
                'inventory_management': True,
                'sales_analytics': True,
                'multi_shop': True,
                'advanced_reporting': False
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price_monthly'], '59.99')
        self.assertEqual(response.data['max_users'], 8)
        self.assertTrue(response.data['features']['multi_shop'])
        
        # Check that the plan was updated in the database
        self.basic_plan.refresh_from_db()
        self.assertEqual(self.basic_plan.price_monthly, Decimal('59.99'))
        self.assertEqual(self.basic_plan.max_users, 8)
        self.assertTrue(self.basic_plan.features['multi_shop'])
    
    def test_list_tenants(self):
        """
        Test listing tenants.
        """
        url = reverse('tenant-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that the response contains the expected tenants
        tenant_names = [tenant['name'] for tenant in response.data['results']]
        self.assertIn('Liquor Shop 1', tenant_names)
        self.assertIn('Liquor Shop 2', tenant_names)
    
    def test_filter_tenants_by_status(self):
        """
        Test filtering tenants by status.
        """
        # Create a suspended tenant
        suspended_tenant = Tenant.objects.create(
            name="Suspended Shop",
            slug="suspended-shop",
            domain="suspendedshop.com",
            status=Tenant.STATUS_SUSPENDED,
            business_name="Suspended Enterprises",
            business_address="789 Pine St, City, State, 12345",
            business_phone="3456789012",
            business_email="contact@suspendedshop.com",
            contact_name="Bob Johnson",
            contact_email="bob@suspendedshop.com",
            contact_phone="7654321098",
            billing_plan=self.standard_plan,
            billing_cycle=Tenant.BILLING_MONTHLY
        )
        
        url = reverse('tenant-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url, {'status': Tenant.STATUS_SUSPENDED})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Suspended Shop')
        self.assertEqual(response.data['results'][0]['status'], Tenant.STATUS_SUSPENDED)
    
    def test_filter_tenants_by_billing_plan(self):
        """
        Test filtering tenants by billing plan.
        """
        url = reverse('tenant-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url, {'billing_plan': self.standard_plan.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Liquor Shop 1')
        self.assertEqual(response.data['results'][0]['billing_plan'], str(self.standard_plan.id))
    
    def test_create_tenant(self):
        """
        Test creating a tenant.
        """
        url = reverse('tenant-list')
        data = {
            'name': 'New Liquor Shop',
            'slug': 'new-liquor-shop',
            'domain': 'newliquorshop.com',
            'status': Tenant.STATUS_ACTIVE,
            'business_name': 'New Liquor Enterprises',
            'business_address': '789 Pine St, City, State, 12345',
            'business_phone': '3456789012',
            'business_email': 'contact@newliquorshop.com',
            'tax_id': 'TAX345678',
            'registration_number': 'REG345678',
            'contact_name': 'Bob Johnson',
            'contact_email': 'bob.johnson@newliquorshop.com',
            'contact_phone': '7654321098',
            'billing_plan': str(self.premium_plan.id),
            'billing_cycle': Tenant.BILLING_MONTHLY,
            'billing_address': '789 Pine St, City, State, 12345',
            'billing_email': 'billing@newliquorshop.com',
            'subscription_start_date': date.today().isoformat(),
            'subscription_end_date': (date.today() + timedelta(days=30)).isoformat(),
            'is_trial': False
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Liquor Shop')
        self.assertEqual(response.data['slug'], 'new-liquor-shop')
        self.assertEqual(response.data['domain'], 'newliquorshop.com')
        self.assertEqual(response.data['status'], Tenant.STATUS_ACTIVE)
        self.assertEqual(response.data['business_name'], 'New Liquor Enterprises')
        self.assertEqual(response.data['billing_plan'], str(self.premium_plan.id))
        self.assertEqual(response.data['billing_cycle'], Tenant.BILLING_MONTHLY)
        
        # Check that the tenant was created in the database
        tenant = Tenant.objects.get(slug='new-liquor-shop')
        self.assertEqual(tenant.name, 'New Liquor Shop')
        self.assertEqual(tenant.business_email, 'contact@newliquorshop.com')
        self.assertEqual(tenant.billing_plan, self.premium_plan)
    
    def test_retrieve_tenant(self):
        """
        Test retrieving a tenant.
        """
        url = reverse('tenant-detail', args=[self.tenant1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Liquor Shop 1')
        self.assertEqual(response.data['slug'], 'liquor-shop-1')
        self.assertEqual(response.data['domain'], 'liquorshop1.com')
        self.assertEqual(response.data['status'], Tenant.STATUS_ACTIVE)
        self.assertEqual(response.data['business_name'], 'Liquor Enterprises 1')
        self.assertEqual(response.data['billing_plan'], str(self.standard_plan.id))
        self.assertEqual(response.data['billing_cycle'], Tenant.BILLING_MONTHLY)
    
    def test_update_tenant(self):
        """
        Test updating a tenant.
        """
        url = reverse('tenant-detail', args=[self.tenant1.id])
        data = {
            'business_phone': '9998887777',
            'business_email': 'updated@liquorshop1.com',
            'billing_cycle': Tenant.BILLING_YEARLY,
            'primary_color': '#FF5733',
            'secondary_color': '#33FF57'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['business_phone'], '9998887777')
        self.assertEqual(response.data['business_email'], 'updated@liquorshop1.com')
        self.assertEqual(response.data['billing_cycle'], Tenant.BILLING_YEARLY)
        self.assertEqual(response.data['primary_color'], '#FF5733')
        self.assertEqual(response.data['secondary_color'], '#33FF57')
        
        # Check that the tenant was updated in the database
        self.tenant1.refresh_from_db()
        self.assertEqual(self.tenant1.business_phone, '9998887777')
        self.assertEqual(self.tenant1.business_email, 'updated@liquorshop1.com')
        self.assertEqual(self.tenant1.billing_cycle, Tenant.BILLING_YEARLY)
        self.assertEqual(self.tenant1.primary_color, '#FF5733')
        self.assertEqual(self.tenant1.secondary_color, '#33FF57')
    
    def test_suspend_tenant(self):
        """
        Test suspending a tenant.
        """
        url = reverse('tenant-suspend', args=[self.tenant1.id])
        data = {
            'notes': 'Suspended due to payment issues'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Tenant.STATUS_SUSPENDED)
        self.assertEqual(response.data['notes'], 'Suspended due to payment issues')
        
        # Check that the tenant was suspended in the database
        self.tenant1.refresh_from_db()
        self.assertEqual(self.tenant1.status, Tenant.STATUS_SUSPENDED)
        self.assertEqual(self.tenant1.notes, 'Suspended due to payment issues')
    
    def test_activate_tenant(self):
        """
        Test activating a suspended tenant.
        """
        # First suspend the tenant
        self.tenant1.status = Tenant.STATUS_SUSPENDED
        self.tenant1.save()
        
        url = reverse('tenant-activate', args=[self.tenant1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Tenant.STATUS_ACTIVE)
        
        # Check that the tenant was activated in the database
        self.tenant1.refresh_from_db()
        self.assertEqual(self.tenant1.status, Tenant.STATUS_ACTIVE)
    
    def test_list_tenant_billing_history(self):
        """
        Test listing tenant billing history.
        """
        url = reverse('tenantbillinghistory-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_number'], 'INV-2023-001')
        self.assertEqual(response.data['results'][0]['amount'], '99.99')
    
    def test_filter_tenant_billing_history_by_tenant(self):
        """
        Test filtering tenant billing history by tenant.
        """
        url = reverse('tenantbillinghistory-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url, {'tenant': self.tenant1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tenant'], str(self.tenant1.id))
    
    def test_create_tenant_billing_history(self):
        """
        Test creating a tenant billing history.
        """
        url = reverse('tenantbillinghistory-list')
        data = {
            'tenant': str(self.tenant2.id),
            'billing_plan': str(self.basic_plan.id),
            'amount': '499.99',
            'status': TenantBillingHistory.STATUS_PAID,
            'invoice_number': 'INV-2023-002',
            'invoice_date': date.today().isoformat(),
            'due_date': (date.today() + timedelta(days=15)).isoformat(),
            'payment_date': date.today().isoformat(),
            'payment_method': 'Bank Transfer',
            'payment_reference': 'TRANSFER123456',
            'billing_period_start': date.today().isoformat(),
            'billing_period_end': (date.today() + timedelta(days=365)).isoformat(),
            'notes': 'Yearly billing'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tenant'], str(self.tenant2.id))
        self.assertEqual(response.data['billing_plan'], str(self.basic_plan.id))
        self.assertEqual(response.data['amount'], '499.99')
        self.assertEqual(response.data['invoice_number'], 'INV-2023-002')
        self.assertEqual(response.data['payment_method'], 'Bank Transfer')
        
        # Check that the billing history was created in the database
        billing_history = TenantBillingHistory.objects.get(invoice_number='INV-2023-002')
        self.assertEqual(billing_history.tenant, self.tenant2)
        self.assertEqual(billing_history.amount, Decimal('499.99'))
        self.assertEqual(billing_history.payment_method, 'Bank Transfer')
    
    def test_retrieve_tenant_billing_history(self):
        """
        Test retrieving a tenant billing history.
        """
        url = reverse('tenantbillinghistory-detail', args=[self.billing_history1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tenant'], str(self.tenant1.id))
        self.assertEqual(response.data['billing_plan'], str(self.standard_plan.id))
        self.assertEqual(response.data['amount'], '99.99')
        self.assertEqual(response.data['invoice_number'], 'INV-2023-001')
        self.assertEqual(response.data['payment_method'], 'Credit Card')
    
    def test_update_tenant_billing_history(self):
        """
        Test updating a tenant billing history.
        """
        url = reverse('tenantbillinghistory-detail', args=[self.billing_history1.id])
        data = {
            'status': TenantBillingHistory.STATUS_REFUNDED,
            'notes': 'Refunded due to service issues'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.saas_admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], TenantBillingHistory.STATUS_REFUNDED)
        self.assertEqual(response.data['notes'], 'Refunded due to service issues')
        
        # Check that the billing history was updated in the database
        self.billing_history1.refresh_from_db()
        self.assertEqual(self.billing_history1.status, TenantBillingHistory.STATUS_REFUNDED)
        self.assertEqual(self.billing_history1.notes, 'Refunded due to service issues')
    
    def test_tenant_admin_cannot_access_other_tenants(self):
        """
        Test that tenant admins cannot access other tenants' data.
        """
        url = reverse('tenant-detail', args=[self.tenant2.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_tenant_admin_can_access_own_tenant(self):
        """
        Test that tenant admins can access their own tenant's data.
        """
        url = reverse('tenant-detail', args=[self.tenant1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Liquor Shop 1')
        self.assertEqual(response.data['slug'], 'liquor-shop-1')
    
    def test_tenant_admin_cannot_create_tenants(self):
        """
        Test that tenant admins cannot create new tenants.
        """
        url = reverse('tenant-list')
        data = {
            'name': 'Unauthorized Tenant',
            'slug': 'unauthorized-tenant',
            'domain': 'unauthorizedtenant.com',
            'status': Tenant.STATUS_ACTIVE,
            'business_name': 'Unauthorized Enterprises',
            'business_address': '999 Elm St, City, State, 12345',
            'business_phone': '5556667777',
            'business_email': 'contact@unauthorizedtenant.com',
            'contact_name': 'Unauthorized User',
            'contact_email': 'user@unauthorizedtenant.com',
            'contact_phone': '7778889999',
            'billing_plan': str(self.basic_plan.id),
            'billing_cycle': Tenant.BILLING_MONTHLY
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)