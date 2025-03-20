import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from tenants.models import BillingPlan, Tenant, TenantBillingHistory, TenantActivity

class TenantModelsTest(TestCase):
    """
    Test the tenant models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.user_id = uuid.uuid4()
        
        # Create billing plan
        self.billing_plan = BillingPlan.objects.create(
            name="Standard Plan",
            description="Standard plan for small businesses",
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
            is_active=True,
            created_by=self.user_id
        )
        
        # Create tenant
        self.tenant = Tenant.objects.create(
            name="Test Liquor Shop",
            slug="test-liquor-shop",
            domain="testliquorshop.com",
            status=Tenant.STATUS_ACTIVE,
            business_name="Test Liquor Enterprises",
            business_address="123 Main St, City, State, 12345",
            business_phone="1234567890",
            business_email="contact@testliquorshop.com",
            tax_id="TAX123456",
            registration_number="REG123456",
            contact_name="John Doe",
            contact_email="john.doe@testliquorshop.com",
            contact_phone="9876543210",
            billing_plan=self.billing_plan,
            billing_cycle=Tenant.BILLING_MONTHLY,
            billing_address="123 Main St, City, State, 12345",
            billing_email="billing@testliquorshop.com",
            subscription_start_date=date.today(),
            subscription_end_date=date.today() + timedelta(days=30),
            is_trial=False,
            primary_color="#FF5733",
            secondary_color="#33FF57",
            created_by=self.user_id,
            notes="Test tenant for liquor shop"
        )
        
        # Create tenant billing history
        self.billing_history = TenantBillingHistory.objects.create(
            tenant=self.tenant,
            billing_plan=self.billing_plan,
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
            notes="Monthly billing",
            created_by=self.user_id
        )
        
        # Create tenant activity
        self.tenant_activity = TenantActivity.objects.create(
            tenant=self.tenant,
            user_id=self.user_id,
            activity_type="login",
            description="User logged in",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            metadata={
                'browser': 'Chrome',
                'device': 'Desktop'
            },
            created_by=self.user_id
        )
    
    def test_billing_plan_creation(self):
        """
        Test BillingPlan creation.
        """
        self.assertEqual(self.billing_plan.name, "Standard Plan")
        self.assertEqual(self.billing_plan.description, "Standard plan for small businesses")
        self.assertEqual(self.billing_plan.price_monthly, Decimal('99.99'))
        self.assertEqual(self.billing_plan.price_yearly, Decimal('999.99'))
        self.assertEqual(self.billing_plan.max_shops, 3)
        self.assertEqual(self.billing_plan.max_users, 10)
        self.assertTrue(self.billing_plan.features['inventory_management'])
        self.assertTrue(self.billing_plan.features['sales_analytics'])
        self.assertTrue(self.billing_plan.features['multi_shop'])
        self.assertFalse(self.billing_plan.features['advanced_reporting'])
        self.assertTrue(self.billing_plan.is_active)
        self.assertEqual(self.billing_plan.created_by, self.user_id)
    
    def test_billing_plan_str(self):
        """
        Test BillingPlan string representation.
        """
        self.assertEqual(str(self.billing_plan), "Standard Plan")
    
    def test_tenant_creation(self):
        """
        Test Tenant creation.
        """
        self.assertEqual(self.tenant.name, "Test Liquor Shop")
        self.assertEqual(self.tenant.slug, "test-liquor-shop")
        self.assertEqual(self.tenant.domain, "testliquorshop.com")
        self.assertEqual(self.tenant.status, Tenant.STATUS_ACTIVE)
        self.assertEqual(self.tenant.business_name, "Test Liquor Enterprises")
        self.assertEqual(self.tenant.business_address, "123 Main St, City, State, 12345")
        self.assertEqual(self.tenant.business_phone, "1234567890")
        self.assertEqual(self.tenant.business_email, "contact@testliquorshop.com")
        self.assertEqual(self.tenant.tax_id, "TAX123456")
        self.assertEqual(self.tenant.registration_number, "REG123456")
        self.assertEqual(self.tenant.contact_name, "John Doe")
        self.assertEqual(self.tenant.contact_email, "john.doe@testliquorshop.com")
        self.assertEqual(self.tenant.contact_phone, "9876543210")
        self.assertEqual(self.tenant.billing_plan, self.billing_plan)
        self.assertEqual(self.tenant.billing_cycle, Tenant.BILLING_MONTHLY)
        self.assertEqual(self.tenant.billing_address, "123 Main St, City, State, 12345")
        self.assertEqual(self.tenant.billing_email, "billing@testliquorshop.com")
        self.assertEqual(self.tenant.subscription_start_date, date.today())
        self.assertEqual(self.tenant.subscription_end_date, date.today() + timedelta(days=30))
        self.assertFalse(self.tenant.is_trial)
        self.assertIsNone(self.tenant.trial_end_date)
        self.assertEqual(self.tenant.primary_color, "#FF5733")
        self.assertEqual(self.tenant.secondary_color, "#33FF57")
        self.assertEqual(self.tenant.created_by, self.user_id)
        self.assertEqual(self.tenant.notes, "Test tenant for liquor shop")
    
    def test_tenant_str(self):
        """
        Test Tenant string representation.
        """
        self.assertEqual(str(self.tenant), "Test Liquor Shop")
    
    def test_tenant_billing_history_creation(self):
        """
        Test TenantBillingHistory creation.
        """
        self.assertEqual(self.billing_history.tenant, self.tenant)
        self.assertEqual(self.billing_history.billing_plan, self.billing_plan)
        self.assertEqual(self.billing_history.amount, Decimal('99.99'))
        self.assertEqual(self.billing_history.status, TenantBillingHistory.STATUS_PAID)
        self.assertEqual(self.billing_history.invoice_number, "INV-2023-001")
        self.assertEqual(self.billing_history.invoice_date, date.today())
        self.assertEqual(self.billing_history.due_date, date.today() + timedelta(days=15))
        self.assertEqual(self.billing_history.payment_date, date.today())
        self.assertEqual(self.billing_history.payment_method, "Credit Card")
        self.assertEqual(self.billing_history.payment_reference, "PAYMENT123456")
        self.assertEqual(self.billing_history.billing_period_start, date.today())
        self.assertEqual(self.billing_history.billing_period_end, date.today() + timedelta(days=30))
        self.assertEqual(self.billing_history.notes, "Monthly billing")
        self.assertEqual(self.billing_history.created_by, self.user_id)
    
    def test_tenant_billing_history_str(self):
        """
        Test TenantBillingHistory string representation.
        """
        expected_str = "Test Liquor Shop - INV-2023-001"
        self.assertEqual(str(self.billing_history), expected_str)
    
    def test_tenant_activity_creation(self):
        """
        Test TenantActivity creation.
        """
        self.assertEqual(self.tenant_activity.tenant, self.tenant)
        self.assertEqual(self.tenant_activity.user_id, self.user_id)
        self.assertEqual(self.tenant_activity.activity_type, "login")
        self.assertEqual(self.tenant_activity.description, "User logged in")
        self.assertEqual(self.tenant_activity.ip_address, "192.168.1.1")
        self.assertEqual(self.tenant_activity.user_agent, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        self.assertEqual(self.tenant_activity.metadata['browser'], "Chrome")
        self.assertEqual(self.tenant_activity.metadata['device'], "Desktop")
        self.assertEqual(self.tenant_activity.created_by, self.user_id)
    
    def test_tenant_activity_str(self):
        """
        Test TenantActivity string representation.
        """
        expected_str = f"Test Liquor Shop - login - {self.tenant_activity.created_at}"
        self.assertEqual(str(self.tenant_activity), expected_str)