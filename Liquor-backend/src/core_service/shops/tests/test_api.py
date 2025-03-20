import uuid
import json
from datetime import date, time
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from common.jwt_auth import MicroserviceUser
from core_service.shops.models import Shop, ShopOperatingHours, ShopHoliday, ShopSettings

class ShopAPITest(TestCase):
    """
    Test the shop API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_shop', 'add_shop', 'change_shop', 'delete_shop']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Create shop
        self.shop = Shop.objects.create(
            tenant_id=self.tenant_id,
            name="Downtown Liquor Store",
            code="DLS001",
            address="123 Main Street",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10001",
            phone="212-555-1234",
            email="downtown@example.com",
            license_number="LIQ-2023-12345",
            license_expiry=date(2024, 12, 31),
            tax_id="TAX-987654321",
            manager_id=self.user_id,
            manager_name="John Smith",
            manager_phone="212-555-5678",
            manager_email="john.smith@example.com",
            is_open=True,
            created_by=self.user_id
        )
        
        # Create shop operating hours
        self.operating_hours = ShopOperatingHours.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            day_of_week=0,  # Monday
            opening_time=time(9, 0),  # 9:00 AM
            closing_time=time(21, 0),  # 9:00 PM
            is_closed=False,
            created_by=self.user_id
        )
        
        # Create shop holiday
        self.holiday = ShopHoliday.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            name="New Year's Day",
            date=date(2024, 1, 1),
            description="Closed for New Year's Day",
            created_by=self.user_id
        )
        
        # Create shop settings
        self.settings = ShopSettings.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            enable_low_stock_alerts=True,
            low_stock_threshold=10,
            enable_expiry_alerts=True,
            expiry_alert_days=30,
            default_tax_rate=Decimal('18.00'),
            enable_discounts=True,
            max_discount_percentage=Decimal('10.00'),
            require_discount_approval=True,
            discount_approval_threshold=Decimal('5.00'),
            receipt_header="Downtown Liquor Store\n123 Main Street\nNew York, NY 10001",
            receipt_footer="Thank you for shopping with us!",
            show_tax_on_receipt=True,
            enable_cash_management=True,
            require_cash_verification=True,
            created_by=self.user_id
        )
        
        # Create another shop
        self.shop2 = Shop.objects.create(
            tenant_id=self.tenant_id,
            name="Uptown Liquor Store",
            code="ULS001",
            address="456 Park Avenue",
            city="New York",
            state="NY",
            country="USA",
            postal_code="10022",
            created_by=self.user_id
        )
    
    def test_list_shops(self):
        """
        Test listing shops.
        """
        url = reverse('shop-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Downtown Liquor Store")
        self.assertEqual(response.data['results'][1]['name'], "Uptown Liquor Store")
    
    def test_retrieve_shop(self):
        """
        Test retrieving a shop.
        """
        url = reverse('shop-detail', args=[self.shop.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Downtown Liquor Store")
        self.assertEqual(response.data['code'], "DLS001")
        self.assertEqual(response.data['address'], "123 Main Street")
        self.assertEqual(response.data['city'], "New York")
        self.assertEqual(response.data['state'], "NY")
        self.assertEqual(response.data['country'], "USA")
        self.assertEqual(response.data['postal_code'], "10001")
        self.assertEqual(response.data['phone'], "212-555-1234")
        self.assertEqual(response.data['email'], "downtown@example.com")
        self.assertEqual(response.data['license_number'], "LIQ-2023-12345")
        self.assertEqual(response.data['license_expiry'], "2024-12-31")
        self.assertEqual(response.data['tax_id'], "TAX-987654321")
        self.assertEqual(response.data['manager_id'], str(self.user_id))
        self.assertEqual(response.data['manager_name'], "John Smith")
        self.assertEqual(response.data['manager_phone'], "212-555-5678")
        self.assertEqual(response.data['manager_email'], "john.smith@example.com")
        self.assertTrue(response.data['is_open'])
    
    def test_create_shop(self):
        """
        Test creating a shop.
        """
        url = reverse('shop-list')
        data = {
            'name': "Midtown Liquor Store",
            'code': "MLS001",
            'address': "789 Broadway",
            'city': "New York",
            'state': "NY",
            'country': "USA",
            'postal_code': "10003",
            'phone': "212-555-4321",
            'email': "midtown@example.com",
            'license_number': "LIQ-2023-67890",
            'license_expiry': "2024-12-31",
            'tax_id': "TAX-123456789",
            'manager_id': str(self.user_id),
            'manager_name': "Jane Doe",
            'manager_phone': "212-555-8765",
            'manager_email': "jane.doe@example.com",
            'is_open': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Midtown Liquor Store")
        self.assertEqual(response.data['code'], "MLS001")
        
        # Check that the shop was created in the database
        shop = Shop.objects.get(code="MLS001")
        self.assertEqual(shop.name, "Midtown Liquor Store")
        self.assertEqual(shop.tenant_id, self.tenant_id)
        self.assertEqual(shop.created_by, self.user_id)
    
    def test_update_shop(self):
        """
        Test updating a shop.
        """
        url = reverse('shop-detail', args=[self.shop.id])
        data = {
            'name': "Downtown Liquor Emporium",
            'address': "123 Main Street, Suite 100",
            'phone': "212-555-9876",
            'email': "downtown.emporium@example.com"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Downtown Liquor Emporium")
        self.assertEqual(response.data['address'], "123 Main Street, Suite 100")
        self.assertEqual(response.data['phone'], "212-555-9876")
        self.assertEqual(response.data['email'], "downtown.emporium@example.com")
        
        # Check that the shop was updated in the database
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, "Downtown Liquor Emporium")
        self.assertEqual(self.shop.address, "123 Main Street, Suite 100")
        self.assertEqual(self.shop.phone, "212-555-9876")
        self.assertEqual(self.shop.email, "downtown.emporium@example.com")
    
    def test_delete_shop(self):
        """
        Test deleting a shop.
        """
        url = reverse('shop-detail', args=[self.shop2.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the shop was deleted from the database
        with self.assertRaises(Shop.DoesNotExist):
            Shop.objects.get(id=self.shop2.id)
    
    def test_list_operating_hours(self):
        """
        Test listing shop operating hours.
        """
        url = reverse('shop-operating-hours-list', args=[self.shop.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['day_of_week'], 0)
        self.assertEqual(response.data[0]['opening_time'], '09:00:00')
        self.assertEqual(response.data[0]['closing_time'], '21:00:00')
        self.assertFalse(response.data[0]['is_closed'])
    
    def test_create_operating_hours(self):
        """
        Test creating shop operating hours.
        """
        url = reverse('shop-operating-hours-list', args=[self.shop.id])
        data = {
            'day_of_week': 1,  # Tuesday
            'opening_time': '09:00:00',
            'closing_time': '21:00:00',
            'is_closed': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['day_of_week'], 1)
        self.assertEqual(response.data['opening_time'], '09:00:00')
        self.assertEqual(response.data['closing_time'], '21:00:00')
        self.assertFalse(response.data['is_closed'])
        
        # Check that the operating hours were created in the database
        hours = ShopOperatingHours.objects.get(shop=self.shop, day_of_week=1)
        self.assertEqual(hours.opening_time, time(9, 0))
        self.assertEqual(hours.closing_time, time(21, 0))
        self.assertFalse(hours.is_closed)
        self.assertEqual(hours.tenant_id, self.tenant_id)
        self.assertEqual(hours.created_by, self.user_id)
    
    def test_update_operating_hours(self):
        """
        Test updating shop operating hours.
        """
        url = reverse('shop-operating-hours-detail', args=[self.shop.id, self.operating_hours.id])
        data = {
            'opening_time': '10:00:00',
            'closing_time': '22:00:00'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['opening_time'], '10:00:00')
        self.assertEqual(response.data['closing_time'], '22:00:00')
        
        # Check that the operating hours were updated in the database
        self.operating_hours.refresh_from_db()
        self.assertEqual(self.operating_hours.opening_time, time(10, 0))
        self.assertEqual(self.operating_hours.closing_time, time(22, 0))
    
    def test_delete_operating_hours(self):
        """
        Test deleting shop operating hours.
        """
        # Create another operating hours entry to delete
        tuesday_hours = ShopOperatingHours.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            day_of_week=1,  # Tuesday
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            created_by=self.user_id
        )
        
        url = reverse('shop-operating-hours-detail', args=[self.shop.id, tuesday_hours.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the operating hours were deleted from the database
        with self.assertRaises(ShopOperatingHours.DoesNotExist):
            ShopOperatingHours.objects.get(id=tuesday_hours.id)
    
    def test_list_holidays(self):
        """
        Test listing shop holidays.
        """
        url = reverse('shop-holidays-list', args=[self.shop.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "New Year's Day")
        self.assertEqual(response.data[0]['date'], '2024-01-01')
        self.assertEqual(response.data[0]['description'], "Closed for New Year's Day")
    
    def test_create_holiday(self):
        """
        Test creating a shop holiday.
        """
        url = reverse('shop-holidays-list', args=[self.shop.id])
        data = {
            'name': "Christmas",
            'date': '2024-12-25',
            'description': "Closed for Christmas"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Christmas")
        self.assertEqual(response.data['date'], '2024-12-25')
        self.assertEqual(response.data['description'], "Closed for Christmas")
        
        # Check that the holiday was created in the database
        holiday = ShopHoliday.objects.get(shop=self.shop, date='2024-12-25')
        self.assertEqual(holiday.name, "Christmas")
        self.assertEqual(holiday.description, "Closed for Christmas")
        self.assertEqual(holiday.tenant_id, self.tenant_id)
        self.assertEqual(holiday.created_by, self.user_id)
    
    def test_update_holiday(self):
        """
        Test updating a shop holiday.
        """
        url = reverse('shop-holidays-detail', args=[self.shop.id, self.holiday.id])
        data = {
            'name': "New Year's Day 2024",
            'description': "Updated description"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "New Year's Day 2024")
        self.assertEqual(response.data['description'], "Updated description")
        
        # Check that the holiday was updated in the database
        self.holiday.refresh_from_db()
        self.assertEqual(self.holiday.name, "New Year's Day 2024")
        self.assertEqual(self.holiday.description, "Updated description")
    
    def test_delete_holiday(self):
        """
        Test deleting a shop holiday.
        """
        url = reverse('shop-holidays-detail', args=[self.shop.id, self.holiday.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the holiday was deleted from the database
        with self.assertRaises(ShopHoliday.DoesNotExist):
            ShopHoliday.objects.get(id=self.holiday.id)
    
    def test_get_shop_settings(self):
        """
        Test getting shop settings.
        """
        url = reverse('shop-settings', args=[self.shop.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['enable_low_stock_alerts'])
        self.assertEqual(response.data['low_stock_threshold'], 10)
        self.assertTrue(response.data['enable_expiry_alerts'])
        self.assertEqual(response.data['expiry_alert_days'], 30)
        self.assertEqual(response.data['default_tax_rate'], '18.00')
        self.assertTrue(response.data['enable_discounts'])
        self.assertEqual(response.data['max_discount_percentage'], '10.00')
        self.assertTrue(response.data['require_discount_approval'])
        self.assertEqual(response.data['discount_approval_threshold'], '5.00')
        self.assertEqual(response.data['receipt_header'], "Downtown Liquor Store\n123 Main Street\nNew York, NY 10001")
        self.assertEqual(response.data['receipt_footer'], "Thank you for shopping with us!")
        self.assertTrue(response.data['show_tax_on_receipt'])
        self.assertTrue(response.data['enable_cash_management'])
        self.assertTrue(response.data['require_cash_verification'])
    
    def test_update_shop_settings(self):
        """
        Test updating shop settings.
        """
        url = reverse('shop-settings', args=[self.shop.id])
        data = {
            'default_tax_rate': '20.00',
            'max_discount_percentage': '15.00',
            'receipt_header': "Updated Header",
            'receipt_footer': "Updated Footer"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['default_tax_rate'], '20.00')
        self.assertEqual(response.data['max_discount_percentage'], '15.00')
        self.assertEqual(response.data['receipt_header'], "Updated Header")
        self.assertEqual(response.data['receipt_footer'], "Updated Footer")
        
        # Check that the settings were updated in the database
        self.settings.refresh_from_db()
        self.assertEqual(self.settings.default_tax_rate, Decimal('20.00'))
        self.assertEqual(self.settings.max_discount_percentage, Decimal('15.00'))
        self.assertEqual(self.settings.receipt_header, "Updated Header")
        self.assertEqual(self.settings.receipt_footer, "Updated Footer")
    
    def test_create_shop_settings_if_not_exists(self):
        """
        Test that settings are created if they don't exist when updating.
        """
        # Delete existing settings
        self.settings.delete()
        
        url = reverse('shop-settings', args=[self.shop.id])
        data = {
            'default_tax_rate': '20.00',
            'max_discount_percentage': '15.00'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['default_tax_rate'], '20.00')
        self.assertEqual(response.data['max_discount_percentage'], '15.00')
        
        # Check that new settings were created in the database
        settings = ShopSettings.objects.get(shop=self.shop)
        self.assertEqual(settings.default_tax_rate, Decimal('20.00'))
        self.assertEqual(settings.max_discount_percentage, Decimal('15.00'))
        self.assertEqual(settings.tenant_id, self.tenant_id)
        self.assertEqual(settings.created_by, self.user_id)
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to shop endpoints.
        """
        # Create a user without shop permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'cashier',
            'permissions': ['view_shop']  # Only has view permission
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        # Try to create a shop (should fail)
        url = reverse('shop-list')
        data = {
            'name': "Test Shop",
            'code': "TEST001"
        }
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to update a shop (should fail)
        url = reverse('shop-detail', args=[self.shop.id])
        data = {
            'name': "Updated Name"
        }
        response = client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to delete a shop (should fail)
        url = reverse('shop-detail', args=[self.shop.id])
        response = client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # View a shop (should succeed)
        url = reverse('shop-detail', args=[self.shop.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_tenant_isolation(self):
        """
        Test that shops are isolated by tenant.
        """
        # Create a shop for another tenant
        another_tenant_id = uuid.uuid4()
        another_shop = Shop.objects.create(
            tenant_id=another_tenant_id,
            name="Another Tenant's Shop",
            code="ATS001",
            created_by=uuid.uuid4()
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
            'permissions': ['view_shop', 'add_shop', 'change_shop', 'delete_shop']
        })
        
        # Set up client with the other tenant user
        client = APIClient()
        client.force_authenticate(user=other_tenant_user)
        
        # List shops (should only see shops for their tenant)
        url = reverse('shop-list')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Another Tenant's Shop")
        
        # Try to access a shop from a different tenant (should return 404)
        url = reverse('shop-detail', args=[self.shop.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_search_shops(self):
        """
        Test searching for shops.
        """
        url = reverse('shop-list')
        response = self.client.get(url, {'search': 'Downtown'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Downtown Liquor Store")
        
        # Search by code
        response = self.client.get(url, {'search': 'ULS'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Uptown Liquor Store")
        
        # Search with no results
        response = self.client.get(url, {'search': 'Nonexistent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_filter_shops(self):
        """
        Test filtering shops.
        """
        # Filter by is_open
        url = reverse('shop-list')
        response = self.client.get(url, {'is_open': 'true'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Close one shop
        self.shop2.is_open = False
        self.shop2.save()
        
        # Filter by is_open=false
        response = self.client.get(url, {'is_open': 'false'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Uptown Liquor Store")
        
        # Filter by city
        response = self.client.get(url, {'city': 'New York'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_bulk_update_operating_hours(self):
        """
        Test bulk updating operating hours.
        """
        url = reverse('shop-bulk-operating-hours', args=[self.shop.id])
        data = [
            {
                'day_of_week': 0,  # Monday
                'opening_time': '10:00:00',
                'closing_time': '22:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 1,  # Tuesday
                'opening_time': '10:00:00',
                'closing_time': '22:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 2,  # Wednesday
                'opening_time': '10:00:00',
                'closing_time': '22:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 3,  # Thursday
                'opening_time': '10:00:00',
                'closing_time': '22:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 4,  # Friday
                'opening_time': '10:00:00',
                'closing_time': '23:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 5,  # Saturday
                'opening_time': '10:00:00',
                'closing_time': '23:00:00',
                'is_closed': False
            },
            {
                'day_of_week': 6,  # Sunday
                'opening_time': '12:00:00',
                'closing_time': '20:00:00',
                'is_closed': False
            }
        ]
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)
        
        # Check that all operating hours were created/updated in the database
        hours = ShopOperatingHours.objects.filter(shop=self.shop).order_by('day_of_week')
        self.assertEqual(hours.count(), 7)
        
        # Check Monday (should be updated)
        monday = hours.get(day_of_week=0)
        self.assertEqual(monday.opening_time, time(10, 0))
        self.assertEqual(monday.closing_time, time(22, 0))
        
        # Check Sunday (should be created)
        sunday = hours.get(day_of_week=6)
        self.assertEqual(sunday.opening_time, time(12, 0))
        self.assertEqual(sunday.closing_time, time(20, 0))
    
    def test_shop_status_toggle(self):
        """
        Test toggling shop open/closed status.
        """
        url = reverse('shop-toggle-status', args=[self.shop.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_open'])
        
        # Check that the shop status was updated in the database
        self.shop.refresh_from_db()
        self.assertFalse(self.shop.is_open)
        
        # Toggle back to open
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_open'])
        
        # Check that the shop status was updated in the database
        self.shop.refresh_from_db()
        self.assertTrue(self.shop.is_open)