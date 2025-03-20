import uuid
from decimal import Decimal
from datetime import date, time, timedelta
from django.test import TestCase
from django.utils import timezone
from shops.models import Shop, ShopSettings, ShopActivity

class ShopModelsTest(TestCase):
    """
    Test the shop models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        # Create shop
        self.shop = Shop.objects.create(
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
            description="Downtown premium liquor store",
            created_by=self.user_id,
            notes="Flagship store"
        )
        
        # Create shop settings
        self.shop_settings = ShopSettings.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
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
            },
            created_by=self.user_id
        )
        
        # Create shop activity
        self.shop_activity = ShopActivity.objects.create(
            tenant_id=self.tenant_id,
            shop=self.shop,
            user_id=self.user_id,
            activity_type="shop_opened",
            description="Shop opened for business",
            ip_address="192.168.1.1",
            metadata={
                'opening_balance': '5000.00',
                'opened_by': 'John Doe'
            },
            created_by=self.user_id
        )
    
    def test_shop_creation(self):
        """
        Test Shop creation.
        """
        self.assertEqual(self.shop.tenant_id, self.tenant_id)
        self.assertEqual(self.shop.name, "Downtown Liquor Store")
        self.assertEqual(self.shop.code, "DLS001")
        self.assertEqual(self.shop.shop_type, Shop.TYPE_RETAIL)
        self.assertEqual(self.shop.status, Shop.STATUS_ACTIVE)
        self.assertEqual(self.shop.address, "123 Main St, Downtown")
        self.assertEqual(self.shop.city, "Metropolis")
        self.assertEqual(self.shop.state, "State")
        self.assertEqual(self.shop.country, "Country")
        self.assertEqual(self.shop.postal_code, "12345")
        self.assertEqual(self.shop.latitude, Decimal('37.123456'))
        self.assertEqual(self.shop.longitude, Decimal('-122.123456'))
        self.assertEqual(self.shop.phone, "1234567890")
        self.assertEqual(self.shop.email, "downtown@example.com")
        self.assertEqual(self.shop.license_number, "LIQ123456")
        self.assertEqual(self.shop.license_type, "Retail Liquor License")
        self.assertEqual(self.shop.license_expiry, date.today() + timedelta(days=365))
        self.assertEqual(self.shop.opening_time, time(9, 0))
        self.assertEqual(self.shop.closing_time, time(21, 0))
        self.assertTrue(self.shop.is_open_on_monday)
        self.assertTrue(self.shop.is_open_on_tuesday)
        self.assertTrue(self.shop.is_open_on_wednesday)
        self.assertTrue(self.shop.is_open_on_thursday)
        self.assertTrue(self.shop.is_open_on_friday)
        self.assertTrue(self.shop.is_open_on_saturday)
        self.assertFalse(self.shop.is_open_on_sunday)
        self.assertEqual(self.shop.description, "Downtown premium liquor store")
        self.assertEqual(self.shop.created_by, self.user_id)
        self.assertEqual(self.shop.notes, "Flagship store")
    
    def test_shop_str(self):
        """
        Test Shop string representation.
        """
        self.assertEqual(str(self.shop), "Downtown Liquor Store (DLS001)")
    
    def test_shop_settings_creation(self):
        """
        Test ShopSettings creation.
        """
        self.assertEqual(self.shop_settings.tenant_id, self.tenant_id)
        self.assertEqual(self.shop_settings.shop, self.shop)
        self.assertTrue(self.shop_settings.enable_low_stock_alerts)
        self.assertEqual(self.shop_settings.low_stock_threshold, 5)
        self.assertTrue(self.shop_settings.enable_expiry_alerts)
        self.assertEqual(self.shop_settings.expiry_alert_days, 45)
        self.assertEqual(self.shop_settings.default_tax_rate, Decimal('18.00'))
        self.assertTrue(self.shop_settings.enable_discounts)
        self.assertEqual(self.shop_settings.max_discount_percentage, Decimal('15.00'))
        self.assertTrue(self.shop_settings.require_discount_approval)
        self.assertEqual(self.shop_settings.discount_approval_threshold, Decimal('7.50'))
        self.assertFalse(self.shop_settings.require_sales_approval)
        self.assertTrue(self.shop_settings.require_stock_adjustment_approval)
        self.assertTrue(self.shop_settings.require_return_approval)
        self.assertEqual(self.shop_settings.receipt_header, "Downtown Liquor Store\n123 Main St, Downtown")
        self.assertEqual(self.shop_settings.receipt_footer, "Thank you for shopping with us!")
        self.assertTrue(self.shop_settings.show_tax_on_receipt)
        self.assertTrue(self.shop_settings.settings_json['enable_loyalty_program'])
        self.assertEqual(self.shop_settings.settings_json['points_per_dollar'], 1)
        self.assertEqual(self.shop_settings.settings_json['redemption_rate'], 0.01)
        self.assertEqual(self.shop_settings.created_by, self.user_id)
    
    def test_shop_settings_str(self):
        """
        Test ShopSettings string representation.
        """
        self.assertEqual(str(self.shop_settings), "Settings for Downtown Liquor Store")
    
    def test_shop_activity_creation(self):
        """
        Test ShopActivity creation.
        """
        self.assertEqual(self.shop_activity.tenant_id, self.tenant_id)
        self.assertEqual(self.shop_activity.shop, self.shop)
        self.assertEqual(self.shop_activity.user_id, self.user_id)
        self.assertEqual(self.shop_activity.activity_type, "shop_opened")
        self.assertEqual(self.shop_activity.description, "Shop opened for business")
        self.assertEqual(self.shop_activity.ip_address, "192.168.1.1")
        self.assertEqual(self.shop_activity.metadata['opening_balance'], '5000.00')
        self.assertEqual(self.shop_activity.metadata['opened_by'], 'John Doe')
        self.assertEqual(self.shop_activity.created_by, self.user_id)
    
    def test_shop_activity_str(self):
        """
        Test ShopActivity string representation.
        """
        expected_str = f"Downtown Liquor Store - shop_opened - {self.shop_activity.created_at}"
        self.assertEqual(str(self.shop_activity), expected_str)