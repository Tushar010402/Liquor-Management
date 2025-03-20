import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserShopAssignment, UserPermission

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')
        
        # Create tenants (represented by UUIDs)
        tenant1_id = uuid.uuid4()
        tenant2_id = uuid.uuid4()
        
        self.stdout.write(f'Created tenant 1: {tenant1_id}')
        self.stdout.write(f'Created tenant 2: {tenant2_id}')
        
        # Create shops (represented by UUIDs)
        tenant1_shop1_id = uuid.uuid4()
        tenant1_shop2_id = uuid.uuid4()
        tenant2_shop1_id = uuid.uuid4()
        
        self.stdout.write(f'Created shop 1 for tenant 1: {tenant1_shop1_id}')
        self.stdout.write(f'Created shop 2 for tenant 1: {tenant1_shop2_id}')
        self.stdout.write(f'Created shop 1 for tenant 2: {tenant2_shop1_id}')
        
        # Create SaaS Admin
        saas_admin = User.objects.create_user(
            email='saas_admin@example.com',
            password='password123',
            full_name='SaaS Admin',
            role=User.ROLE_SAAS_ADMIN,
            is_staff=True,
            is_superuser=True
        )
        self.stdout.write(f'Created SaaS Admin: {saas_admin.email}')
        
        # Create Tenant Admin for Tenant 1
        tenant1_admin = User.objects.create_user(
            email='tenant1_admin@example.com',
            password='password123',
            full_name='Tenant 1 Admin',
            role=User.ROLE_TENANT_ADMIN,
            tenant_id=tenant1_id
        )
        self.stdout.write(f'Created Tenant 1 Admin: {tenant1_admin.email}')
        
        # Create Tenant Admin for Tenant 2
        tenant2_admin = User.objects.create_user(
            email='tenant2_admin@example.com',
            password='password123',
            full_name='Tenant 2 Admin',
            role=User.ROLE_TENANT_ADMIN,
            tenant_id=tenant2_id
        )
        self.stdout.write(f'Created Tenant 2 Admin: {tenant2_admin.email}')
        
        # Create Manager for Tenant 1
        tenant1_manager = User.objects.create_user(
            email='tenant1_manager@example.com',
            password='password123',
            full_name='Tenant 1 Manager',
            role=User.ROLE_MANAGER,
            tenant_id=tenant1_id
        )
        self.stdout.write(f'Created Tenant 1 Manager: {tenant1_manager.email}')
        
        # Assign shops to manager
        UserShopAssignment.objects.create(
            user=tenant1_manager,
            shop_id=tenant1_shop1_id,
            is_primary=True
        )
        UserShopAssignment.objects.create(
            user=tenant1_manager,
            shop_id=tenant1_shop2_id,
            is_primary=False
        )
        self.stdout.write(f'Assigned shops to Tenant 1 Manager')
        
        # Create Assistant Manager for Tenant 1
        tenant1_assistant_manager = User.objects.create_user(
            email='tenant1_assistant@example.com',
            password='password123',
            full_name='Tenant 1 Assistant Manager',
            role=User.ROLE_ASSISTANT_MANAGER,
            tenant_id=tenant1_id
        )
        self.stdout.write(f'Created Tenant 1 Assistant Manager: {tenant1_assistant_manager.email}')
        
        # Assign shop to assistant manager
        UserShopAssignment.objects.create(
            user=tenant1_assistant_manager,
            shop_id=tenant1_shop1_id,
            is_primary=True
        )
        self.stdout.write(f'Assigned shop to Tenant 1 Assistant Manager')
        
        # Create Executive for Tenant 1
        tenant1_executive = User.objects.create_user(
            email='tenant1_executive@example.com',
            password='password123',
            full_name='Tenant 1 Executive',
            role=User.ROLE_EXECUTIVE,
            tenant_id=tenant1_id
        )
        self.stdout.write(f'Created Tenant 1 Executive: {tenant1_executive.email}')
        
        # Assign shop to executive
        UserShopAssignment.objects.create(
            user=tenant1_executive,
            shop_id=tenant1_shop1_id,
            is_primary=True
        )
        self.stdout.write(f'Assigned shop to Tenant 1 Executive')
        
        # Create Manager for Tenant 2
        tenant2_manager = User.objects.create_user(
            email='tenant2_manager@example.com',
            password='password123',
            full_name='Tenant 2 Manager',
            role=User.ROLE_MANAGER,
            tenant_id=tenant2_id
        )
        self.stdout.write(f'Created Tenant 2 Manager: {tenant2_manager.email}')
        
        # Assign shop to manager
        UserShopAssignment.objects.create(
            user=tenant2_manager,
            shop_id=tenant2_shop1_id,
            is_primary=True
        )
        self.stdout.write(f'Assigned shop to Tenant 2 Manager')
        
        # Add custom permissions
        UserPermission.objects.create(
            user=tenant1_manager,
            permission_key='can_approve_large_sales'
        )
        UserPermission.objects.create(
            user=tenant1_manager,
            permission_key='can_view_financial_reports'
        )
        self.stdout.write(f'Added custom permissions to Tenant 1 Manager')
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))