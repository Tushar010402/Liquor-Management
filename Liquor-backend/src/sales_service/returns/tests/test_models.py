import uuid
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from returns.models import Return, ReturnItem, ReturnExchange
from sales.models import Sale, SaleItem

class ReturnModelsTest(TestCase):
    """
    Test the return models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        self.variant_id = uuid.uuid4()
        
        # Create sale
        self.sale = Sale.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            invoice_number="INV-2023-0001",
            invoice_date=timezone.now(),
            customer_name="John Doe",
            customer_phone="1234567890",
            subtotal=Decimal('5000.00'),
            tax_amount=Decimal('900.00'),
            discount_amount=Decimal('500.00'),
            total_amount=Decimal('5400.00'),
            payment_method=Sale.PAYMENT_CASH,
            payment_status=Sale.PAYMENT_STATUS_PAID,
            created_by=self.user_id
        )
        
        # Create sale item
        self.sale_item = SaleItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            sale=self.sale,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            quantity=Decimal('5.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('900.00'),
            discount_percentage=Decimal('10.00'),
            discount_amount=Decimal('500.00'),
            total_amount=Decimal('5400.00'),
            created_by=self.user_id
        )
        
        # Create return
        self.return_transaction = Return.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_number="RET-2023-0001",
            return_date=timezone.now(),
            sale=self.sale,
            original_invoice_number="INV-2023-0001",
            customer_name="John Doe",
            customer_phone="1234567890",
            return_type=Return.TYPE_PARTIAL,
            status=Return.STATUS_DRAFT,
            subtotal=Decimal('2000.00'),
            tax_amount=Decimal('360.00'),
            total_amount=Decimal('2360.00'),
            refund_method=Return.REFUND_CASH,
            reason="Customer dissatisfied with product",
            created_by=self.user_id
        )
        
        # Create return item
        self.return_item = ReturnItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_transaction=self.return_transaction,
            sale_item=self.sale_item,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            quantity=Decimal('2.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('360.00'),
            total_amount=Decimal('2360.00'),
            reason=ReturnItem.REASON_CUSTOMER_DISSATISFIED,
            reason_details="Customer didn't like the taste",
            created_by=self.user_id
        )
        
        # Create return exchange
        self.return_exchange = ReturnExchange.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_transaction=self.return_transaction,
            product_id=uuid.uuid4(),
            product_name="Johnnie Walker Red Label",
            product_code="JW-RL",
            product_barcode="5000267023663",
            variant_id=uuid.uuid4(),
            variant_name="750ml",
            quantity=Decimal('1.000'),
            unit_price=Decimal('800.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('144.00'),
            total_amount=Decimal('944.00'),
            notes="Exchanged for a different product",
            created_by=self.user_id
        )
    
    def test_return_creation(self):
        """
        Test Return creation.
        """
        self.assertEqual(self.return_transaction.tenant_id, self.tenant_id)
        self.assertEqual(self.return_transaction.shop_id, self.shop_id)
        self.assertEqual(self.return_transaction.return_number, "RET-2023-0001")
        self.assertEqual(self.return_transaction.sale, self.sale)
        self.assertEqual(self.return_transaction.original_invoice_number, "INV-2023-0001")
        self.assertEqual(self.return_transaction.customer_name, "John Doe")
        self.assertEqual(self.return_transaction.customer_phone, "1234567890")
        self.assertEqual(self.return_transaction.return_type, Return.TYPE_PARTIAL)
        self.assertEqual(self.return_transaction.status, Return.STATUS_DRAFT)
        self.assertEqual(self.return_transaction.subtotal, Decimal('2000.00'))
        self.assertEqual(self.return_transaction.tax_amount, Decimal('360.00'))
        self.assertEqual(self.return_transaction.total_amount, Decimal('2360.00'))
        self.assertEqual(self.return_transaction.refund_method, Return.REFUND_CASH)
        self.assertEqual(self.return_transaction.reason, "Customer dissatisfied with product")
        self.assertEqual(self.return_transaction.created_by, self.user_id)
        self.assertIsNone(self.return_transaction.approved_by)
        self.assertIsNone(self.return_transaction.approved_at)
        self.assertEqual(self.return_transaction.rejection_reason, "")
        self.assertTrue(self.return_transaction.is_synced)
        self.assertEqual(self.return_transaction.sync_id, "")
    
    def test_return_str(self):
        """
        Test Return string representation.
        """
        expected_str = "RET-2023-0001 - 2360.00"
        self.assertEqual(str(self.return_transaction), expected_str)
    
    def test_return_item_creation(self):
        """
        Test ReturnItem creation.
        """
        self.assertEqual(self.return_item.tenant_id, self.tenant_id)
        self.assertEqual(self.return_item.shop_id, self.shop_id)
        self.assertEqual(self.return_item.return_transaction, self.return_transaction)
        self.assertEqual(self.return_item.sale_item, self.sale_item)
        self.assertEqual(self.return_item.product_id, self.product_id)
        self.assertEqual(self.return_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.return_item.product_code, "JW-BL")
        self.assertEqual(self.return_item.product_barcode, "5000267023656")
        self.assertEqual(self.return_item.variant_id, self.variant_id)
        self.assertEqual(self.return_item.variant_name, "750ml")
        self.assertEqual(self.return_item.quantity, Decimal('2.000'))
        self.assertEqual(self.return_item.unit_price, Decimal('1000.00'))
        self.assertEqual(self.return_item.tax_rate, Decimal('18.00'))
        self.assertEqual(self.return_item.tax_amount, Decimal('360.00'))
        self.assertEqual(self.return_item.total_amount, Decimal('2360.00'))
        self.assertEqual(self.return_item.reason, ReturnItem.REASON_CUSTOMER_DISSATISFIED)
        self.assertEqual(self.return_item.reason_details, "Customer didn't like the taste")
        self.assertEqual(self.return_item.created_by, self.user_id)
    
    def test_return_item_str(self):
        """
        Test ReturnItem string representation.
        """
        expected_str = "Johnnie Walker Black Label - 2.000 x 1000.00"
        self.assertEqual(str(self.return_item), expected_str)
    
    def test_return_exchange_creation(self):
        """
        Test ReturnExchange creation.
        """
        self.assertEqual(self.return_exchange.tenant_id, self.tenant_id)
        self.assertEqual(self.return_exchange.shop_id, self.shop_id)
        self.assertEqual(self.return_exchange.return_transaction, self.return_transaction)
        self.assertEqual(self.return_exchange.product_name, "Johnnie Walker Red Label")
        self.assertEqual(self.return_exchange.product_code, "JW-RL")
        self.assertEqual(self.return_exchange.product_barcode, "5000267023663")
        self.assertEqual(self.return_exchange.variant_name, "750ml")
        self.assertEqual(self.return_exchange.quantity, Decimal('1.000'))
        self.assertEqual(self.return_exchange.unit_price, Decimal('800.00'))
        self.assertEqual(self.return_exchange.tax_rate, Decimal('18.00'))
        self.assertEqual(self.return_exchange.tax_amount, Decimal('144.00'))
        self.assertEqual(self.return_exchange.total_amount, Decimal('944.00'))
        self.assertEqual(self.return_exchange.notes, "Exchanged for a different product")
        self.assertEqual(self.return_exchange.created_by, self.user_id)
    
    def test_return_exchange_str(self):
        """
        Test ReturnExchange string representation.
        """
        expected_str = "Johnnie Walker Red Label - 1.000 x 800.00"
        self.assertEqual(str(self.return_exchange), expected_str)
    
    def test_return_approval(self):
        """
        Test approving a return.
        """
        # Approve the return
        self.return_transaction.status = Return.STATUS_APPROVED
        self.return_transaction.approved_by = self.user_id
        self.return_transaction.approved_at = timezone.now()
        self.return_transaction.save()
        
        # Refresh from database
        self.return_transaction.refresh_from_db()
        
        # Check that the return was approved
        self.assertEqual(self.return_transaction.status, Return.STATUS_APPROVED)
        self.assertEqual(self.return_transaction.approved_by, self.user_id)
        self.assertIsNotNone(self.return_transaction.approved_at)
    
    def test_return_rejection(self):
        """
        Test rejecting a return.
        """
        # Reject the return
        self.return_transaction.status = Return.STATUS_REJECTED
        self.return_transaction.rejection_reason = "Return policy violation"
        self.return_transaction.save()
        
        # Refresh from database
        self.return_transaction.refresh_from_db()
        
        # Check that the return was rejected
        self.assertEqual(self.return_transaction.status, Return.STATUS_REJECTED)
        self.assertEqual(self.return_transaction.rejection_reason, "Return policy violation")
    
    def test_return_completion(self):
        """
        Test completing a return.
        """
        # First approve the return
        self.return_transaction.status = Return.STATUS_APPROVED
        self.return_transaction.approved_by = self.user_id
        self.return_transaction.approved_at = timezone.now()
        self.return_transaction.save()
        
        # Then complete the return
        self.return_transaction.status = Return.STATUS_COMPLETED
        self.return_transaction.refund_reference = "CASH-REF-001"
        self.return_transaction.refund_details = {
            "cashier": "Jane Smith",
            "register": "REG-001",
            "amount_returned": "2360.00"
        }
        self.return_transaction.save()
        
        # Refresh from database
        self.return_transaction.refresh_from_db()
        
        # Check that the return was completed
        self.assertEqual(self.return_transaction.status, Return.STATUS_COMPLETED)
        self.assertEqual(self.return_transaction.refund_reference, "CASH-REF-001")
        self.assertEqual(self.return_transaction.refund_details["cashier"], "Jane Smith")
        self.assertEqual(self.return_transaction.refund_details["register"], "REG-001")
        self.assertEqual(self.return_transaction.refund_details["amount_returned"], "2360.00")
    
    def test_return_cancellation(self):
        """
        Test cancelling a return.
        """
        # Cancel the return
        self.return_transaction.status = Return.STATUS_CANCELLED
        self.return_transaction.notes = "Customer changed their mind"
        self.return_transaction.save()
        
        # Refresh from database
        self.return_transaction.refresh_from_db()
        
        # Check that the return was cancelled
        self.assertEqual(self.return_transaction.status, Return.STATUS_CANCELLED)
        self.assertEqual(self.return_transaction.notes, "Customer changed their mind")
    
    def test_full_return(self):
        """
        Test creating a full return.
        """
        # Create a full return
        full_return = Return.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_number="RET-2023-0002",
            return_date=timezone.now(),
            sale=self.sale,
            original_invoice_number="INV-2023-0001",
            customer_name="John Doe",
            customer_phone="1234567890",
            return_type=Return.TYPE_FULL,
            status=Return.STATUS_DRAFT,
            subtotal=Decimal('5000.00'),
            tax_amount=Decimal('900.00'),
            total_amount=Decimal('5400.00'),
            refund_method=Return.REFUND_CASH,
            reason="Defective product",
            created_by=self.user_id
        )
        
        # Create return item for the full return
        ReturnItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_transaction=full_return,
            sale_item=self.sale_item,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            quantity=Decimal('5.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('900.00'),
            total_amount=Decimal('5400.00'),
            reason=ReturnItem.REASON_DEFECTIVE,
            reason_details="Seal broken",
            created_by=self.user_id
        )
        
        # Check that the full return was created
        self.assertEqual(full_return.return_type, Return.TYPE_FULL)
        self.assertEqual(full_return.total_amount, self.sale.total_amount)
        
        # Check that the return item was created
        return_item = ReturnItem.objects.get(return_transaction=full_return)
        self.assertEqual(return_item.quantity, self.sale_item.quantity)
        self.assertEqual(return_item.total_amount, self.sale_item.total_amount)
    
    def test_exchange_return(self):
        """
        Test creating a return with exchange.
        """
        # Create a return with exchange
        exchange_return = Return.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_number="RET-2023-0003",
            return_date=timezone.now(),
            sale=self.sale,
            original_invoice_number="INV-2023-0001",
            customer_name="John Doe",
            customer_phone="1234567890",
            return_type=Return.TYPE_PARTIAL,
            status=Return.STATUS_DRAFT,
            subtotal=Decimal('3000.00'),
            tax_amount=Decimal('540.00'),
            total_amount=Decimal('3540.00'),
            refund_method=Return.REFUND_EXCHANGE,
            reason="Wrong item",
            created_by=self.user_id
        )
        
        # Create return item for the exchange return
        ReturnItem.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_transaction=exchange_return,
            sale_item=self.sale_item,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            product_barcode="5000267023656",
            variant_id=self.variant_id,
            variant_name="750ml",
            quantity=Decimal('3.000'),
            unit_price=Decimal('1000.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('540.00'),
            total_amount=Decimal('3540.00'),
            reason=ReturnItem.REASON_WRONG_ITEM,
            reason_details="Customer wanted Red Label",
            created_by=self.user_id
        )
        
        # Create exchange items
        ReturnExchange.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_transaction=exchange_return,
            product_id=uuid.uuid4(),
            product_name="Johnnie Walker Red Label",
            product_code="JW-RL",
            product_barcode="5000267023663",
            variant_id=uuid.uuid4(),
            variant_name="750ml",
            quantity=Decimal('3.000'),
            unit_price=Decimal('800.00'),
            tax_rate=Decimal('18.00'),
            tax_amount=Decimal('432.00'),
            total_amount=Decimal('2832.00'),
            notes="Exchanged for Red Label",
            created_by=self.user_id
        )
        
        # Check that the exchange return was created
        self.assertEqual(exchange_return.refund_method, Return.REFUND_EXCHANGE)
        
        # Check that the return item was created
        return_item = ReturnItem.objects.get(return_transaction=exchange_return)
        self.assertEqual(return_item.reason, ReturnItem.REASON_WRONG_ITEM)
        
        # Check that the exchange item was created
        exchange_item = ReturnExchange.objects.get(return_transaction=exchange_return)
        self.assertEqual(exchange_item.product_name, "Johnnie Walker Red Label")
        self.assertEqual(exchange_item.quantity, Decimal('3.000'))
        self.assertEqual(exchange_item.total_amount, Decimal('2832.00'))