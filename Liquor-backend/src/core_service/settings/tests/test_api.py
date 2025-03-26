import uuid
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from common.jwt_auth import MicroserviceUser
from core_service.settings.models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate

class SettingsAPITest(TestCase):
    """
    Test the settings API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test users
        self.admin_id = uuid.uuid4()
        self.tenant_id = uuid.uuid4()
        
        self.admin_user = MicroserviceUser({
            'id': str(self.admin_id),
            'email': 'admin@example.com',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
            'role': 'system_admin',
            'permissions': ['view_systemsetting', 'add_systemsetting', 'change_systemsetting', 'delete_systemsetting']
        })
        
        self.tenant_user = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'tenant@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_tenantsetting', 'add_tenantsetting', 'change_tenantsetting', 'delete_tenantsetting',
                           'view_emailtemplate', 'add_emailtemplate', 'change_emailtemplate', 'delete_emailtemplate',
                           'view_notificationtemplate', 'add_notificationtemplate', 'change_notificationtemplate', 'delete_notificationtemplate']
        })
        
        # Create system settings
        self.system_setting = SystemSetting.objects.create(
            key="SYSTEM_NAME",
            value="Liquor Management System",
            description="The name of the system",
            is_public=True,
            created_by=self.admin_id
        )
        
        self.private_system_setting = SystemSetting.objects.create(
            key="API_SECRET_KEY",
            value="secret-key-value",
            description="API secret key",
            is_public=False,
            created_by=self.admin_id
        )
        
        # Create tenant settings
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
    
    def test_list_system_settings_as_admin(self):
        """
        Test listing system settings as admin.
        """
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('system-settings-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['key'], "API_SECRET_KEY")
        self.assertEqual(response.data['results'][1]['key'], "SYSTEM_NAME")
    
    def test_list_system_settings_as_tenant_user(self):
        """
        Test listing system settings as tenant user (should only see public settings).
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('system-settings-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['key'], "SYSTEM_NAME")
        self.assertEqual(response.data['results'][0]['value'], "Liquor Management System")
    
    def test_retrieve_system_setting_as_admin(self):
        """
        Test retrieving a system setting as admin.
        """
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('system-settings-detail', args=[self.system_setting.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], "SYSTEM_NAME")
        self.assertEqual(response.data['value'], "Liquor Management System")
        self.assertEqual(response.data['description'], "The name of the system")
        self.assertTrue(response.data['is_public'])
    
    def test_retrieve_private_system_setting_as_tenant_user(self):
        """
        Test retrieving a private system setting as tenant user (should fail).
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('system-settings-detail', args=[self.private_system_setting.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_system_setting_as_admin(self):
        """
        Test creating a system setting as admin.
        """
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('system-settings-list')
        data = {
            'key': "NEW_SYSTEM_SETTING",
            'value': "New Value",
            'description': "New system setting",
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['key'], "NEW_SYSTEM_SETTING")
        self.assertEqual(response.data['value'], "New Value")
        self.assertEqual(response.data['description'], "New system setting")
        self.assertTrue(response.data['is_public'])
        
        # Check that the system setting was created in the database
        setting = SystemSetting.objects.get(key="NEW_SYSTEM_SETTING")
        self.assertEqual(setting.value, "New Value")
        self.assertEqual(setting.created_by, self.admin_id)
    
    def test_create_system_setting_as_tenant_user(self):
        """
        Test creating a system setting as tenant user (should fail).
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('system-settings-list')
        data = {
            'key': "NEW_SYSTEM_SETTING",
            'value': "New Value",
            'description': "New system setting",
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_system_setting_as_admin(self):
        """
        Test updating a system setting as admin.
        """
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('system-settings-detail', args=[self.system_setting.id])
        data = {
            'value': "Updated Liquor Management System",
            'description': "Updated description"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], "Updated Liquor Management System")
        self.assertEqual(response.data['description'], "Updated description")
        
        # Check that the system setting was updated in the database
        self.system_setting.refresh_from_db()
        self.assertEqual(self.system_setting.value, "Updated Liquor Management System")
        self.assertEqual(self.system_setting.description, "Updated description")
    
    def test_delete_system_setting_as_admin(self):
        """
        Test deleting a system setting as admin.
        """
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('system-settings-detail', args=[self.system_setting.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the system setting was deleted from the database
        with self.assertRaises(SystemSetting.DoesNotExist):
            SystemSetting.objects.get(id=self.system_setting.id)
    
    def test_list_tenant_settings(self):
        """
        Test listing tenant settings.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('tenant-settings-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['key'], "DEFAULT_TAX_RATE")
        self.assertEqual(response.data['results'][0]['value'], "18.0")
    
    def test_retrieve_tenant_setting(self):
        """
        Test retrieving a tenant setting.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('tenant-settings-detail', args=[self.tenant_setting.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['key'], "DEFAULT_TAX_RATE")
        self.assertEqual(response.data['value'], "18.0")
        self.assertEqual(response.data['description'], "Default tax rate for the tenant")
    
    def test_create_tenant_setting(self):
        """
        Test creating a tenant setting.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('tenant-settings-list')
        data = {
            'key': "NEW_TENANT_SETTING",
            'value': "New Value",
            'description': "New tenant setting"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['key'], "NEW_TENANT_SETTING")
        self.assertEqual(response.data['value'], "New Value")
        self.assertEqual(response.data['description'], "New tenant setting")
        
        # Check that the tenant setting was created in the database
        setting = TenantSetting.objects.get(tenant_id=self.tenant_id, key="NEW_TENANT_SETTING")
        self.assertEqual(setting.value, "New Value")
        self.assertEqual(str(setting.tenant_id), str(self.tenant_id))
    
    def test_update_tenant_setting(self):
        """
        Test updating a tenant setting.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('tenant-settings-detail', args=[self.tenant_setting.id])
        data = {
            'value': "20.0",
            'description': "Updated description"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], "20.0")
        self.assertEqual(response.data['description'], "Updated description")
        
        # Check that the tenant setting was updated in the database
        self.tenant_setting.refresh_from_db()
        self.assertEqual(self.tenant_setting.value, "20.0")
        self.assertEqual(self.tenant_setting.description, "Updated description")
    
    def test_delete_tenant_setting(self):
        """
        Test deleting a tenant setting.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('tenant-settings-detail', args=[self.tenant_setting.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the tenant setting was deleted from the database
        with self.assertRaises(TenantSetting.DoesNotExist):
            TenantSetting.objects.get(id=self.tenant_setting.id)
    
    def test_list_email_templates(self):
        """
        Test listing email templates.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('email-templates-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "WELCOME_EMAIL")
        self.assertEqual(response.data['results'][0]['subject'], "Welcome to Liquor Management System")
    
    def test_retrieve_email_template(self):
        """
        Test retrieving an email template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('email-templates-detail', args=[self.email_template.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "WELCOME_EMAIL")
        self.assertEqual(response.data['subject'], "Welcome to Liquor Management System")
        self.assertEqual(response.data['body'], "Dear {{name}},\n\nWelcome to the Liquor Management System.\n\nRegards,\nThe Team")
        self.assertEqual(response.data['description'], "Email sent to new users")
    
    def test_create_email_template(self):
        """
        Test creating an email template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('email-templates-list')
        data = {
            'name': "ORDER_CONFIRMATION",
            'subject': "Order Confirmation",
            'body': "Dear {{name}},\n\nYour order #{{order_number}} has been confirmed.\n\nRegards,\nThe Team",
            'description': "Email sent when an order is confirmed"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "ORDER_CONFIRMATION")
        self.assertEqual(response.data['subject'], "Order Confirmation")
        self.assertEqual(response.data['body'], "Dear {{name}},\n\nYour order #{{order_number}} has been confirmed.\n\nRegards,\nThe Team")
        self.assertEqual(response.data['description'], "Email sent when an order is confirmed")
        
        # Check that the email template was created in the database
        template = EmailTemplate.objects.get(tenant_id=self.tenant_id, name="ORDER_CONFIRMATION")
        self.assertEqual(template.subject, "Order Confirmation")
        self.assertEqual(str(template.tenant_id), str(self.tenant_id))
    
    def test_update_email_template(self):
        """
        Test updating an email template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('email-templates-detail', args=[self.email_template.id])
        data = {
            'subject': "Updated Welcome Email Subject",
            'body': "Updated welcome email body"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], "Updated Welcome Email Subject")
        self.assertEqual(response.data['body'], "Updated welcome email body")
        
        # Check that the email template was updated in the database
        self.email_template.refresh_from_db()
        self.assertEqual(self.email_template.subject, "Updated Welcome Email Subject")
        self.assertEqual(self.email_template.body, "Updated welcome email body")
    
    def test_delete_email_template(self):
        """
        Test deleting an email template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('email-templates-detail', args=[self.email_template.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the email template was deleted from the database
        with self.assertRaises(EmailTemplate.DoesNotExist):
            EmailTemplate.objects.get(id=self.email_template.id)
    
    def test_list_notification_templates(self):
        """
        Test listing notification templates.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('notification-templates-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "LOW_STOCK_ALERT")
        self.assertEqual(response.data['results'][0]['title'], "Low Stock Alert")
    
    def test_retrieve_notification_template(self):
        """
        Test retrieving a notification template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('notification-templates-detail', args=[self.notification_template.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "LOW_STOCK_ALERT")
        self.assertEqual(response.data['title'], "Low Stock Alert")
        self.assertEqual(response.data['body'], "Product {{product_name}} is running low on stock. Current stock: {{current_stock}}")
        self.assertEqual(response.data['description'], "Notification sent when product stock is low")
    
    def test_create_notification_template(self):
        """
        Test creating a notification template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('notification-templates-list')
        data = {
            'name': "ORDER_RECEIVED",
            'title': "New Order Received",
            'body': "A new order #{{order_number}} has been received from {{customer_name}}.",
            'description': "Notification sent when a new order is received"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "ORDER_RECEIVED")
        self.assertEqual(response.data['title'], "New Order Received")
        self.assertEqual(response.data['body'], "A new order #{{order_number}} has been received from {{customer_name}}.")
        self.assertEqual(response.data['description'], "Notification sent when a new order is received")
        
        # Check that the notification template was created in the database
        template = NotificationTemplate.objects.get(tenant_id=self.tenant_id, name="ORDER_RECEIVED")
        self.assertEqual(template.title, "New Order Received")
        self.assertEqual(str(template.tenant_id), str(self.tenant_id))
    
    def test_update_notification_template(self):
        """
        Test updating a notification template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('notification-templates-detail', args=[self.notification_template.id])
        data = {
            'title': "Updated Low Stock Alert",
            'body': "Updated low stock alert body"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Low Stock Alert")
        self.assertEqual(response.data['body'], "Updated low stock alert body")
        
        # Check that the notification template was updated in the database
        self.notification_template.refresh_from_db()
        self.assertEqual(self.notification_template.title, "Updated Low Stock Alert")
        self.assertEqual(self.notification_template.body, "Updated low stock alert body")
    
    def test_delete_notification_template(self):
        """
        Test deleting a notification template.
        """
        # Authenticate as tenant user
        self.client.force_authenticate(user=self.tenant_user)
        
        url = reverse('notification-templates-detail', args=[self.notification_template.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the notification template was deleted from the database
        with self.assertRaises(NotificationTemplate.DoesNotExist):
            NotificationTemplate.objects.get(id=self.notification_template.id)
    
    def test_tenant_isolation(self):
        """
        Test that tenants can only access their own settings and templates.
        """
        # Create another tenant
        another_tenant_id = uuid.uuid4()
        
        # Create settings and templates for the other tenant
        another_tenant_setting = TenantSetting.objects.create(
            tenant_id=another_tenant_id,
            key="DEFAULT_TAX_RATE",
            value="20.0",
            created_by=self.admin_id
        )
        
        another_email_template = EmailTemplate.objects.create(
            tenant_id=another_tenant_id,
            name="WELCOME_EMAIL",
            subject="Welcome Email for Another Tenant",
            body="Welcome email body for another tenant",
            created_by=self.admin_id
        )
        
        another_notification_template = NotificationTemplate.objects.create(
            tenant_id=another_tenant_id,
            name="LOW_STOCK_ALERT",
            title="Low Stock Alert for Another Tenant",
            body="Low stock alert body for another tenant",
            created_by=self.admin_id
        )
        
        # Create a user for the other tenant
        other_tenant_user = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'other@example.com',
            'tenant_id': str(another_tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_tenantsetting', 'add_tenantsetting', 'change_tenantsetting', 'delete_tenantsetting',
                           'view_emailtemplate', 'add_emailtemplate', 'change_emailtemplate', 'delete_emailtemplate',
                           'view_notificationtemplate', 'add_notificationtemplate', 'change_notificationtemplate', 'delete_notificationtemplate']
        })
        
        # Authenticate as the other tenant user
        self.client.force_authenticate(user=other_tenant_user)
        
        # List tenant settings (should only see settings for their tenant)
        url = reverse('tenant-settings-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['key'], "DEFAULT_TAX_RATE")
        self.assertEqual(response.data['results'][0]['value'], "20.0")
        
        # Try to access a tenant setting from a different tenant (should return 404)
        url = reverse('tenant-settings-detail', args=[self.tenant_setting.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # List email templates (should only see templates for their tenant)
        url = reverse('email-templates-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject'], "Welcome Email for Another Tenant")
        
        # Try to access an email template from a different tenant (should return 404)
        url = reverse('email-templates-detail', args=[self.email_template.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # List notification templates (should only see templates for their tenant)
        url = reverse('notification-templates-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Low Stock Alert for Another Tenant")
        
        # Try to access a notification template from a different tenant (should return 404)
        url = reverse('notification-templates-detail', args=[self.notification_template.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)