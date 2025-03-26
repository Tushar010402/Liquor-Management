import uuid
import datetime
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tenants.models import Tenant, TenantSettings
from shops.models import Shop, ShopOperatingHours, ShopSettings
from settings.models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate

class Command(BaseCommand):
    help = 'Creates test data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')
        
        # Create system settings
        self.create_system_settings()
        
        # Create tenants
        tenant1 = self.create_tenant(
            name='ABC Liquors',
            address='123 Main St',
            city='Mumbai',
            state='Maharashtra',
            country='India',
            postal_code='400001',
            phone='9876543210',
            email='contact@abcliquors.com',
            website='https://abcliquors.com',
            business_type='Retail',
            tax_id='GSTIN123456789',
            license_number='L-123456',
            license_expiry=datetime.date(2025, 12, 31),
            subscription_plan='premium',
            max_shops=10,
            max_users=50,
            contact_person_name='Raj Sharma',
            contact_person_email='raj@abcliquors.com',
            contact_person_phone='9876543211'
        )
        
        tenant2 = self.create_tenant(
            name='XYZ Wines',
            address='456 Park Avenue',
            city='Delhi',
            state='Delhi',
            country='India',
            postal_code='110001',
            phone='9876543220',
            email='contact@xyzwines.com',
            website='https://xyzwines.com',
            business_type='Wholesale',
            tax_id='GSTIN987654321',
            license_number='L-654321',
            license_expiry=datetime.date(2025, 10, 15),
            subscription_plan='basic',
            max_shops=3,
            max_users=15,
            contact_person_name='Priya Patel',
            contact_person_email='priya@xyzwines.com',
            contact_person_phone='9876543222'
        )
        
        # Create shops for tenant 1
        shop1 = self.create_shop(
            tenant_id=tenant1.id,
            name='ABC Liquors - Downtown',
            code='ABC-DT',
            address='123 Main St, Downtown',
            city='Mumbai',
            state='Maharashtra',
            country='India',
            postal_code='400001',
            phone='9876543212',
            email='downtown@abcliquors.com',
            license_number='L-123456-DT',
            license_expiry=datetime.date(2025, 12, 31),
            manager_id=uuid.uuid4(),
            manager_name='Vikram Singh',
            manager_phone='9876543213',
            manager_email='vikram@abcliquors.com'
        )
        
        shop2 = self.create_shop(
            tenant_id=tenant1.id,
            name='ABC Liquors - Uptown',
            code='ABC-UT',
            address='456 Park Avenue, Uptown',
            city='Mumbai',
            state='Maharashtra',
            country='India',
            postal_code='400002',
            phone='9876543214',
            email='uptown@abcliquors.com',
            license_number='L-123456-UT',
            license_expiry=datetime.date(2025, 12, 31),
            manager_id=uuid.uuid4(),
            manager_name='Anita Desai',
            manager_phone='9876543215',
            manager_email='anita@abcliquors.com'
        )
        
        # Create shop for tenant 2
        shop3 = self.create_shop(
            tenant_id=tenant2.id,
            name='XYZ Wines - Central',
            code='XYZ-CT',
            address='789 Central Avenue',
            city='Delhi',
            state='Delhi',
            country='India',
            postal_code='110001',
            phone='9876543223',
            email='central@xyzwines.com',
            license_number='L-654321-CT',
            license_expiry=datetime.date(2025, 10, 15),
            manager_id=uuid.uuid4(),
            manager_name='Rahul Verma',
            manager_phone='9876543224',
            manager_email='rahul@xyzwines.com'
        )
        
        # Create operating hours for shops
        self.create_operating_hours(shop1)
        self.create_operating_hours(shop2)
        self.create_operating_hours(shop3)
        
        # Create tenant settings
        self.create_tenant_settings(tenant1.id)
        self.create_tenant_settings(tenant2.id)
        
        # Create email templates
        self.create_email_templates(tenant1.id)
        self.create_email_templates(tenant2.id)
        
        # Create notification templates
        self.create_notification_templates(tenant1.id)
        self.create_notification_templates(tenant2.id)
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
    
    def create_system_settings(self):
        """
        Create system settings.
        """
        settings = [
            {
                'key': 'system.name',
                'value': 'Liquor Shop Management System',
                'description': 'Name of the system',
                'is_public': True
            },
            {
                'key': 'system.version',
                'value': '1.0.0',
                'description': 'Current system version',
                'is_public': True
            },
            {
                'key': 'system.maintenance_mode',
                'value': 'false',
                'description': 'Whether the system is in maintenance mode',
                'is_public': True
            },
            {
                'key': 'system.default_timezone',
                'value': 'Asia/Kolkata',
                'description': 'Default timezone for the system',
                'is_public': True
            },
            {
                'key': 'system.support_email',
                'value': 'support@liquorshop.com',
                'description': 'Support email address',
                'is_public': True
            },
            {
                'key': 'system.support_phone',
                'value': '+91 9876543200',
                'description': 'Support phone number',
                'is_public': True
            },
            {
                'key': 'system.max_file_upload_size',
                'value': '5242880',  # 5MB
                'description': 'Maximum file upload size in bytes',
                'is_public': True
            },
            {
                'key': 'system.allowed_file_types',
                'value': 'jpg,jpeg,png,pdf,xlsx,csv',
                'description': 'Allowed file types for upload',
                'is_public': True
            },
            {
                'key': 'system.password_policy.min_length',
                'value': '8',
                'description': 'Minimum password length',
                'is_public': True
            },
            {
                'key': 'system.password_policy.require_uppercase',
                'value': 'true',
                'description': 'Whether passwords require uppercase letters',
                'is_public': True
            }
        ]
        
        for setting in settings:
            SystemSetting.objects.get_or_create(
                key=setting['key'],
                defaults={
                    'value': setting['value'],
                    'description': setting['description'],
                    'is_public': setting['is_public']
                }
            )
        
        self.stdout.write(f'Created {len(settings)} system settings')
    
    def create_tenant(self, **kwargs):
        """
        Create a tenant with the given attributes.
        """
        name = kwargs.pop('name')
        tenant, created = Tenant.objects.get_or_create(
            name=name,
            defaults={
                'slug': slugify(name),
                **kwargs
            }
        )
        
        if created:
            # Create tenant settings
            TenantSettings.objects.create(tenant=tenant)
            self.stdout.write(f'Created tenant: {tenant.name}')
        else:
            self.stdout.write(f'Tenant already exists: {tenant.name}')
        
        return tenant
    
    def create_shop(self, **kwargs):
        """
        Create a shop with the given attributes.
        """
        tenant_id = kwargs.pop('tenant_id')
        name = kwargs.pop('name')
        code = kwargs.pop('code')
        
        shop, created = Shop.objects.get_or_create(
            tenant_id=tenant_id,
            code=code,
            defaults={
                'name': name,
                **kwargs
            }
        )
        
        if created:
            # Create shop settings
            ShopSettings.objects.create(
                shop=shop,
                tenant_id=tenant_id
            )
            self.stdout.write(f'Created shop: {shop.name}')
        else:
            self.stdout.write(f'Shop already exists: {shop.name}')
        
        return shop
    
    def create_operating_hours(self, shop):
        """
        Create operating hours for a shop.
        """
        # Delete existing operating hours
        ShopOperatingHours.objects.filter(shop=shop).delete()
        
        # Create operating hours for each day of the week
        for day in range(7):
            # Monday to Saturday: 10:00 AM to 10:00 PM
            if day < 6:
                ShopOperatingHours.objects.create(
                    shop=shop,
                    tenant_id=shop.tenant_id,
                    day_of_week=day,
                    opening_time=datetime.time(10, 0),
                    closing_time=datetime.time(22, 0),
                    is_closed=False
                )
            # Sunday: Closed
            else:
                ShopOperatingHours.objects.create(
                    shop=shop,
                    tenant_id=shop.tenant_id,
                    day_of_week=day,
                    opening_time=datetime.time(0, 0),
                    closing_time=datetime.time(0, 0),
                    is_closed=True
                )
        
        self.stdout.write(f'Created operating hours for shop: {shop.name}')
    
    def create_tenant_settings(self, tenant_id):
        """
        Create tenant settings.
        """
        settings = [
            {
                'key': 'tenant.default_currency',
                'value': 'INR',
                'description': 'Default currency for the tenant'
            },
            {
                'key': 'tenant.default_language',
                'value': 'en-IN',
                'description': 'Default language for the tenant'
            },
            {
                'key': 'tenant.default_timezone',
                'value': 'Asia/Kolkata',
                'description': 'Default timezone for the tenant'
            },
            {
                'key': 'tenant.tax_rate',
                'value': '18.0',
                'description': 'Default tax rate for the tenant'
            },
            {
                'key': 'tenant.enable_sms_notifications',
                'value': 'true',
                'description': 'Whether SMS notifications are enabled'
            },
            {
                'key': 'tenant.enable_email_notifications',
                'value': 'true',
                'description': 'Whether email notifications are enabled'
            },
            {
                'key': 'tenant.low_stock_threshold',
                'value': '10',
                'description': 'Low stock threshold for inventory alerts'
            },
            {
                'key': 'tenant.expiry_alert_days',
                'value': '30',
                'description': 'Days before expiry to send alerts'
            },
            {
                'key': 'tenant.require_sales_approval',
                'value': 'true',
                'description': 'Whether sales require approval'
            },
            {
                'key': 'tenant.max_discount_percentage',
                'value': '10.0',
                'description': 'Maximum discount percentage allowed'
            }
        ]
        
        for setting in settings:
            TenantSetting.objects.get_or_create(
                tenant_id=tenant_id,
                key=setting['key'],
                defaults={
                    'value': setting['value'],
                    'description': setting['description']
                }
            )
        
        self.stdout.write(f'Created {len(settings)} tenant settings for tenant: {tenant_id}')
    
    def create_email_templates(self, tenant_id):
        """
        Create email templates for a tenant.
        """
        templates = [
            {
                'name': 'welcome_email',
                'subject': 'Welcome to {{tenant_name}}',
                'body': '''
                <p>Dear {{user_name}},</p>
                <p>Welcome to {{tenant_name}}! Your account has been created successfully.</p>
                <p>Your login credentials:</p>
                <ul>
                    <li>Email: {{user_email}}</li>
                    <li>Password: {{user_password}}</li>
                </ul>
                <p>Please change your password after your first login.</p>
                <p>Best regards,<br>{{tenant_name}} Team</p>
                ''',
                'description': 'Email sent to new users'
            },
            {
                'name': 'password_reset',
                'subject': 'Password Reset Request',
                'body': '''
                <p>Dear {{user_name}},</p>
                <p>We received a request to reset your password. Please click the link below to reset your password:</p>
                <p><a href="{{reset_link}}">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>Best regards,<br>{{tenant_name}} Team</p>
                ''',
                'description': 'Email sent for password reset'
            },
            {
                'name': 'sale_approval',
                'subject': 'Sale Approval Required',
                'body': '''
                <p>Dear {{manager_name}},</p>
                <p>A new sale requires your approval:</p>
                <ul>
                    <li>Sale ID: {{sale_id}}</li>
                    <li>Amount: {{sale_amount}}</li>
                    <li>Created by: {{executive_name}}</li>
                    <li>Shop: {{shop_name}}</li>
                    <li>Date: {{sale_date}}</li>
                </ul>
                <p>Please login to the system to approve or reject this sale.</p>
                <p>Best regards,<br>{{tenant_name}} Team</p>
                ''',
                'description': 'Email sent for sale approval'
            },
            {
                'name': 'low_stock_alert',
                'subject': 'Low Stock Alert',
                'body': '''
                <p>Dear {{manager_name}},</p>
                <p>The following products are running low on stock:</p>
                <ul>
                    {{#products}}
                    <li>{{name}} - Current stock: {{current_stock}}</li>
                    {{/products}}
                </ul>
                <p>Please take necessary action to replenish the stock.</p>
                <p>Best regards,<br>{{tenant_name}} Team</p>
                ''',
                'description': 'Email sent for low stock alerts'
            }
        ]
        
        for template in templates:
            EmailTemplate.objects.get_or_create(
                tenant_id=tenant_id,
                name=template['name'],
                defaults={
                    'subject': template['subject'],
                    'body': template['body'],
                    'description': template['description']
                }
            )
        
        self.stdout.write(f'Created {len(templates)} email templates for tenant: {tenant_id}')
    
    def create_notification_templates(self, tenant_id):
        """
        Create notification templates for a tenant.
        """
        templates = [
            {
                'name': 'sale_approval_required',
                'title': 'Sale Approval Required',
                'body': 'Sale #{{sale_id}} requires your approval.',
                'description': 'Notification sent when a sale requires approval'
            },
            {
                'name': 'sale_approved',
                'title': 'Sale Approved',
                'body': 'Sale #{{sale_id}} has been approved by {{manager_name}}.',
                'description': 'Notification sent when a sale is approved'
            },
            {
                'name': 'sale_rejected',
                'title': 'Sale Rejected',
                'body': 'Sale #{{sale_id}} has been rejected by {{manager_name}}.',
                'description': 'Notification sent when a sale is rejected'
            },
            {
                'name': 'low_stock_alert',
                'title': 'Low Stock Alert',
                'body': '{{product_name}} is running low on stock ({{current_stock}} remaining).',
                'description': 'Notification sent for low stock alerts'
            },
            {
                'name': 'expiry_alert',
                'title': 'Product Expiry Alert',
                'body': '{{product_name}} will expire in {{days_to_expiry}} days.',
                'description': 'Notification sent for product expiry alerts'
            }
        ]
        
        for template in templates:
            NotificationTemplate.objects.get_or_create(
                tenant_id=tenant_id,
                name=template['name'],
                defaults={
                    'title': template['title'],
                    'body': template['body'],
                    'description': template['description']
                }
            )
        
        self.stdout.write(f'Created {len(templates)} notification templates for tenant: {tenant_id}')