import uuid
from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.db import IntegrityError
from core_service.tenants.models import Tenant, TenantSettings

class TenantModelsTest(TestCase):
    """
    Test the tenant models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.admin_id = uuid.uuid4()
        
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
    
    def test_tenant_creation(self):
        """
        Test Tenant creation.
        """
        self.assertEqual(self.tenant.name, "Liquor Enterprises")
        self.assertEqual(self.tenant.slug, "liquor-enterprises")
        self.assertEqual(self.tenant.address, "456 Business Avenue")
        self.assertEqual(self.tenant.city, "New York")
        self.assertEqual(self.tenant.state, "NY")
        self.assertEqual(self.tenant.country, "USA")
        self.assertEqual(self.tenant.postal_code, "10001")
        self.assertEqual(self.tenant.phone, "212-555-1234")
        self.assertEqual(self.tenant.email, "info@liquorenterprises.com")
        self.assertEqual(self.tenant.website, "https://www.liquorenterprises.com")
        self.assertEqual(self.tenant.business_type, "Retail")
        self.assertEqual(self.tenant.tax_id, "TAX-987654321")
        self.assertEqual(self.tenant.license_number, "LIQ-2023-12345")
        self.assertEqual(self.tenant.license_expiry, date(2024, 12, 31))
        self.assertEqual(self.tenant.subscription_plan, "premium")
        self.assertEqual(self.tenant.subscription_start_date, date(2023, 1, 1))
        self.assertEqual(self.tenant.subscription_end_date, date(2023, 12, 31))
        self.assertEqual(self.tenant.max_shops, 10)
        self.assertEqual(self.tenant.max_users, 50)
        self.assertEqual(self.tenant.contact_person_name, "John Smith")
        self.assertEqual(self.tenant.contact_person_email, "john.smith@liquorenterprises.com")
        self.assertEqual(self.tenant.contact_person_phone, "212-555-5678")
        self.assertEqual(self.tenant.primary_color, "#4a6da7")
        self.assertEqual(self.tenant.secondary_color, "#ffffff")
        self.assertEqual(self.tenant.created_by, self.admin_id)
    
    def test_tenant_str(self):
        """
        Test Tenant string representation.
        """
        self.assertEqual(str(self.tenant), "Liquor Enterprises")
    
    def test_tenant_unique_slug(self):
        """
        Test that tenant slug must be unique.
        """
        # Try to create another tenant with the same slug
        with self.assertRaises(IntegrityError):
            Tenant.objects.create(
                name="Another Liquor Enterprise",
                slug="liquor-enterprises",  # Same slug as existing tenant
                created_by=self.admin_id
            )
    
    def test_tenant_settings_creation(self):
        """
        Test TenantSettings creation.
        """
        self.assertEqual(self.tenant_settings.tenant, self.tenant)
        self.assertEqual(self.tenant_settings.timezone, "America/New_York")
        self.assertEqual(self.tenant_settings.date_format, "MM/DD/YYYY")
        self.assertEqual(self.tenant_settings.time_format, "hh:mm A")
        self.assertEqual(self.tenant_settings.currency, "USD")
        self.assertEqual(self.tenant_settings.language, "en-US")
        self.assertEqual(self.tenant_settings.fiscal_year_start, "01-01")
        self.assertEqual(self.tenant_settings.tax_rate, Decimal('8.875'))
        self.assertTrue(self.tenant_settings.enable_tax)
        self.assertTrue(self.tenant_settings.require_2fa)
        self.assertEqual(self.tenant_settings.password_expiry_days, 60)
        self.assertEqual(self.tenant_settings.session_timeout_minutes, 15)
        self.assertTrue(self.tenant_settings.enable_email_notifications)
        self.assertTrue(self.tenant_settings.enable_sms_notifications)
        self.assertTrue(self.tenant_settings.require_sales_approval)
        self.assertTrue(self.tenant_settings.require_purchase_approval)
        self.assertTrue(self.tenant_settings.require_expense_approval)
        self.assertTrue(self.tenant_settings.enable_inventory_management)
        self.assertTrue(self.tenant_settings.enable_financial_management)
        self.assertTrue(self.tenant_settings.enable_reports)
        self.assertTrue(self.tenant_settings.enable_analytics)
        self.assertEqual(self.tenant_settings.created_by, self.admin_id)
    
    def test_tenant_settings_str(self):
        """
        Test TenantSettings string representation.
        """
        expected_str = "Liquor Enterprises Settings"
        self.assertEqual(str(self.tenant_settings), expected_str)
    
    def test_tenant_settings_one_to_one_relationship(self):
        """
        Test that a tenant can only have one settings object.
        """
        # Try to create another settings object for the same tenant
        with self.assertRaises(IntegrityError):
            TenantSettings.objects.create(
                tenant=self.tenant,
                created_by=self.admin_id
            )
    
    def test_tenant_relationships(self):
        """
        Test relationships between Tenant and TenantSettings.
        """
        # Test settings relationship
        self.assertEqual(self.tenant.settings, self.tenant_settings)
    
    def test_update_tenant(self):
        """
        Test updating a tenant.
        """
        # Update tenant
        self.tenant.name = "Updated Liquor Enterprises"
        self.tenant.address = "789 Updated Avenue"
        self.tenant.subscription_plan = "enterprise"
        self.tenant.max_shops = 20
        self.tenant.max_users = 100
        self.tenant.save()
        
        # Refresh from database
        self.tenant.refresh_from_db()
        
        # Check that the tenant was updated
        self.assertEqual(self.tenant.name, "Updated Liquor Enterprises")
        self.assertEqual(self.tenant.address, "789 Updated Avenue")
        self.assertEqual(self.tenant.subscription_plan, "enterprise")
        self.assertEqual(self.tenant.max_shops, 20)
        self.assertEqual(self.tenant.max_users, 100)
    
    def test_update_tenant_settings(self):
        """
        Test updating tenant settings.
        """
        # Update tenant settings
        self.tenant_settings.timezone = "America/Los_Angeles"
        self.tenant_settings.tax_rate = Decimal('9.5')
        self.tenant_settings.require_2fa = False
        self.tenant_settings.password_expiry_days = 90
        self.tenant_settings.save()
        
        # Refresh from database
        self.tenant_settings.refresh_from_db()
        
        # Check that the settings were updated
        self.assertEqual(self.tenant_settings.timezone, "America/Los_Angeles")
        self.assertEqual(self.tenant_settings.tax_rate, Decimal('9.5'))
        self.assertFalse(self.tenant_settings.require_2fa)
        self.assertEqual(self.tenant_settings.password_expiry_days, 90)
    
    def test_create_tenant_with_minimal_fields(self):
        """
        Test creating a tenant with only required fields.
        """
        minimal_tenant = Tenant.objects.create(
            name="Minimal Tenant",
            slug="minimal-tenant",
            created_by=self.admin_id
        )
        
        self.assertEqual(minimal_tenant.name, "Minimal Tenant")
        self.assertEqual(minimal_tenant.slug, "minimal-tenant")
        self.assertEqual(minimal_tenant.subscription_plan, "basic")  # Default value
        self.assertEqual(minimal_tenant.max_shops, 1)  # Default value
        self.assertEqual(minimal_tenant.max_users, 5)  # Default value
        self.assertEqual(minimal_tenant.primary_color, "#4a6da7")  # Default value
        self.assertEqual(minimal_tenant.secondary_color, "#ffffff")  # Default value
        self.assertEqual(minimal_tenant.created_by, self.admin_id)
    
    def test_create_tenant_settings_with_minimal_fields(self):
        """
        Test creating tenant settings with only required fields.
        """
        minimal_tenant = Tenant.objects.create(
            name="Another Minimal Tenant",
            slug="another-minimal-tenant",
            created_by=self.admin_id
        )
        
        minimal_settings = TenantSettings.objects.create(
            tenant=minimal_tenant,
            created_by=self.admin_id
        )
        
        self.assertEqual(minimal_settings.tenant, minimal_tenant)
        self.assertEqual(minimal_settings.timezone, "UTC")  # Default value
        self.assertEqual(minimal_settings.date_format, "YYYY-MM-DD")  # Default value
        self.assertEqual(minimal_settings.time_format, "HH:mm:ss")  # Default value
        self.assertEqual(minimal_settings.currency, "USD")  # Default value
        self.assertEqual(minimal_settings.language, "en-US")  # Default value
        self.assertEqual(minimal_settings.fiscal_year_start, "01-01")  # Default value
        self.assertEqual(minimal_settings.tax_rate, Decimal('0'))  # Default value
        self.assertTrue(minimal_settings.enable_tax)  # Default value
        self.assertFalse(minimal_settings.require_2fa)  # Default value
        self.assertEqual(minimal_settings.password_expiry_days, 90)  # Default value
        self.assertEqual(minimal_settings.session_timeout_minutes, 30)  # Default value
        self.assertTrue(minimal_settings.enable_email_notifications)  # Default value
        self.assertFalse(minimal_settings.enable_sms_notifications)  # Default value
        self.assertTrue(minimal_settings.require_sales_approval)  # Default value
        self.assertTrue(minimal_settings.require_purchase_approval)  # Default value
        self.assertTrue(minimal_settings.require_expense_approval)  # Default value
        self.assertTrue(minimal_settings.enable_inventory_management)  # Default value
        self.assertTrue(minimal_settings.enable_financial_management)  # Default value
        self.assertTrue(minimal_settings.enable_reports)  # Default value
        self.assertTrue(minimal_settings.enable_analytics)  # Default value
        self.assertEqual(minimal_settings.created_by, self.admin_id)