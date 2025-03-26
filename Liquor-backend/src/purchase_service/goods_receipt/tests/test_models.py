import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from goods_receipt.models import (
    GoodsReceipt, GoodsReceiptItem, GoodsReceiptAttachment, 
    GoodsReceiptHistory, QualityCheck, QualityCheckItem
)

class GoodsReceiptModelsTest(TestCase):
    """
    Test the goods receipt models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.supplier_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        self.variant_id = uuid.uuid4()
        
        # Create purchase order
        self.purchase_order = PurchaseOrder.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            po_number="PO-2023-0001",
            po_date=date(2023, 4, 15),
            supplier_id=self.supplier_id,
            supplier_name="United Spirits Ltd",
            supplier_code="USL",
            expected_delivery_date=date(2023, 4, 25),
            status=PurchaseOrder.STATUS_APPROVED,
            subtotal=Decimal('10000.00'),
            tax_amount=Decimal('1800.00'),
            discount_amount=Decimal('500.00'),
            shipping_amount=Decimal('200.00'),
            total_amount=Decimal('11500.00'),
            created_by=self.user_id
        )
        
        # Create purchase order item
        self.purchase_order_item = PurchaseOrderItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            purchase_order=self.purchase_order,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            quantity=Decimal('10.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('1800.00'),
            discount_percentage=Decimal('5.00'),
            discount_amount=Decimal('500.00'),
            total_amount=Decimal('11500.00')
        )
        
        # Create goods receipt
        self.goods_receipt = GoodsReceipt.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            gr_number="GR-2023-0001",
            gr_date=date(2023, 4, 25),
            purchase_order=self.purchase_order,
            po_number="PO-2023-0001",
            supplier_id=self.supplier_id,
            supplier_name="United Spirits Ltd",
            supplier_code="USL",
            delivery_date=date(2023, 4, 25),
            delivery_note_number="DN-2023-0001",
            status=GoodsReceipt.STATUS_PENDING,
            subtotal=Decimal('10000.00'),
            tax_amount=Decimal('1800.00'),
            discount_amount=Decimal('500.00'),
            shipping_amount=Decimal('200.00'),
            total_amount=Decimal('11500.00'),
            notes="Regular delivery",
            internal_notes="Check quality",
            created_by=self.user_id
        )
        
        # Create goods receipt item
        self.goods_receipt_item = GoodsReceiptItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            purchase_order_item=self.purchase_order_item,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            expected_quantity=Decimal('10.000'),
            received_quantity=Decimal('10.000'),
            accepted_quantity=Decimal('9.000'),
            rejected_quantity=Decimal('1.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('1620.00'),
            discount_percentage=Decimal('5.00'),
            discount_amount=Decimal('450.00'),
            total_amount=Decimal('10350.00'),
            batch_number="BL-2023-001",
            expiry_date=date(2025, 4, 25),
            manufacturing_date=date(2023, 1, 15),
            notes="Premium whisky",
            rejection_reason="One bottle damaged"
        )
        
        # Create goods receipt attachment
        self.goods_receipt_attachment = GoodsReceiptAttachment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            file="goods_receipt_attachments/gr-2023-0001.pdf",
            file_name="gr-2023-0001.pdf",
            file_type="application/pdf",
            file_size=1024,
            description="Goods receipt document",
            uploaded_by=self.user_id
        )
        
        # Create goods receipt history
        self.goods_receipt_history = GoodsReceiptHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_CREATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Goods receipt created"
        )
        
        # Create quality check
        self.quality_check = QualityCheck.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            check_number="QC-2023-0001",
            check_date=date(2023, 4, 25),
            status=QualityCheck.STATUS_PARTIALLY_PASSED,
            notes="Quality check performed",
            checked_by=self.user_id
        )
        
        # Create quality check item
        self.quality_check_item = QualityCheckItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            quality_check=self.quality_check,
            goods_receipt_item=self.goods_receipt_item,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            quantity_checked=Decimal('10.000'),
            quantity_passed=Decimal('9.000'),
            quantity_failed=Decimal('1.000'),
            status=QualityCheckItem.STATUS_PARTIALLY_PASSED,
            notes="Quality check performed",
            failure_reason="One bottle damaged"
        )
    
    def test_goods_receipt_creation(self):
        """
        Test GoodsReceipt creation.
        """
        self.assertEqual(self.goods_receipt.gr_number, "GR-2023-0001")
        self.assertEqual(self.goods_receipt.gr_date, date(2023, 4, 25))
        self.assertEqual(self.goods_receipt.purchase_order, self.purchase_order)
        self.assertEqual(self.goods_receipt.po_number, "PO-2023-0001")
        self.assertEqual(self.goods_receipt.supplier_id, self.supplier_id)
        self.assertEqual(self.goods_receipt.supplier_name, "United Spirits Ltd")
        self.assertEqual(self.goods_receipt.supplier_code, "USL")
        self.assertEqual(self.goods_receipt.delivery_date, date(2023, 4, 25))
        self.assertEqual(self.goods_receipt.delivery_note_number, "DN-2023-0001")
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_PENDING)
        self.assertEqual(self.goods_receipt.subtotal, Decimal('10000.00'))
        self.assertEqual(self.goods_receipt.tax_amount, Decimal('1800.00'))
        self.assertEqual(self.goods_receipt.discount_amount, Decimal('500.00'))
        self.assertEqual(self.goods_receipt.shipping_amount, Decimal('200.00'))
        self.assertEqual(self.goods_receipt.total_amount, Decimal('11500.00'))
        self.assertEqual(self.goods_receipt.notes, "Regular delivery")
        self.assertEqual(self.goods_receipt.internal_notes, "Check quality")
        self.assertEqual(self.goods_receipt.created_by, self.user_id)
        self.assertIsNone(self.goods_receipt.approved_by)
        self.assertIsNone(self.goods_receipt.approved_at)
        self.assertEqual(self.goods_receipt.rejection_reason, "")
        self.assertTrue(self.goods_receipt.is_synced)
        self.assertEqual(self.goods_receipt.sync_id, "")
        self.assertEqual(self.goods_receipt.tenant_id, self.tenant_id)
        self.assertEqual(self.goods_receipt.shop_id, self.shop_id)
    
    def test_goods_receipt_str(self):
        """
        Test GoodsReceipt string representation.
        """
        self.assertEqual(str(self.goods_receipt), "GR-2023-0001 - United Spirits Ltd - 11500.00")
    
    def test_goods_receipt_item_creation(self):
        """
        Test GoodsReceiptItem creation.
        """
        self.assertEqual(self.goods_receipt_item.goods_receipt, self.goods_receipt)
        self.assertEqual(self.goods_receipt_item.purchase_order_item, self.purchase_order_item)
        self.assertEqual(self.goods_receipt_item.product_id, self.product_id)
        self.assertEqual(self.goods_receipt_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.goods_receipt_item.product_code, "JW-BL")
        self.assertEqual(self.goods_receipt_item.product_barcode, "5000267023656")
        self.assertEqual(self.goods_receipt_item.variant_id, self.variant_id)
        self.assertEqual(self.goods_receipt_item.variant_name, "750ml")
        self.assertEqual(self.goods_receipt_item.expected_quantity, Decimal('10.000'))
        self.assertEqual(self.goods_receipt_item.received_quantity, Decimal('10.000'))
        self.assertEqual(self.goods_receipt_item.accepted_quantity, Decimal('9.000'))
        self.assertEqual(self.goods_receipt_item.rejected_quantity, Decimal('1.000'))
        self.assertEqual(self.goods_receipt_item.unit_price, Decimal('1000.00'))
        self.assertEqual(self.goods_receipt_item.tax_rate, Decimal('18.00'))
        self.assertEqual(self.goods_receipt_item.tax_amount, Decimal('1620.00'))
        self.assertEqual(self.goods_receipt_item.discount_percentage, Decimal('5.00'))
        self.assertEqual(self.goods_receipt_item.discount_amount, Decimal('450.00'))
        self.assertEqual(self.goods_receipt_item.total_amount, Decimal('10350.00'))
        self.assertEqual(self.goods_receipt_item.batch_number, "BL-2023-001")
        self.assertEqual(self.goods_receipt_item.expiry_date, date(2025, 4, 25))
        self.assertEqual(self.goods_receipt_item.manufacturing_date, date(2023, 1, 15))
        self.assertEqual(self.goods_receipt_item.notes, "Premium whisky")
        self.assertEqual(self.goods_receipt_item.rejection_reason, "One bottle damaged")
        self.assertEqual(self.goods_receipt_item.tenant_id, self.tenant_id)
        self.assertEqual(self.goods_receipt_item.shop_id, self.shop_id)
    
    def test_goods_receipt_item_str(self):
        """
        Test GoodsReceiptItem string representation.
        """
        self.assertEqual(str(self.goods_receipt_item), "Johnnie Walker Black Label - 10.000 x 1000.00")
    
    def test_goods_receipt_attachment_creation(self):
        """
        Test GoodsReceiptAttachment creation.
        """
        self.assertEqual(self.goods_receipt_attachment.goods_receipt, self.goods_receipt)
        self.assertEqual(self.goods_receipt_attachment.file, "goods_receipt_attachments/gr-2023-0001.pdf")
        self.assertEqual(self.goods_receipt_attachment.file_name, "gr-2023-0001.pdf")
        self.assertEqual(self.goods_receipt_attachment.file_type, "application/pdf")
        self.assertEqual(self.goods_receipt_attachment.file_size, 1024)
        self.assertEqual(self.goods_receipt_attachment.description, "Goods receipt document")
        self.assertEqual(self.goods_receipt_attachment.uploaded_by, self.user_id)
        self.assertEqual(self.goods_receipt_attachment.tenant_id, self.tenant_id)
        self.assertEqual(self.goods_receipt_attachment.shop_id, self.shop_id)
    
    def test_goods_receipt_attachment_str(self):
        """
        Test GoodsReceiptAttachment string representation.
        """
        self.assertEqual(str(self.goods_receipt_attachment), "GR-2023-0001 - gr-2023-0001.pdf")
    
    def test_goods_receipt_history_creation(self):
        """
        Test GoodsReceiptHistory creation.
        """
        self.assertEqual(self.goods_receipt_history.goods_receipt, self.goods_receipt)
        self.assertEqual(self.goods_receipt_history.action, GoodsReceiptHistory.ACTION_CREATED)
        self.assertIsNotNone(self.goods_receipt_history.action_date)
        self.assertEqual(self.goods_receipt_history.user_id, self.user_id)
        self.assertEqual(self.goods_receipt_history.user_name, "John Doe")
        self.assertEqual(self.goods_receipt_history.notes, "Goods receipt created")
        self.assertEqual(self.goods_receipt_history.tenant_id, self.tenant_id)
        self.assertEqual(self.goods_receipt_history.shop_id, self.shop_id)
    
    def test_goods_receipt_history_str(self):
        """
        Test GoodsReceiptHistory string representation.
        """
        expected_str = f"GR-2023-0001 - created - {self.goods_receipt_history.action_date}"
        self.assertEqual(str(self.goods_receipt_history), expected_str)
    
    def test_quality_check_creation(self):
        """
        Test QualityCheck creation.
        """
        self.assertEqual(self.quality_check.goods_receipt, self.goods_receipt)
        self.assertEqual(self.quality_check.check_number, "QC-2023-0001")
        self.assertEqual(self.quality_check.check_date, date(2023, 4, 25))
        self.assertEqual(self.quality_check.status, QualityCheck.STATUS_PARTIALLY_PASSED)
        self.assertEqual(self.quality_check.notes, "Quality check performed")
        self.assertEqual(self.quality_check.checked_by, self.user_id)
        self.assertEqual(self.quality_check.tenant_id, self.tenant_id)
        self.assertEqual(self.quality_check.shop_id, self.shop_id)
    
    def test_quality_check_str(self):
        """
        Test QualityCheck string representation.
        """
        self.assertEqual(str(self.quality_check), "QC-2023-0001 - GR-2023-0001 - partially_passed")
    
    def test_quality_check_item_creation(self):
        """
        Test QualityCheckItem creation.
        """
        self.assertEqual(self.quality_check_item.quality_check, self.quality_check)
        self.assertEqual(self.quality_check_item.goods_receipt_item, self.goods_receipt_item)
        self.assertEqual(self.quality_check_item.product_id, self.product_id)
        self.assertEqual(self.quality_check_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.quality_check_item.quantity_checked, Decimal('10.000'))
        self.assertEqual(self.quality_check_item.quantity_passed, Decimal('9.000'))
        self.assertEqual(self.quality_check_item.quantity_failed, Decimal('1.000'))
        self.assertEqual(self.quality_check_item.status, QualityCheckItem.STATUS_PARTIALLY_PASSED)
        self.assertEqual(self.quality_check_item.notes, "Quality check performed")
        self.assertEqual(self.quality_check_item.failure_reason, "One bottle damaged")
        self.assertEqual(self.quality_check_item.tenant_id, self.tenant_id)
        self.assertEqual(self.quality_check_item.shop_id, self.shop_id)
    
    def test_quality_check_item_str(self):
        """
        Test QualityCheckItem string representation.
        """
        self.assertEqual(str(self.quality_check_item), "Johnnie Walker Black Label - 10.000 - partially_passed")