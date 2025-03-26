import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from products.models import (
    Category, Brand, Product, ProductVariant
)
from stock.models import (
    Stock, StockMovement, StockAdjustment, StockAdjustmentItem,
    StockTransfer, StockTransferItem, Batch
)

class StockModelsTest(TestCase):
    """
    Test the stock models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.shop_id2 = uuid.uuid4()
        
        # Create category
        self.category = Category.objects.create(
            tenant_id=self.tenant_id,
            name="Whisky",
            code="WHSK",
            description="Whisky products",
            created_by=self.user_id
        )
        
        # Create brand
        self.brand = Brand.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker",
            code="JW",
            description="Johnnie Walker whisky",
            country_of_origin="Scotland",
            created_by=self.user_id
        )
        
        # Create product
        self.product = Product.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker Black Label",
            code="JW-BL",
            description="Johnnie Walker Black Label whisky",
            category=self.category,
            brand=self.brand,
            barcode="5000267023656",
            is_active=True,
            is_returnable=True,
            min_stock=10,
            max_stock=100,
            reorder_level=20,
            created_by=self.user_id
        )
        
        # Create product variant
        self.product_variant = ProductVariant.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            name="750ml",
            sku="JW-BL-750",
            barcode="5000267023656",
            price=Decimal('3500.00'),
            cost_price=Decimal('2800.00'),
            mrp=Decimal('3800.00'),
            discount_price=Decimal('3500.00'),
            weight=750,
            weight_unit="ml",
            is_active=True,
            created_by=self.user_id
        )
        
        # Create batch
        self.batch = Batch.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            product_variant=self.product_variant,
            batch_number="BL-2023-001",
            manufacturing_date=date(2023, 1, 1),
            expiry_date=date(2025, 1, 1),
            cost_price=Decimal('2800.00'),
            mrp=Decimal('3800.00'),
            created_by=self.user_id
        )
        
        # Create stock
        self.stock = Stock.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=50,
            available_quantity=50,
            created_by=self.user_id
        )
        
        # Create stock movement
        self.stock_movement = StockMovement.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=50,
            movement_type=StockMovement.MOVEMENT_TYPE_IN,
            reference_type=StockMovement.REFERENCE_TYPE_PURCHASE,
            reference_id=uuid.uuid4(),
            notes="Initial stock",
            created_by=self.user_id
        )
        
        # Create stock adjustment
        self.stock_adjustment = StockAdjustment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            adjustment_number="ADJ-2023-001",
            adjustment_date=date(2023, 4, 15),
            adjustment_type=StockAdjustment.ADJUSTMENT_TYPE_LOSS,
            status=StockAdjustment.STATUS_PENDING,
            notes="Breakage adjustment",
            created_by=self.user_id
        )
        
        # Create stock adjustment item
        self.stock_adjustment_item = StockAdjustmentItem.objects.create(
            tenant_id=self.tenant_id,
            adjustment=self.stock_adjustment,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            current_quantity=50,
            adjusted_quantity=45,
            adjustment_quantity=5,
            reason="Breakage",
            created_by=self.user_id
        )
        
        # Create stock transfer
        self.stock_transfer = StockTransfer.objects.create(
            tenant_id=self.tenant_id,
            transfer_number="TRF-2023-001",
            transfer_date=date(2023, 4, 20),
            from_shop_id=self.shop_id,
            to_shop_id=self.shop_id2,
            status=StockTransfer.STATUS_PENDING,
            notes="Transfer to new shop",
            created_by=self.user_id
        )
        
        # Create stock transfer item
        self.stock_transfer_item = StockTransferItem.objects.create(
            tenant_id=self.tenant_id,
            transfer=self.stock_transfer,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=10,
            created_by=self.user_id
        )
    
    def test_batch_creation(self):
        """
        Test Batch creation.
        """
        self.assertEqual(self.batch.product, self.product)
        self.assertEqual(self.batch.product_variant, self.product_variant)
        self.assertEqual(self.batch.batch_number, "BL-2023-001")
        self.assertEqual(self.batch.manufacturing_date, date(2023, 1, 1))
        self.assertEqual(self.batch.expiry_date, date(2025, 1, 1))
        self.assertEqual(self.batch.cost_price, Decimal('2800.00'))
        self.assertEqual(self.batch.mrp, Decimal('3800.00'))
        self.assertEqual(self.batch.tenant_id, self.tenant_id)
        self.assertEqual(self.batch.created_by, self.user_id)
        self.assertTrue(self.batch.is_active)
    
    def test_batch_str(self):
        """
        Test Batch string representation.
        """
        self.assertEqual(str(self.batch), "BL-2023-001 - Johnnie Walker Black Label (750ml)")
    
    def test_stock_creation(self):
        """
        Test Stock creation.
        """
        self.assertEqual(self.stock.shop_id, self.shop_id)
        self.assertEqual(self.stock.product, self.product)
        self.assertEqual(self.stock.product_variant, self.product_variant)
        self.assertEqual(self.stock.batch, self.batch)
        self.assertEqual(self.stock.quantity, 50)
        self.assertEqual(self.stock.available_quantity, 50)
        self.assertEqual(self.stock.tenant_id, self.tenant_id)
        self.assertEqual(self.stock.created_by, self.user_id)
        self.assertTrue(self.stock.is_active)
    
    def test_stock_str(self):
        """
        Test Stock string representation.
        """
        self.assertEqual(str(self.stock), "Johnnie Walker Black Label (750ml) - 50 units")
    
    def test_stock_movement_creation(self):
        """
        Test StockMovement creation.
        """
        self.assertEqual(self.stock_movement.shop_id, self.shop_id)
        self.assertEqual(self.stock_movement.product, self.product)
        self.assertEqual(self.stock_movement.product_variant, self.product_variant)
        self.assertEqual(self.stock_movement.batch, self.batch)
        self.assertEqual(self.stock_movement.quantity, 50)
        self.assertEqual(self.stock_movement.movement_type, StockMovement.MOVEMENT_TYPE_IN)
        self.assertEqual(self.stock_movement.reference_type, StockMovement.REFERENCE_TYPE_PURCHASE)
        self.assertIsNotNone(self.stock_movement.reference_id)
        self.assertEqual(self.stock_movement.notes, "Initial stock")
        self.assertEqual(self.stock_movement.tenant_id, self.tenant_id)
        self.assertEqual(self.stock_movement.created_by, self.user_id)
    
    def test_stock_movement_str(self):
        """
        Test StockMovement string representation.
        """
        self.assertEqual(str(self.stock_movement), "IN: Johnnie Walker Black Label (750ml) - 50 units")
    
    def test_stock_adjustment_creation(self):
        """
        Test StockAdjustment creation.
        """
        self.assertEqual(self.stock_adjustment.shop_id, self.shop_id)
        self.assertEqual(self.stock_adjustment.adjustment_number, "ADJ-2023-001")
        self.assertEqual(self.stock_adjustment.adjustment_date, date(2023, 4, 15))
        self.assertEqual(self.stock_adjustment.adjustment_type, StockAdjustment.ADJUSTMENT_TYPE_LOSS)
        self.assertEqual(self.stock_adjustment.status, StockAdjustment.STATUS_PENDING)
        self.assertEqual(self.stock_adjustment.notes, "Breakage adjustment")
        self.assertEqual(self.stock_adjustment.tenant_id, self.tenant_id)
        self.assertEqual(self.stock_adjustment.created_by, self.user_id)
        self.assertIsNone(self.stock_adjustment.approved_by)
        self.assertIsNone(self.stock_adjustment.approved_at)
        self.assertTrue(self.stock_adjustment.is_active)
    
    def test_stock_adjustment_str(self):
        """
        Test StockAdjustment string representation.
        """
        self.assertEqual(str(self.stock_adjustment), "ADJ-2023-001 - Loss")
    
    def test_stock_adjustment_item_creation(self):
        """
        Test StockAdjustmentItem creation.
        """
        self.assertEqual(self.stock_adjustment_item.adjustment, self.stock_adjustment)
        self.assertEqual(self.stock_adjustment_item.product, self.product)
        self.assertEqual(self.stock_adjustment_item.product_variant, self.product_variant)
        self.assertEqual(self.stock_adjustment_item.batch, self.batch)
        self.assertEqual(self.stock_adjustment_item.current_quantity, 50)
        self.assertEqual(self.stock_adjustment_item.adjusted_quantity, 45)
        self.assertEqual(self.stock_adjustment_item.adjustment_quantity, 5)
        self.assertEqual(self.stock_adjustment_item.reason, "Breakage")
        self.assertEqual(self.stock_adjustment_item.tenant_id, self.tenant_id)
        self.assertEqual(self.stock_adjustment_item.created_by, self.user_id)
    
    def test_stock_adjustment_item_str(self):
        """
        Test StockAdjustmentItem string representation.
        """
        self.assertEqual(str(self.stock_adjustment_item), "Johnnie Walker Black Label (750ml) - 5 units")
    
    def test_stock_transfer_creation(self):
        """
        Test StockTransfer creation.
        """
        self.assertEqual(self.stock_transfer.transfer_number, "TRF-2023-001")
        self.assertEqual(self.stock_transfer.transfer_date, date(2023, 4, 20))
        self.assertEqual(self.stock_transfer.from_shop_id, self.shop_id)
        self.assertEqual(self.stock_transfer.to_shop_id, self.shop_id2)
        self.assertEqual(self.stock_transfer.status, StockTransfer.STATUS_PENDING)
        self.assertEqual(self.stock_transfer.notes, "Transfer to new shop")
        self.assertEqual(self.stock_transfer.tenant_id, self.tenant_id)
        self.assertEqual(self.stock_transfer.created_by, self.user_id)
        self.assertIsNone(self.stock_transfer.approved_by)
        self.assertIsNone(self.stock_transfer.approved_at)
        self.assertIsNone(self.stock_transfer.received_by)
        self.assertIsNone(self.stock_transfer.received_at)
        self.assertTrue(self.stock_transfer.is_active)
    
    def test_stock_transfer_str(self):
        """
        Test StockTransfer string representation.
        """
        self.assertEqual(str(self.stock_transfer), "TRF-2023-001 - Pending")
    
    def test_stock_transfer_item_creation(self):
        """
        Test StockTransferItem creation.
        """
        self.assertEqual(self.stock_transfer_item.transfer, self.stock_transfer)
        self.assertEqual(self.stock_transfer_item.product, self.product)
        self.assertEqual(self.stock_transfer_item.product_variant, self.product_variant)
        self.assertEqual(self.stock_transfer_item.batch, self.batch)
        self.assertEqual(self.stock_transfer_item.quantity, 10)
        self.assertEqual(self.stock_transfer_item.tenant_id, self.tenant_id)
        self.assertEqual(self.stock_transfer_item.created_by, self.user_id)
    
    def test_stock_transfer_item_str(self):
        """
        Test StockTransferItem string representation.
        """
        self.assertEqual(str(self.stock_transfer_item), "Johnnie Walker Black Label (750ml) - 10 units")