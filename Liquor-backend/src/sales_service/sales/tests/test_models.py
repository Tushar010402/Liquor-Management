import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from sales.models import (
    Sale, SaleItem, SalePayment, SaleReturn, SaleReturnItem,
    Customer, CustomerGroup, CustomerLoyalty, CustomerCredit
)

class SalesModelsTest(TestCase):
    """
    Test the sales models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        self.product_variant_id = uuid.uuid4()
        self.batch_id = uuid.uuid4()
        
        # Create customer group
        self.customer_group = CustomerGroup.objects.create(
            tenant_id=self.tenant_id,
            name="Regular Customers",
            code="REG",
            description="Regular customers with standard discounts",
            discount_percentage=Decimal('5.00'),
            created_by=self.user_id
        )
        
        # Create customer
        self.customer = Customer.objects.create(
            tenant_id=self.tenant_id,
            name="John Smith",
            customer_type=Customer.CUSTOMER_TYPE_INDIVIDUAL,
            customer_group=self.customer_group,
            phone="9876543210",
            email="john.smith@example.com",
            address="123 Main St, City",
            tax_id="TAXPAN123456",
            credit_limit=Decimal('10000.00'),
            status=Customer.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        # Create customer loyalty
        self.customer_loyalty = CustomerLoyalty.objects.create(
            tenant_id=self.tenant_id,
            customer=self.customer,
            loyalty_number="LOY123456",
            points_balance=100,
            tier="Silver",
            created_by=self.user_id
        )
        
        # Create customer credit
        self.customer_credit = CustomerCredit.objects.create(
            tenant_id=self.tenant_id,
            customer=self.customer,
            credit_limit=Decimal('10000.00'),
            credit_used=Decimal('2000.00'),
            credit_available=Decimal('8000.00'),
            created_by=self.user_id
        )
        
        # Create sale
        self.sale = Sale.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            invoice_number="INV-2023-0001",
            invoice_date=date(2023, 4, 15),
            customer=self.customer,
            sale_type=Sale.SALE_TYPE_RETAIL,
            status=Sale.STATUS_COMPLETED,
            subtotal=Decimal('3500.00'),
            discount_amount=Decimal('175.00'),
            tax_amount=Decimal('630.00'),
            total_amount=Decimal('3955.00'),
            paid_amount=Decimal('4000.00'),
            change_amount=Decimal('45.00'),
            notes="Regular sale",
            created_by=self.user_id
        )
        
        # Create sale item
        self.sale_item = SaleItem.objects.create(
            tenant_id=self.tenant_id,
            sale=self.sale,
            product_id=self.product_id,
            product_variant_id=self.product_variant_id,
            batch_id=self.batch_id,
            product_name="Johnnie Walker Black Label",
            variant_name="750ml",
            quantity=1,
            unit_price=Decimal('3500.00'),
            discount_percentage=Decimal('5.00'),
            discount_amount=Decimal('175.00'),
            tax_percentage=Decimal('18.00'),
            tax_amount=Decimal('630.00'),
            subtotal=Decimal('3500.00'),
            total=Decimal('3955.00'),
            created_by=self.user_id
        )
        
        # Create sale payment
        self.sale_payment = SalePayment.objects.create(
            tenant_id=self.tenant_id,
            sale=self.sale,
            payment_method=SalePayment.PAYMENT_METHOD_CASH,
            amount=Decimal('4000.00'),
            reference_number="",
            status=SalePayment.STATUS_COMPLETED,
            created_by=self.user_id
        )
        
        # Create sale return
        self.sale_return = SaleReturn.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            return_number="RET-2023-0001",
            return_date=date(2023, 4, 20),
            sale=self.sale,
            customer=self.customer,
            status=SaleReturn.STATUS_COMPLETED,
            subtotal=Decimal('3500.00'),
            discount_amount=Decimal('175.00'),
            tax_amount=Decimal('630.00'),
            total_amount=Decimal('3955.00'),
            refund_amount=Decimal('3955.00'),
            reason="Customer changed mind",
            notes="Full return",
            created_by=self.user_id
        )
        
        # Create sale return item
        self.sale_return_item = SaleReturnItem.objects.create(
            tenant_id=self.tenant_id,
            sale_return=self.sale_return,
            sale_item=self.sale_item,
            product_id=self.product_id,
            product_variant_id=self.product_variant_id,
            batch_id=self.batch_id,
            product_name="Johnnie Walker Black Label",
            variant_name="750ml",
            quantity=1,
            unit_price=Decimal('3500.00'),
            discount_percentage=Decimal('5.00'),
            discount_amount=Decimal('175.00'),
            tax_percentage=Decimal('18.00'),
            tax_amount=Decimal('630.00'),
            subtotal=Decimal('3500.00'),
            total=Decimal('3955.00'),
            reason="Customer changed mind",
            created_by=self.user_id
        )
    
    def test_customer_group_creation(self):
        """
        Test CustomerGroup creation.
        """
        self.assertEqual(self.customer_group.name, "Regular Customers")
        self.assertEqual(self.customer_group.code, "REG")
        self.assertEqual(self.customer_group.description, "Regular customers with standard discounts")
        self.assertEqual(self.customer_group.discount_percentage, Decimal('5.00'))
        self.assertEqual(self.customer_group.tenant_id, self.tenant_id)
        self.assertEqual(self.customer_group.created_by, self.user_id)
        self.assertTrue(self.customer_group.is_active)
    
    def test_customer_group_str(self):
        """
        Test CustomerGroup string representation.
        """
        self.assertEqual(str(self.customer_group), "REG - Regular Customers")
    
    def test_customer_creation(self):
        """
        Test Customer creation.
        """
        self.assertEqual(self.customer.name, "John Smith")
        self.assertEqual(self.customer.customer_type, Customer.CUSTOMER_TYPE_INDIVIDUAL)
        self.assertEqual(self.customer.customer_group, self.customer_group)
        self.assertEqual(self.customer.phone, "9876543210")
        self.assertEqual(self.customer.email, "john.smith@example.com")
        self.assertEqual(self.customer.address, "123 Main St, City")
        self.assertEqual(self.customer.tax_id, "TAXPAN123456")
        self.assertEqual(self.customer.credit_limit, Decimal('10000.00'))
        self.assertEqual(self.customer.status, Customer.STATUS_ACTIVE)
        self.assertEqual(self.customer.tenant_id, self.tenant_id)
        self.assertEqual(self.customer.created_by, self.user_id)
        self.assertTrue(self.customer.is_active)
    
    def test_customer_str(self):
        """
        Test Customer string representation.
        """
        self.assertEqual(str(self.customer), "John Smith - 9876543210")
    
    def test_customer_loyalty_creation(self):
        """
        Test CustomerLoyalty creation.
        """
        self.assertEqual(self.customer_loyalty.customer, self.customer)
        self.assertEqual(self.customer_loyalty.loyalty_number, "LOY123456")
        self.assertEqual(self.customer_loyalty.points_balance, 100)
        self.assertEqual(self.customer_loyalty.tier, "Silver")
        self.assertEqual(self.customer_loyalty.tenant_id, self.tenant_id)
        self.assertEqual(self.customer_loyalty.created_by, self.user_id)
        self.assertTrue(self.customer_loyalty.is_active)
    
    def test_customer_loyalty_str(self):
        """
        Test CustomerLoyalty string representation.
        """
        self.assertEqual(str(self.customer_loyalty), "John Smith - LOY123456 - 100 points")
    
    def test_customer_credit_creation(self):
        """
        Test CustomerCredit creation.
        """
        self.assertEqual(self.customer_credit.customer, self.customer)
        self.assertEqual(self.customer_credit.credit_limit, Decimal('10000.00'))
        self.assertEqual(self.customer_credit.credit_used, Decimal('2000.00'))
        self.assertEqual(self.customer_credit.credit_available, Decimal('8000.00'))
        self.assertEqual(self.customer_credit.tenant_id, self.tenant_id)
        self.assertEqual(self.customer_credit.created_by, self.user_id)
        self.assertTrue(self.customer_credit.is_active)
    
    def test_customer_credit_str(self):
        """
        Test CustomerCredit string representation.
        """
        self.assertEqual(str(self.customer_credit), "John Smith - Available: 8000.00")
    
    def test_sale_creation(self):
        """
        Test Sale creation.
        """
        self.assertEqual(self.sale.shop_id, self.shop_id)
        self.assertEqual(self.sale.invoice_number, "INV-2023-0001")
        self.assertEqual(self.sale.invoice_date, date(2023, 4, 15))
        self.assertEqual(self.sale.customer, self.customer)
        self.assertEqual(self.sale.sale_type, Sale.SALE_TYPE_RETAIL)
        self.assertEqual(self.sale.status, Sale.STATUS_COMPLETED)
        self.assertEqual(self.sale.subtotal, Decimal('3500.00'))
        self.assertEqual(self.sale.discount_amount, Decimal('175.00'))
        self.assertEqual(self.sale.tax_amount, Decimal('630.00'))
        self.assertEqual(self.sale.total_amount, Decimal('3955.00'))
        self.assertEqual(self.sale.paid_amount, Decimal('4000.00'))
        self.assertEqual(self.sale.change_amount, Decimal('45.00'))
        self.assertEqual(self.sale.notes, "Regular sale")
        self.assertEqual(self.sale.tenant_id, self.tenant_id)
        self.assertEqual(self.sale.created_by, self.user_id)
        self.assertTrue(self.sale.is_active)
    
    def test_sale_str(self):
        """
        Test Sale string representation.
        """
        self.assertEqual(str(self.sale), "INV-2023-0001 - 3955.00")
    
    def test_sale_item_creation(self):
        """
        Test SaleItem creation.
        """
        self.assertEqual(self.sale_item.sale, self.sale)
        self.assertEqual(self.sale_item.product_id, self.product_id)
        self.assertEqual(self.sale_item.product_variant_id, self.product_variant_id)
        self.assertEqual(self.sale_item.batch_id, self.batch_id)
        self.assertEqual(self.sale_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.sale_item.variant_name, "750ml")
        self.assertEqual(self.sale_item.quantity, 1)
        self.assertEqual(self.sale_item.unit_price, Decimal('3500.00'))
        self.assertEqual(self.sale_item.discount_percentage, Decimal('5.00'))
        self.assertEqual(self.sale_item.discount_amount, Decimal('175.00'))
        self.assertEqual(self.sale_item.tax_percentage, Decimal('18.00'))
        self.assertEqual(self.sale_item.tax_amount, Decimal('630.00'))
        self.assertEqual(self.sale_item.subtotal, Decimal('3500.00'))
        self.assertEqual(self.sale_item.total, Decimal('3955.00'))
        self.assertEqual(self.sale_item.tenant_id, self.tenant_id)
        self.assertEqual(self.sale_item.created_by, self.user_id)
    
    def test_sale_item_str(self):
        """
        Test SaleItem string representation.
        """
        self.assertEqual(str(self.sale_item), "Johnnie Walker Black Label (750ml) - 1 x 3500.00")
    
    def test_sale_payment_creation(self):
        """
        Test SalePayment creation.
        """
        self.assertEqual(self.sale_payment.sale, self.sale)
        self.assertEqual(self.sale_payment.payment_method, SalePayment.PAYMENT_METHOD_CASH)
        self.assertEqual(self.sale_payment.amount, Decimal('4000.00'))
        self.assertEqual(self.sale_payment.reference_number, "")
        self.assertEqual(self.sale_payment.status, SalePayment.STATUS_COMPLETED)
        self.assertEqual(self.sale_payment.tenant_id, self.tenant_id)
        self.assertEqual(self.sale_payment.created_by, self.user_id)
    
    def test_sale_payment_str(self):
        """
        Test SalePayment string representation.
        """
        self.assertEqual(str(self.sale_payment), "Cash - 4000.00")
    
    def test_sale_return_creation(self):
        """
        Test SaleReturn creation.
        """
        self.assertEqual(self.sale_return.shop_id, self.shop_id)
        self.assertEqual(self.sale_return.return_number, "RET-2023-0001")
        self.assertEqual(self.sale_return.return_date, date(2023, 4, 20))
        self.assertEqual(self.sale_return.sale, self.sale)
        self.assertEqual(self.sale_return.customer, self.customer)
        self.assertEqual(self.sale_return.status, SaleReturn.STATUS_COMPLETED)
        self.assertEqual(self.sale_return.subtotal, Decimal('3500.00'))
        self.assertEqual(self.sale_return.discount_amount, Decimal('175.00'))
        self.assertEqual(self.sale_return.tax_amount, Decimal('630.00'))
        self.assertEqual(self.sale_return.total_amount, Decimal('3955.00'))
        self.assertEqual(self.sale_return.refund_amount, Decimal('3955.00'))
        self.assertEqual(self.sale_return.reason, "Customer changed mind")
        self.assertEqual(self.sale_return.notes, "Full return")
        self.assertEqual(self.sale_return.tenant_id, self.tenant_id)
        self.assertEqual(self.sale_return.created_by, self.user_id)
        self.assertTrue(self.sale_return.is_active)
    
    def test_sale_return_str(self):
        """
        Test SaleReturn string representation.
        """
        self.assertEqual(str(self.sale_return), "RET-2023-0001 - 3955.00")
    
    def test_sale_return_item_creation(self):
        """
        Test SaleReturnItem creation.
        """
        self.assertEqual(self.sale_return_item.sale_return, self.sale_return)
        self.assertEqual(self.sale_return_item.sale_item, self.sale_item)
        self.assertEqual(self.sale_return_item.product_id, self.product_id)
        self.assertEqual(self.sale_return_item.product_variant_id, self.product_variant_id)
        self.assertEqual(self.sale_return_item.batch_id, self.batch_id)
        self.assertEqual(self.sale_return_item.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.sale_return_item.variant_name, "750ml")
        self.assertEqual(self.sale_return_item.quantity, 1)
        self.assertEqual(self.sale_return_item.unit_price, Decimal('3500.00'))
        self.assertEqual(self.sale_return_item.discount_percentage, Decimal('5.00'))
        self.assertEqual(self.sale_return_item.discount_amount, Decimal('175.00'))
        self.assertEqual(self.sale_return_item.tax_percentage, Decimal('18.00'))
        self.assertEqual(self.sale_return_item.tax_amount, Decimal('630.00'))
        self.assertEqual(self.sale_return_item.subtotal, Decimal('3500.00'))
        self.assertEqual(self.sale_return_item.total, Decimal('3955.00'))
        self.assertEqual(self.sale_return_item.reason, "Customer changed mind")
        self.assertEqual(self.sale_return_item.tenant_id, self.tenant_id)
        self.assertEqual(self.sale_return_item.created_by, self.user_id)
    
    def test_sale_return_item_str(self):
        """
        Test SaleReturnItem string representation.
        """
        self.assertEqual(str(self.sale_return_item), "Johnnie Walker Black Label (750ml) - 1 x 3500.00")