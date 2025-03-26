import uuid
from django.test import TestCase
from django.db import IntegrityError
from core_service.settings.models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate

class SettingsModelsTest(TestCase):
    """
    Test the settings models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.admin_id = uuid.uuid4()
        self.tenant_id = uuid.uuid4()
        
        # Create system setting
        self.system_setting = SystemSetting.objects.create(
            key="SYSTEM_NAME",
            value="Liquor Management System",
            description="The name of the system",
            is_public=True,
            created_by=self.admin_id
        )
        
        # Create tenant setting
        self.tenant_setting = TenantSetting.objects.create(
            tenant_id=self.tenant_id,
            key="DEFAULT_TAX_RATE",
            value="18.0",
            description="Default tax rate for the tenant",
            created_by=self.admin_id
        )
        
        # Create email template
        self.email_template = EmailTemplate.objects.create(
            tenant_id=self.tenant_id,
            name="WELCOME_EMAIL",
            subject="Welcome to Liquor Management System",
            body="Dear {{name}},\n\nWelcome to the Liquor Management System.\n\nRegards,\nThe Team",
            description="Email sent to new users",
            created_by=self.admin_id
        )
        
        # Create notification template
        self.notification_template = NotificationTemplate.objects.create(
            tenant_id=self.tenant_id,
            name="LOW_STOCK_ALERT",
            title="Low Stock Alert",
            body="Product {{product_name}} is running low on stock. Current stock: {{current_stock}}",
            description="Notification sent when product stock is low",
            created_by=self.admin_id
        )
    
    def test_system_setting_creation(self):
        """
        Test SystemSetting creation.
        """
        self.assertEqual(self.system_setting.key, "SYSTEM_NAME")
        self.assertEqual(self.system_setting.value, "Liquor Management System")
        self.assertEqual(self.system_setting.description, "The name of the system")
        self.assertTrue(self.system_setting.is_public)
        self.assertEqual(self.system_setting.created_by, self.admin_id)
    
    def test_system_setting_str(self):
        """
        Test SystemSetting string representation.
        """
        self.assertEqual(str(self.system_setting), "SYSTEM_NAME")
    
    def test_system_setting_unique_key(self):
        """
        Test that system setting key must be unique.
        """
        # Try to create another system setting with the same key
        with self.assertRaises(IntegrityError):
            SystemSetting.objects.create(
                key="SYSTEM_NAME",  # Same key as existing setting
                value="Another System Name",
                created_by=self.admin_id
            )
    
    def test_tenant_setting_creation(self):
        """
        Test TenantSetting creation.
        """
        self.assertEqual(self.tenant_setting.tenant_id, self.tenant_id)
        self.assertEqual(self.tenant_setting.key, "DEFAULT_TAX_RATE")
        self.assertEqual(self.tenant_setting.value, "18.0")
        self.assertEqual(self.tenant_setting.description, "Default tax rate for the tenant")
        self.assertEqual(self.tenant_setting.created_by, self.admin_id)
    
    def test_tenant_setting_str(self):
        """
        Test TenantSetting string representation.
        """
        expected_str = f"{self.tenant_id} - DEFAULT_TAX_RATE"
        self.assertEqual(str(self.tenant_setting), expected_str)
    
    def test_tenant_setting_unique_key_per_tenant(self):
        """
        Test that tenant setting key must be unique per tenant.
        """
        # Try to create another tenant setting with the same key for the same tenant
        with self.assertRaises(IntegrityError):
            TenantSetting.objects.create(
                tenant_id=self.tenant_id,
                key="DEFAULT_TAX_RATE",  # Same key as existing setting
                value="20.0",
                created_by=self.admin_id
            )
        
        # Create a tenant setting with the same key but for a different tenant (should work)
        another_tenant_id = uuid.uuid4()
        another_tenant_setting = TenantSetting.objects.create(
            tenant_id=another_tenant_id,
            key="DEFAULT_TAX_RATE",  # Same key but different tenant
            value="20.0",
            created_by=self.admin_id
        )
        self.assertEqual(another_tenant_setting.key, "DEFAULT_TAX_RATE")
        self.assertEqual(another_tenant_setting.tenant_id, another_tenant_id)
    
    def test_email_template_creation(self):
        """
        Test EmailTemplate creation.
        """
        self.assertEqual(self.email_template.tenant_id, self.tenant_id)
        self.assertEqual(self.email_template.name, "WELCOME_EMAIL")
        self.assertEqual(self.email_template.subject, "Welcome to Liquor Management System")
        self.assertEqual(self.email_template.body, "Dear {{name}},\n\nWelcome to the Liquor Management System.\n\nRegards,\nThe Team")
        self.assertEqual(self.email_template.description, "Email sent to new users")
        self.assertEqual(self.email_template.created_by, self.admin_id)
    
    def test_email_template_str(self):
        """
        Test EmailTemplate string representation.
        """
        expected_str = f"{self.tenant_id} - WELCOME_EMAIL"
        self.assertEqual(str(self.email_template), expected_str)
    
    def test_email_template_unique_name_per_tenant(self):
        """
        Test that email template name must be unique per tenant.
        """
        # Try to create another email template with the same name for the same tenant
        with self.assertRaises(IntegrityError):
            EmailTemplate.objects.create(
                tenant_id=self.tenant_id,
                name="WELCOME_EMAIL",  # Same name as existing template
                subject="Another Welcome Email",
                body="Another welcome email body",
                created_by=self.admin_id
            )
        
        # Create an email template with the same name but for a different tenant (should work)
        another_tenant_id = uuid.uuid4()
        another_email_template = EmailTemplate.objects.create(
            tenant_id=another_tenant_id,
            name="WELCOME_EMAIL",  # Same name but different tenant
            subject="Another Welcome Email",
            body="Another welcome email body",
            created_by=self.admin_id
        )
        self.assertEqual(another_email_template.name, "WELCOME_EMAIL")
        self.assertEqual(another_email_template.tenant_id, another_tenant_id)
    
    def test_notification_template_creation(self):
        """
        Test NotificationTemplate creation.
        """
        self.assertEqual(self.notification_template.tenant_id, self.tenant_id)
        self.assertEqual(self.notification_template.name, "LOW_STOCK_ALERT")
        self.assertEqual(self.notification_template.title, "Low Stock Alert")
        self.assertEqual(self.notification_template.body, "Product {{product_name}} is running low on stock. Current stock: {{current_stock}}")
        self.assertEqual(self.notification_template.description, "Notification sent when product stock is low")
        self.assertEqual(self.notification_template.created_by, self.admin_id)
    
    def test_notification_template_str(self):
        """
        Test NotificationTemplate string representation.
        """
        expected_str = f"{self.tenant_id} - LOW_STOCK_ALERT"
        self.assertEqual(str(self.notification_template), expected_str)
    
    def test_notification_template_unique_name_per_tenant(self):
        """
        Test that notification template name must be unique per tenant.
        """
        # Try to create another notification template with the same name for the same tenant
        with self.assertRaises(IntegrityError):
            NotificationTemplate.objects.create(
                tenant_id=self.tenant_id,
                name="LOW_STOCK_ALERT",  # Same name as existing template
                title="Another Low Stock Alert",
                body="Another low stock alert body",
                created_by=self.admin_id
            )
        
        # Create a notification template with the same name but for a different tenant (should work)
        another_tenant_id = uuid.uuid4()
        another_notification_template = NotificationTemplate.objects.create(
            tenant_id=another_tenant_id,
            name="LOW_STOCK_ALERT",  # Same name but different tenant
            title="Another Low Stock Alert",
            body="Another low stock alert body",
            created_by=self.admin_id
        )
        self.assertEqual(another_notification_template.name, "LOW_STOCK_ALERT")
        self.assertEqual(another_notification_template.tenant_id, another_tenant_id)
    
    def test_update_system_setting(self):
        """
        Test updating a system setting.
        """
        # Update system setting
        self.system_setting.value = "Updated Liquor Management System"
        self.system_setting.is_public = False
        self.system_setting.save()
        
        # Refresh from database
        self.system_setting.refresh_from_db()
        
        # Check that the system setting was updated
        self.assertEqual(self.system_setting.value, "Updated Liquor Management System")
        self.assertFalse(self.system_setting.is_public)
    
    def test_update_tenant_setting(self):
        """
        Test updating a tenant setting.
        """
        # Update tenant setting
        self.tenant_setting.value = "20.0"
        self.tenant_setting.description = "Updated description"
        self.tenant_setting.save()
        
        # Refresh from database
        self.tenant_setting.refresh_from_db()
        
        # Check that the tenant setting was updated
        self.assertEqual(self.tenant_setting.value, "20.0")
        self.assertEqual(self.tenant_setting.description, "Updated description")
    
    def test_update_email_template(self):
        """
        Test updating an email template.
        """
        # Update email template
        self.email_template.subject = "Updated Welcome Email Subject"
        self.email_template.body = "Updated welcome email body"
        self.email_template.save()
        
        # Refresh from database
        self.email_template.refresh_from_db()
        
        # Check that the email template was updated
        self.assertEqual(self.email_template.subject, "Updated Welcome Email Subject")
        self.assertEqual(self.email_template.body, "Updated welcome email body")
    
    def test_update_notification_template(self):
        """
        Test updating a notification template.
        """
        # Update notification template
        self.notification_template.title = "Updated Low Stock Alert"
        self.notification_template.body = "Updated low stock alert body"
        self.notification_template.save()
        
        # Refresh from database
        self.notification_template.refresh_from_db()
        
        # Check that the notification template was updated
        self.assertEqual(self.notification_template.title, "Updated Low Stock Alert")
        self.assertEqual(self.notification_template.body, "Updated low stock alert body")