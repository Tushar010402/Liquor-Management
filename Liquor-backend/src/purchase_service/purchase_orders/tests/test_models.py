import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from purchase_orders.models import (
    PurchaseOrder, PurchaseOrderItem, PurchaseOrderAttachment, PurchaseOrderHistory
)

class PurchaseOrderModelsTest(TestCase):
    """
    Test the purchase order models.
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
            delivery_address="123 Main St, Bangalore",
            status=PurchaseOrder.STATUS_DRAFT,
            priority=PurchaseOrder.PRIORITY_MEDIUM,
            subtotal=Decimal('10000.00'),
            tax_amount=Decimal('1800.00'),
            discount_amount=Decimal('500.00'),
            shipping_amount=Decimal('200.00'),
            total_amount=Decimal('11500.00'),
            payment_terms="Net 30",
            shipping_terms="FOB",
            notes="Regular order",
            internal_notes="Process with priority",
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
            received_quantity=Decimal('0.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('1800.00'),
            discount_percentage=Decimal('5.00'),
            discount_amount=Decimal('500.00'),
            total_amount=Decimal('11500.00'),
            notes="Premium whisky"
        )
        
        # Create purchase order attachment
        self.purchase_order_attachment = PurchaseOrderAttachment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            purchase_order=self.purchase_order,
            file="purchase_order_attachments/po-2023-0001.pdf",
            file_name="po-2023-0001.pdf",
            file_type="application/pdf",
            file_size=1024,
            description="Purchase order document",
            uploaded_by=self.user_id
        )
        
        # Create purchase order history
        self.purchase_order_history = PurchaseOrderHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_CREATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Purchase order created"
        )
    
    def test_purchase_order_creation(self):
        """
        Test PurchaseOrder creation.
        """
        self.assertEqual(self.purchase_order.po_number, "PO-2023-0001")
        self.assertEqual(self.purchase_order.po_date, date(2023, 4, 15))
        self.assertEqual(self.purchase_order.supplier_id, self.supplier_id)
        self.assertEqual(self.purchase_order.supplier_name, "United Spirits Ltd")
        self.assertEqual(self.purchase_order.supplier_code, "USL")
        self.assertEqual(self.purchase_order.expected_delivery_date, date(2023, 4, 25))
        self.assertEqual(self.purchase_order.delivery_address, "123 Main St, Bangalore")
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_DRAFT)
        self.assertEqual(self.purchase_order.priority, PurchaseOrder.PRIORITY_MEDIUM)
        self.assertEqual(self.purchase_order.subtotal, Decimal('10000.00'))
        self.assertEqual(self.purchase_order.tax_amount, Decimal('1800.00'))
        self.assertEqual(self.purchase_order.discount_amount, Decimal('500.00'))
        self.assertEqual(self.purchase_order.shipping_amount, Decimal('200.00'))
        self.assertEqual(self.purchase_order.total_amount, Decimal('11500.00'))
        self.assertEqual(self.purchase_order.payment_terms, "Net 30")
        self.assertEqual(self.purchase_order.shipping_terms, "FOB")
        self.assertEqual(self.purchase_order.notes, "Regular order")
        self.assertEqual(self.purchase_order.internal_notes, "Process with priority")
        self.assertEqual(self.purchase_order.created_by, self.user_id)
        self.assertIsNone(self.purchase_order.approved_by)
        self.assertIsNone(self.purchase_order.approved_at)
        self.assertEqual(self.purchase_order.rejection_reason, "")
        self.assertTrue(self.purchase_order.is_synced)
        self.assertEqual(self.purchase_order.sync_id, "")
        self.assertEqual(self.purchase_order.tenant_id, self.tenant_id)
        self.assertEqual(self.purchase_order.shop_id, self.shop_id)
    
    def test_purchase_order_str(self):
        """
        Test PurchaseOrder string representation.
        """
        self.assertEqual(str(self.purchase_order), "PO-2023-0001 - United Spirits Ltd - 11500.00")
    
    def test_purchase_order_item_creation(self):
        """
        Test PurchaseOrderItem creation.
        """
        self.assertEqual(self.purchase_order_item.purchase_order, self.purchase_order)
        self.assertEqual(self.purchase_order_item.product_id, self.product_id)
        self.assertEqual(self.purchase_order_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.purchase_order_item.product_code, "JW-BL")
        self.assertEqual(self.purchase_order_item.product_barcode, "5000267023656")
        self.assertEqual(self.purchase_order_item.variant_id, self.variant_id)
        self.assertEqual(self.purchase_order_item.variant_name, "750ml")
        self.assertEqual(self.purchase_order_item.quantity, Decimal('10.000'))
        self.assertEqual(self.purchase_order_item.received_quantity, Decimal('0.000'))
        self.assertEqual(self.purchase_order_item.unit_price, Decimal('1000.00'))
        self.assertEqual(self.purchase_order_item.tax_rate, Decimal('18.00'))
        self.assertEqual(self.purchase_order_item.tax_amount, Decimal('1800.00'))
        self.assertEqual(self.purchase_order_item.discount_percentage, Decimal('5.00'))
        self.assertEqual(self.purchase_order_item.discount_amount, Decimal('500.00'))
        self.assertEqual(self.purchase_order_item.total_amount, Decimal('11500.00'))
        self.assertEqual(self.purchase_order_item.notes, "Premium whisky")
        self.assertEqual(self.purchase_order_item.tenant_id, self.tenant_id)
        self.assertEqual(self.purchase_order_item.shop_id, self.shop_id)
    
    def test_purchase_order_item_str(self):
        """
        Test PurchaseOrderItem string representation.
        """
        self.assertEqual(str(self.purchase_order_item), "Johnnie Walker Black Label - 10.000 x 1000.00")
    
    def test_purchase_order_attachment_creation(self):
        """
        Test PurchaseOrderAttachment creation.
        """
        self.assertEqual(self.purchase_order_attachment.purchase_order, self.purchase_order)
        self.assertEqual(self.purchase_order_attachment.file, "purchase_order_attachments/po-2023-0001.pdf")
        self.assertEqual(self.purchase_order_attachment.file_name, "po-2023-0001.pdf")
        self.assertEqual(self.purchase_order_attachment.file_type, "application/pdf")
        self.assertEqual(self.purchase_order_attachment.file_size, 1024)
        self.assertEqual(self.purchase_order_attachment.description, "Purchase order document")
        self.assertEqual(self.purchase_order_attachment.uploaded_by, self.user_id)
        self.assertEqual(self.purchase_order_attachment.tenant_id, self.tenant_id)
        self.assertEqual(self.purchase_order_attachment.shop_id, self.shop_id)
    
    def test_purchase_order_attachment_str(self):
        """
        Test PurchaseOrderAttachment string representation.
        """
        self.assertEqual(str(self.purchase_order_attachment), "PO-2023-0001 - po-2023-0001.pdf")
    
    def test_purchase_order_history_creation(self):
        """
        Test PurchaseOrderHistory creation.
        """
        self.assertEqual(self.purchase_order_history.purchase_order, self.purchase_order)
        self.assertEqual(self.purchase_order_history.action, PurchaseOrderHistory.ACTION_CREATED)
        self.assertIsNotNone(self.purchase_order_history.action_date)
        self.assertEqual(self.purchase_order_history.user_id, self.user_id)
        self.assertEqual(self.purchase_order_history.user_name, "John Doe")
        self.assertEqual(self.purchase_order_history.notes, "Purchase order created")
        self.assertEqual(self.purchase_order_history.tenant_id, self.tenant_id)
        self.assertEqual(self.purchase_order_history.shop_id, self.shop_id)
    
    def test_purchase_order_history_str(self):
        """
        Test PurchaseOrderHistory string representation.
        """
        expected_str = f"PO-2023-0001 - created - {self.purchase_order_history.action_date}"
        self.assertEqual(str(self.purchase_order_history), expected_str)