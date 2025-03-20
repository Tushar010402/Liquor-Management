import uuid
from datetime import date, time
from decimal import Decimal
from django.test import TestCase
from django.db import IntegrityError
from core_service.shops.models import Shop, ShopOperatingHours, ShopHoliday, ShopSettings

class ShopModelsTest(TestCase):
    """
    Test the shop models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.manager_id = uuid.uuid4()
        
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
            latitude=Decimal('40.712776'),
            longitude=Decimal('-74.005974'),
            license_number="LIQ-2023-12345",
            license_expiry=date(2024, 12, 31),
            tax_id="TAX-987654321",
            manager_id=self.manager_id,
            manager_name="John Smith",
            manager_phone="212-555-5678",
            manager_email="john.smith@example.com",
            is_open=True,
            created_by=self.manager_id
        )
        
        # Create shop operating hours
        self.operating_hours = ShopOperatingHours.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            day_of_week=0,  # Monday
            opening_time=time(9, 0),  # 9:00 AM
            closing_time=time(21, 0),  # 9:00 PM
            is_closed=False,
            created_by=self.manager_id
        )
        
        # Create shop holiday
        self.holiday = ShopHoliday.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            name="New Year's Day",
            date=date(2024, 1, 1),
            description="Closed for New Year's Day",
            created_by=self.manager_id
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
            created_by=self.manager_id
        )
    
    def test_shop_creation(self):
        """
        Test Shop creation.
        """
        self.assertEqual(self.shop.tenant_id, self.tenant_id)
        self.assertEqual(self.shop.name, "Downtown Liquor Store")
        self.assertEqual(self.shop.code, "DLS001")
        self.assertEqual(self.shop.address, "123 Main Street")
        self.assertEqual(self.shop.city, "New York")
        self.assertEqual(self.shop.state, "NY")
        self.assertEqual(self.shop.country, "USA")
        self.assertEqual(self.shop.postal_code, "10001")
        self.assertEqual(self.shop.phone, "212-555-1234")
        self.assertEqual(self.shop.email, "downtown@example.com")
        self.assertEqual(self.shop.latitude, Decimal('40.712776'))
        self.assertEqual(self.shop.longitude, Decimal('-74.005974'))
        self.assertEqual(self.shop.license_number, "LIQ-2023-12345")
        self.assertEqual(self.shop.license_expiry, date(2024, 12, 31))
        self.assertEqual(self.shop.tax_id, "TAX-987654321")
        self.assertEqual(self.shop.manager_id, self.manager_id)
        self.assertEqual(self.shop.manager_name, "John Smith")
        self.assertEqual(self.shop.manager_phone, "212-555-5678")
        self.assertEqual(self.shop.manager_email, "john.smith@example.com")
        self.assertTrue(self.shop.is_open)
        self.assertEqual(self.shop.created_by, self.manager_id)
    
    def test_shop_str(self):
        """
        Test Shop string representation.
        """
        expected_str = "Downtown Liquor Store (DLS001)"
        self.assertEqual(str(self.shop), expected_str)
    
    def test_shop_unique_code_per_tenant(self):
        """
        Test that shop code must be unique per tenant.
        """
        # Try to create another shop with the same code for the same tenant
        with self.assertRaises(IntegrityError):
            Shop.objects.create(
                tenant_id=self.tenant_id,
                name="Another Liquor Store",
                code="DLS001",  # Same code as existing shop
                created_by=self.manager_id
            )
        
        # Create a shop with the same code but for a different tenant (should work)
        another_tenant_id = uuid.uuid4()
        another_shop = Shop.objects.create(
            tenant_id=another_tenant_id,
            name="Another Tenant's Liquor Store",
            code="DLS001",  # Same code but different tenant
            created_by=self.manager_id
        )
        self.assertEqual(another_shop.code, "DLS001")
        self.assertEqual(another_shop.tenant_id, another_tenant_id)
    
    def test_operating_hours_creation(self):
        """
        Test ShopOperatingHours creation.
        """
        self.assertEqual(self.operating_hours.tenant_id, self.tenant_id)
        self.assertEqual(self.operating_hours.shop, self.shop)
        self.assertEqual(self.operating_hours.day_of_week, 0)  # Monday
        self.assertEqual(self.operating_hours.opening_time, time(9, 0))
        self.assertEqual(self.operating_hours.closing_time, time(21, 0))
        self.assertFalse(self.operating_hours.is_closed)
        self.assertEqual(self.operating_hours.created_by, self.manager_id)
    
    def test_operating_hours_str(self):
        """
        Test ShopOperatingHours string representation.
        """
        expected_str = f"Downtown Liquor Store (DLS001) - Monday (09:00:00 - 21:00:00)"
        self.assertEqual(str(self.operating_hours), expected_str)
        
        # Test string representation when shop is closed
        closed_hours = ShopOperatingHours.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            day_of_week=6,  # Sunday
            opening_time=time(0, 0),
            closing_time=time(0, 0),
            is_closed=True,
            created_by=self.manager_id
        )
        expected_closed_str = f"Downtown Liquor Store (DLS001) - Sunday (Closed)"
        self.assertEqual(str(closed_hours), expected_closed_str)
    
    def test_operating_hours_unique_day_per_shop(self):
        """
        Test that operating hours must be unique per day per shop.
        """
        # Try to create another operating hours entry for the same day for the same shop
        with self.assertRaises(IntegrityError):
            ShopOperatingHours.objects.create(
                tenant_id=self.tenant_id,
                shop=self.shop,
                day_of_week=0,  # Monday (same as existing)
                opening_time=time(10, 0),
                closing_time=time(22, 0),
                created_by=self.manager_id
            )
    
    def test_holiday_creation(self):
        """
        Test ShopHoliday creation.
        """
        self.assertEqual(self.holiday.tenant_id, self.tenant_id)
        self.assertEqual(self.holiday.shop, self.shop)
        self.assertEqual(self.holiday.name, "New Year's Day")
        self.assertEqual(self.holiday.date, date(2024, 1, 1))
        self.assertEqual(self.holiday.description, "Closed for New Year's Day")
        self.assertEqual(self.holiday.created_by, self.manager_id)
    
    def test_holiday_str(self):
        """
        Test ShopHoliday string representation.
        """
        expected_str = f"Downtown Liquor Store (DLS001) - New Year's Day (2024-01-01)"
        self.assertEqual(str(self.holiday), expected_str)
    
    def test_holiday_unique_date_per_shop(self):
        """
        Test that holiday must be unique per date per shop.
        """
        # Try to create another holiday for the same date for the same shop
        with self.assertRaises(IntegrityError):
            ShopHoliday.objects.create(
                tenant_id=self.tenant_id,
                shop=self.shop,
                name="New Year",  # Different name
                date=date(2024, 1, 1),  # Same date
                created_by=self.manager_id
            )
    
    def test_settings_creation(self):
        """
        Test ShopSettings creation.
        """
        self.assertEqual(self.settings.tenant_id, self.tenant_id)
        self.assertEqual(self.settings.shop, self.shop)
        self.assertTrue(self.settings.enable_low_stock_alerts)
        self.assertEqual(self.settings.low_stock_threshold, 10)
        self.assertTrue(self.settings.enable_expiry_alerts)
        self.assertEqual(self.settings.expiry_alert_days, 30)
        self.assertEqual(self.settings.default_tax_rate, Decimal('18.00'))
        self.assertTrue(self.settings.enable_discounts)
        self.assertEqual(self.settings.max_discount_percentage, Decimal('10.00'))
        self.assertTrue(self.settings.require_discount_approval)
        self.assertEqual(self.settings.discount_approval_threshold, Decimal('5.00'))
        self.assertEqual(self.settings.receipt_header, "Downtown Liquor Store\n123 Main Street\nNew York, NY 10001")
        self.assertEqual(self.settings.receipt_footer, "Thank you for shopping with us!")
        self.assertTrue(self.settings.show_tax_on_receipt)
        self.assertTrue(self.settings.enable_cash_management)
        self.assertTrue(self.settings.require_cash_verification)
        self.assertEqual(self.settings.created_by, self.manager_id)
    
    def test_settings_str(self):
        """
        Test ShopSettings string representation.
        """
        expected_str = "Downtown Liquor Store (DLS001) Settings"
        self.assertEqual(str(self.settings), expected_str)
    
    def test_settings_one_to_one_relationship(self):
        """
        Test that a shop can only have one settings object.
        """
        # Try to create another settings object for the same shop
        with self.assertRaises(IntegrityError):
            ShopSettings.objects.create(
                tenant_id=self.tenant_id,
                shop=self.shop,
                created_by=self.manager_id
            )
    
    def test_shop_relationships(self):
        """
        Test relationships between Shop and related models.
        """
        # Test operating hours relationship
        self.assertEqual(self.shop.operating_hours.count(), 1)
        self.assertEqual(self.shop.operating_hours.first(), self.operating_hours)
        
        # Add more operating hours
        tuesday_hours = ShopOperatingHours.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            day_of_week=1,  # Tuesday
            opening_time=time(9, 0),
            closing_time=time(21, 0),
            created_by=self.manager_id
        )
        self.assertEqual(self.shop.operating_hours.count(), 2)
        
        # Test holidays relationship
        self.assertEqual(self.shop.holidays.count(), 1)
        self.assertEqual(self.shop.holidays.first(), self.holiday)
        
        # Add more holidays
        christmas = ShopHoliday.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            name="Christmas",
            date=date(2024, 12, 25),
            description="Closed for Christmas",
            created_by=self.manager_id
        )
        self.assertEqual(self.shop.holidays.count(), 2)
        
        # Test settings relationship
        self.assertEqual(self.shop.settings, self.settings)
    
    def test_shop_closure(self):
        """
        Test closing a shop.
        """
        # Close the shop
        self.shop.is_open = False
        self.shop.save()
        
        # Refresh from database
        self.shop.refresh_from_db()
        
        # Check that the shop is closed
        self.assertFalse(self.shop.is_open)
    
    def test_update_shop_manager(self):
        """
        Test updating shop manager.
        """
        # Create a new manager
        new_manager_id = uuid.uuid4()
        
        # Update shop manager
        self.shop.manager_id = new_manager_id
        self.shop.manager_name = "Jane Doe"
        self.shop.manager_phone = "212-555-9876"
        self.shop.manager_email = "jane.doe@example.com"
        self.shop.save()
        
        # Refresh from database
        self.shop.refresh_from_db()
        
        # Check that the manager was updated
        self.assertEqual(self.shop.manager_id, new_manager_id)
        self.assertEqual(self.shop.manager_name, "Jane Doe")
        self.assertEqual(self.shop.manager_phone, "212-555-9876")
        self.assertEqual(self.shop.manager_email, "jane.doe@example.com")
    
    def test_update_shop_settings(self):
        """
        Test updating shop settings.
        """
        # Update shop settings
        self.settings.default_tax_rate = Decimal('20.00')
        self.settings.max_discount_percentage = Decimal('15.00')
        self.settings.receipt_header = "Updated Header"
        self.settings.save()
        
        # Refresh from database
        self.settings.refresh_from_db()
        
        # Check that the settings were updated
        self.assertEqual(self.settings.default_tax_rate, Decimal('20.00'))
        self.assertEqual(self.settings.max_discount_percentage, Decimal('15.00'))
        self.assertEqual(self.settings.receipt_header, "Updated Header")