import uuid
import json
from decimal import Decimal
from datetime import date, time, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from shops.models import Shop, ShopSettings, ShopActivity
from authentication.models import Tenant

User = get_user_model()

class ShopsAPITest(TestCase):
    """
    Test the shops API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create tenant
        self.tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            domain="testtenant.com",
            status=Tenant.STATUS_ACTIVE,
            business_name="Test Liquor Enterprises",
            business_address="123 Main St, City, State, 12345",
            business_phone="1234567890",
            business_email="contact@testtenant.com",
            contact_name="John Doe",
            contact_email="john.doe@testtenant.com",
            contact_phone="9876543210"
        )
        self.tenant_id = self.tenant.id
        
        # Create shops
        self.shop1 = Shop.objects.create(
            tenant_id=self.tenant_id,
            name="Downtown Liquor Store",
            code="DLS001",
            shop_type=Shop.TYPE_RETAIL,
            status=Shop.STATUS_ACTIVE,
            address="123 Main St, Downtown",
            city="Metropolis",
            state="State",
            country="Country",
            postal_code="12345",
            latitude=Decimal('37.123456'),
            longitude=Decimal('-122.123456'),
            phone="1234567890",
            email="downtown@example.com",
            license_number="LIQ123456",
            license_type="Retail Liquor License",
            license_expiry=date.today() + timedelta(days=365),
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            is_open_on_sunday=False,
            description="Downtown premium liquor store"
        )
        
        self.shop2 = Shop.objects.create(
            tenant_id=self.tenant_id,
            name="Uptown Liquor Store",
            code="ULS001",
            shop_type=Shop.TYPE_BOTH,
            status=Shop.STATUS_ACTIVE,
            address="456 Oak St, Uptown",
            city="Metropolis",
            state="State",
            country="Country",
            postal_code="12346",
            latitude=Decimal('37.654321'),
            longitude=Decimal('-122.654321'),
            phone="2345678901",
            email="uptown@example.com",
            license_number="LIQ234567",
            license_type="Retail & Wholesale Liquor License",
            license_expiry=date.today() + timedelta(days=365),
            opening_time=time(10, 0),
            closing_time=time(22, 0),
            is_open_on_sunday=True,
            description="Uptown premium liquor store"
        )
        
        # Create shop settings
        self.shop_settings1 = ShopSettings.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop1,
            enable_low_stock_alerts=True,
            low_stock_threshold=5,
            enable_expiry_alerts=True,
            expiry_alert_days=45,
            default_tax_rate=Decimal('18.00'),
            enable_discounts=True,
            max_discount_percentage=Decimal('15.00'),
            require_discount_approval=True,
            discount_approval_threshold=Decimal('7.50'),
            require_sales_approval=False,
            require_stock_adjustment_approval=True,
            require_return_approval=True,
            receipt_header="Downtown Liquor Store\n123 Main St, Downtown",
            receipt_footer="Thank you for shopping with us!",
            show_tax_on_receipt=True,
            settings_json={
                'enable_loyalty_program': True,
                'points_per_dollar': 1,
                'redemption_rate': 0.01
            }
        )
        
        # Create users
        self.tenant_admin = User.objects.create_user(
            email="admin@testtenant.com",
            password="adminpassword",
            full_name="Tenant Admin",
            tenant_id=self.tenant_id,
            role=User.ROLE_TENANT_ADMIN,
            is_active=True
        )
        
        self.shop_manager = User.objects.create_user(
            email="manager@testtenant.com",
            password="managerpassword",
            full_name="Shop Manager",
            tenant_id=self.tenant_id,
            role=User.ROLE_MANAGER,
            is_active=True
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Login as tenant admin
        login_url = reverse('login')
        login_data = {
            'email': 'admin@testtenant.com',
            'password': 'adminpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.tenant_admin_token = login_response.data['data']['access_token']
        
        # Login as shop manager
        login_data = {
            'email': 'manager@testtenant.com',
            'password': 'managerpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.shop_manager_token = login_response.data['data']['access_token']
    
    def test_list_shops(self):
        """
        Test listing shops.
        """
        url = reverse('shop-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that the response contains the expected shops
        shop_names = [shop['name'] for shop in response.data['results']]
        self.assertIn('Downtown Liquor Store', shop_names)
        self.assertIn('Uptown Liquor Store', shop_names)
    
    def test_filter_shops_by_type(self):
        """
        Test filtering shops by type.
        """
        url = reverse('shop-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url, {'shop_type': Shop.TYPE_BOTH})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Uptown Liquor Store')
        self.assertEqual(response.data['results'][0]['shop_type'], Shop.TYPE_BOTH)
    
    def test_filter_shops_by_status(self):
        """
        Test filtering shops by status.
        """
        # Create an inactive shop
        Shop.objects.create(
            tenant_id=self.tenant_id,
            name="Inactive Liquor Store",
            code="ILS001",
            shop_type=Shop.TYPE_RETAIL,
            status=Shop.STATUS_INACTIVE,
            address="789 Pine St, Suburb",
            city="Metropolis",
            state="State",
            country="Country",
            postal_code="12347",
            phone="3456789012",
            email="inactive@example.com",
            license_number="LIQ345678",
            license_type="Retail Liquor License",
            license_expiry=date.today() + timedelta(days=365),
            opening_time=time(9, 0),
            closing_time=time(21, 0)
        )
        
        url = reverse('shop-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url, {'status': Shop.STATUS_INACTIVE})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Inactive Liquor Store')
        self.assertEqual(response.data['results'][0]['status'], Shop.STATUS_INACTIVE)
    
    def test_create_shop(self):
        """
        Test creating a shop.
        """
        url = reverse('shop-list')
        data = {
            'name': 'New Liquor Store',
            'code': 'NLS001',
            'shop_type': Shop.TYPE_RETAIL,
            'status': Shop.STATUS_ACTIVE,
            'address': '789 Pine St, Suburb',
            'city': 'Metropolis',
            'state': 'State',
            'country': 'Country',
            'postal_code': '12347',
            'phone': '3456789012',
            'email': 'new@example.com',
            'license_number': 'LIQ345678',
            'license_type': 'Retail Liquor License',
            'license_expiry': (date.today() + timedelta(days=365)).isoformat(),
            'opening_time': '09:00:00',
            'closing_time': '21:00:00',
            'is_open_on_sunday': True,
            'description': 'New premium liquor store'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Liquor Store')
        self.assertEqual(response.data['code'], 'NLS001')
        self.assertEqual(response.data['shop_type'], Shop.TYPE_RETAIL)
        self.assertEqual(response.data['status'], Shop.STATUS_ACTIVE)
        self.assertEqual(response.data['address'], '789 Pine St, Suburb')
        self.assertEqual(response.data['city'], 'Metropolis')
        self.assertEqual(response.data['phone'], '3456789012')
        self.assertEqual(response.data['email'], 'new@example.com')
        self.assertEqual(response.data['license_number'], 'LIQ345678')
        self.assertEqual(response.data['opening_time'], '09:00:00')
        self.assertEqual(response.data['closing_time'], '21:00:00')
        self.assertTrue(response.data['is_open_on_sunday'])
        
        # Check that the shop was created in the database
        shop = Shop.objects.get(code='NLS001')
        self.assertEqual(shop.name, 'New Liquor Store')
        self.assertEqual(shop.tenant_id, self.tenant_id)
        self.assertEqual(shop.email, 'new@example.com')
    
    def test_retrieve_shop(self):
        """
        Test retrieving a shop.
        """
        url = reverse('shop-detail', args=[self.shop1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Downtown Liquor Store')
        self.assertEqual(response.data['code'], 'DLS001')
        self.assertEqual(response.data['shop_type'], Shop.TYPE_RETAIL)
        self.assertEqual(response.data['status'], Shop.STATUS_ACTIVE)
        self.assertEqual(response.data['address'], '123 Main St, Downtown')
        self.assertEqual(response.data['city'], 'Metropolis')
        self.assertEqual(response.data['phone'], '1234567890')
        self.assertEqual(response.data['email'], 'downtown@example.com')
        self.assertEqual(response.data['license_number'], 'LIQ123456')
        self.assertEqual(response.data['opening_time'], '09:00:00')
        self.assertEqual(response.data['closing_time'], '21:00:00')
        self.assertFalse(response.data['is_open_on_sunday'])
    
    def test_update_shop(self):
        """
        Test updating a shop.
        """
        url = reverse('shop-detail', args=[self.shop1.id])
        data = {
            'phone': '9998887777',
            'email': 'updated@example.com',
            'opening_time': '08:00:00',
            'closing_time': '22:00:00',
            'is_open_on_sunday': True,
            'description': 'Updated description'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '9998887777')
        self.assertEqual(response.data['email'], 'updated@example.com')
        self.assertEqual(response.data['opening_time'], '08:00:00')
        self.assertEqual(response.data['closing_time'], '22:00:00')
        self.assertTrue(response.data['is_open_on_sunday'])
        self.assertEqual(response.data['description'], 'Updated description')
        
        # Check that the shop was updated in the database
        self.shop1.refresh_from_db()
        self.assertEqual(self.shop1.phone, '9998887777')
        self.assertEqual(self.shop1.email, 'updated@example.com')
        self.assertEqual(self.shop1.opening_time, time(8, 0))
        self.assertEqual(self.shop1.closing_time, time(22, 0))
        self.assertTrue(self.shop1.is_open_on_sunday)
        self.assertEqual(self.shop1.description, 'Updated description')
    
    def test_deactivate_shop(self):
        """
        Test deactivating a shop.
        """
        url = reverse('shop-deactivate', args=[self.shop1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Shop.STATUS_INACTIVE)
        
        # Check that the shop was deactivated in the database
        self.shop1.refresh_from_db()
        self.assertEqual(self.shop1.status, Shop.STATUS_INACTIVE)
    
    def test_activate_shop(self):
        """
        Test activating a shop.
        """
        # First deactivate the shop
        self.shop1.status = Shop.STATUS_INACTIVE
        self.shop1.save()
        
        url = reverse('shop-activate', args=[self.shop1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Shop.STATUS_ACTIVE)
        
        # Check that the shop was activated in the database
        self.shop1.refresh_from_db()
        self.assertEqual(self.shop1.status, Shop.STATUS_ACTIVE)
    
    def test_get_shop_settings(self):
        """
        Test getting shop settings.
        """
        url = reverse('shop-settings', args=[self.shop1.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shop'], str(self.shop1.id))
        self.assertTrue(response.data['enable_low_stock_alerts'])
        self.assertEqual(response.data['low_stock_threshold'], 5)
        self.assertEqual(response.data['default_tax_rate'], '18.00')
        self.assertEqual(response.data['max_discount_percentage'], '15.00')
        self.assertEqual(response.data['receipt_header'], 'Downtown Liquor Store\n123 Main St, Downtown')
        self.assertTrue(response.data['settings_json']['enable_loyalty_program'])
    
    def test_update_shop_settings(self):
        """
        Test updating shop settings.
        """
        url = reverse('shop-settings', args=[self.shop1.id])
        data = {
            'low_stock_threshold': 10,
            'default_tax_rate': '20.00',
            'max_discount_percentage': '10.00',
            'receipt_header': 'Updated Header',
            'receipt_footer': 'Updated Footer',
            'settings_json': {
                'enable_loyalty_program': True,
                'points_per_dollar': 2,
                'redemption_rate': 0.02
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['low_stock_threshold'], 10)
        self.assertEqual(response.data['default_tax_rate'], '20.00')
        self.assertEqual(response.data['max_discount_percentage'], '10.00')
        self.assertEqual(response.data['receipt_header'], 'Updated Header')
        self.assertEqual(response.data['receipt_footer'], 'Updated Footer')
        self.assertEqual(response.data['settings_json']['points_per_dollar'], 2)
        self.assertEqual(response.data['settings_json']['redemption_rate'], 0.02)
        
        # Check that the settings were updated in the database
        self.shop_settings1.refresh_from_db()
        self.assertEqual(self.shop_settings1.low_stock_threshold, 10)
        self.assertEqual(self.shop_settings1.default_tax_rate, Decimal('20.00'))
        self.assertEqual(self.shop_settings1.max_discount_percentage, Decimal('10.00'))
        self.assertEqual(self.shop_settings1.receipt_header, 'Updated Header')
        self.assertEqual(self.shop_settings1.receipt_footer, 'Updated Footer')
        self.assertEqual(self.shop_settings1.settings_json['points_per_dollar'], 2)
        self.assertEqual(self.shop_settings1.settings_json['redemption_rate'], 0.02)
    
    def test_create_shop_settings(self):
        """
        Test creating shop settings for a shop that doesn't have them.
        """
        # First delete existing settings
        self.shop_settings1.delete()
        
        url = reverse('shop-settings', args=[self.shop1.id])
        data = {
            'enable_low_stock_alerts': True,
            'low_stock_threshold': 15,
            'default_tax_rate': '18.00',
            'enable_discounts': True,
            'max_discount_percentage': '20.00',
            'receipt_header': 'New Header',
            'receipt_footer': 'New Footer'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shop'], str(self.shop1.id))
        self.assertTrue(response.data['enable_low_stock_alerts'])
        self.assertEqual(response.data['low_stock_threshold'], 15)
        self.assertEqual(response.data['default_tax_rate'], '18.00')
        self.assertEqual(response.data['max_discount_percentage'], '20.00')
        self.assertEqual(response.data['receipt_header'], 'New Header')
        self.assertEqual(response.data['receipt_footer'], 'New Footer')
        
        # Check that the settings were created in the database
        settings = ShopSettings.objects.get(shop=self.shop1)
        self.assertEqual(settings.low_stock_threshold, 15)
        self.assertEqual(settings.max_discount_percentage, Decimal('20.00'))
        self.assertEqual(settings.receipt_header, 'New Header')
    
    def test_list_shop_activities(self):
        """
        Test listing shop activities.
        """
        # Create some shop activities
        ShopActivity.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop1,
            user_id=self.tenant_admin.id,
            activity_type="shop_opened",
            description="Shop opened for business",
            ip_address="192.168.1.1"
        )
        
        ShopActivity.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop1,
            user_id=self.shop_manager.id,
            activity_type="cash_register_opened",
            description="Cash register opened",
            ip_address="192.168.1.2"
        )
        
        url = reverse('shopactivity-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.get(url, {'shop': self.shop1.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Check that the activities are ordered by created_at in descending order
        self.assertEqual(response.data['results'][0]['activity_type'], 'cash_register_opened')
        self.assertEqual(response.data['results'][1]['activity_type'], 'shop_opened')
    
    def test_create_shop_activity(self):
        """
        Test creating a shop activity.
        """
        url = reverse('shopactivity-list')
        data = {
            'shop': str(self.shop1.id),
            'user_id': str(self.tenant_admin.id),
            'activity_type': 'inventory_count',
            'description': 'Inventory count performed',
            'ip_address': '192.168.1.3',
            'metadata': {
                'items_counted': 150,
                'discrepancies': 5
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.tenant_admin_token}')
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop'], str(self.shop1.id))
        self.assertEqual(response.data['user_id'], str(self.tenant_admin.id))
        self.assertEqual(response.data['activity_type'], 'inventory_count')
        self.assertEqual(response.data['description'], 'Inventory count performed')
        self.assertEqual(response.data['ip_address'], '192.168.1.3')
        self.assertEqual(response.data['metadata']['items_counted'], 150)
        self.assertEqual(response.data['metadata']['discrepancies'], 5)
        
        # Check that the activity was created in the database
        activity = ShopActivity.objects.get(activity_type='inventory_count')
        self.assertEqual(activity.shop, self.shop1)
        self.assertEqual(activity.user_id, self.tenant_admin.id)
        self.assertEqual(activity.description, 'Inventory count performed')
        self.assertEqual(activity.metadata['items_counted'], 150)
    
    def test_shop_manager_can_only_access_assigned_shops(self):
        """
        Test that shop managers can only access shops they are assigned to.
        """
        # TODO: Implement shop assignment for the manager and test access restrictions
        pass