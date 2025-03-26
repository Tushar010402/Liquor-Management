import uuid
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import UserShopAssignment, UserPermission
from datetime import timedelta

User = get_user_model()

class UserModelTest(TestCase):
    """
    Test the User model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        
        # Create users with different roles
        self.saas_admin = User.objects.create_user(
            email="saas_admin@example.com",
            password="password123",
            full_name="SaaS Admin",
            phone="1234567890",
            role=User.ROLE_SAAS_ADMIN,
            is_staff=True,
            is_superuser=True
        )
        
        self.tenant_admin = User.objects.create_user(
            email="tenant_admin@example.com",
            password="password123",
            full_name="Tenant Admin",
            phone="1234567891",
            tenant_id=self.tenant_id,
            role=User.ROLE_TENANT_ADMIN
        )
        
        self.manager = User.objects.create_user(
            email="manager@example.com",
            password="password123",
            full_name="Shop Manager",
            phone="1234567892",
            tenant_id=self.tenant_id,
            role=User.ROLE_MANAGER
        )
        
        self.assistant_manager = User.objects.create_user(
            email="assistant@example.com",
            password="password123",
            full_name="Assistant Manager",
            phone="1234567893",
            tenant_id=self.tenant_id,
            role=User.ROLE_ASSISTANT_MANAGER
        )
        
        self.executive = User.objects.create_user(
            email="executive@example.com",
            password="password123",
            full_name="Sales Executive",
            phone="1234567894",
            tenant_id=self.tenant_id,
            role=User.ROLE_EXECUTIVE
        )
        
        # Create shop assignments
        self.shop_assignment = UserShopAssignment.objects.create(
            tenant_id=self.tenant_id,
            user=self.manager,
            shop_id=self.shop_id,
            is_primary=True,
            created_by=self.tenant_admin.id
        )
        
        # Create custom permissions
        self.user_permission = UserPermission.objects.create(
            tenant_id=self.tenant_id,
            user=self.executive,
            permission_key="can_view_reports",
            created_by=self.tenant_admin.id
        )
    
    def test_user_creation(self):
        """
        Test User creation.
        """
        self.assertEqual(self.tenant_admin.email, "tenant_admin@example.com")
        self.assertEqual(self.tenant_admin.full_name, "Tenant Admin")
        self.assertEqual(self.tenant_admin.phone, "1234567891")
        self.assertEqual(self.tenant_admin.tenant_id, self.tenant_id)
        self.assertEqual(self.tenant_admin.role, User.ROLE_TENANT_ADMIN)
        self.assertTrue(self.tenant_admin.is_active)
        self.assertFalse(self.tenant_admin.is_staff)
        self.assertFalse(self.tenant_admin.is_superuser)
        self.assertIsNotNone(self.tenant_admin.date_joined)
        self.assertEqual(self.tenant_admin.failed_login_attempts, 0)
        self.assertIsNone(self.tenant_admin.last_failed_login)
        self.assertIsNone(self.tenant_admin.account_locked_until)
    
    def test_user_str(self):
        """
        Test User string representation.
        """
        self.assertEqual(str(self.manager), "manager@example.com")
    
    def test_get_full_name(self):
        """
        Test get_full_name method.
        """
        self.assertEqual(self.manager.get_full_name(), "Shop Manager")
    
    def test_get_short_name(self):
        """
        Test get_short_name method.
        """
        self.assertEqual(self.manager.get_short_name(), "Shop")
    
    def test_role_methods(self):
        """
        Test role-specific methods.
        """
        self.assertTrue(self.saas_admin.is_saas_admin())
        self.assertFalse(self.saas_admin.is_tenant_admin())
        
        self.assertTrue(self.tenant_admin.is_tenant_admin())
        self.assertFalse(self.tenant_admin.is_manager())
        
        self.assertTrue(self.manager.is_manager())
        self.assertFalse(self.manager.is_assistant_manager())
        
        self.assertTrue(self.assistant_manager.is_assistant_manager())
        self.assertFalse(self.assistant_manager.is_executive())
        
        self.assertTrue(self.executive.is_executive())
        self.assertFalse(self.executive.is_tenant_admin())
    
    def test_account_locking(self):
        """
        Test account locking functionality.
        """
        # Initially account should not be locked
        self.assertFalse(self.executive.is_account_locked())
        
        # Increment failed login attempts
        for _ in range(4):
            self.executive.increment_failed_login()
        
        # After 4 attempts, account should still not be locked
        self.assertEqual(self.executive.failed_login_attempts, 4)
        self.assertFalse(self.executive.is_account_locked())
        
        # One more attempt should lock the account
        self.executive.increment_failed_login()
        self.assertEqual(self.executive.failed_login_attempts, 5)
        self.assertTrue(self.executive.is_account_locked())
        
        # Test unlocking the account
        self.executive.unlock_account()
        self.assertFalse(self.executive.is_account_locked())
        self.assertEqual(self.executive.failed_login_attempts, 0)
        self.assertIsNone(self.executive.account_locked_until)
        
        # Test lock expiration
        self.executive.lock_account(duration_minutes=0)
        self.assertFalse(self.executive.is_account_locked())
    
    def test_reset_failed_login(self):
        """
        Test resetting failed login attempts.
        """
        self.executive.increment_failed_login()
        self.executive.increment_failed_login()
        self.assertEqual(self.executive.failed_login_attempts, 2)
        
        self.executive.reset_failed_login()
        self.assertEqual(self.executive.failed_login_attempts, 0)
    
    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        superuser = User.objects.create_superuser(
            email="super@example.com",
            password="superpassword"
        )
        
        self.assertEqual(superuser.email, "super@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertEqual(superuser.role, User.ROLE_SAAS_ADMIN)
    
    def test_user_shop_assignment_creation(self):
        """
        Test UserShopAssignment creation.
        """
        self.assertEqual(self.shop_assignment.user, self.manager)
        self.assertEqual(self.shop_assignment.shop_id, self.shop_id)
        self.assertTrue(self.shop_assignment.is_primary)
        self.assertEqual(self.shop_assignment.tenant_id, self.tenant_id)
        self.assertEqual(self.shop_assignment.created_by, self.tenant_admin.id)
    
    def test_user_shop_assignment_str(self):
        """
        Test UserShopAssignment string representation.
        """
        expected_str = f"manager@example.com - {self.shop_id}"
        self.assertEqual(str(self.shop_assignment), expected_str)
    
    def test_user_permission_creation(self):
        """
        Test UserPermission creation.
        """
        self.assertEqual(self.user_permission.user, self.executive)
        self.assertEqual(self.user_permission.permission_key, "can_view_reports")
        self.assertEqual(self.user_permission.tenant_id, self.tenant_id)
        self.assertEqual(self.user_permission.created_by, self.tenant_admin.id)
    
    def test_user_permission_str(self):
        """
        Test UserPermission string representation.
        """
        expected_str = "executive@example.com - can_view_reports"
        self.assertEqual(str(self.user_permission), expected_str)