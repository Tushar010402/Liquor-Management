import uuid
from decimal import Decimal
from datetime import date, datetime
from django.test import TestCase
from django.db import IntegrityError
from purchase_service.suppliers.models import (
    Supplier, SupplierContact, SupplierProduct, 
    SupplierPayment, SupplierInvoice, SupplierInvoicePayment
)

class SupplierModelsTest(TestCase):
    """
    Test the supplier models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        
        # Create supplier
        self.supplier = Supplier.objects.create(
            tenant_id=self.tenant_id,
            code="SUP001",
            name="Premium Liquor Distributors",
            legal_name="Premium Liquor Distributors Pvt Ltd",
            supplier_type=Supplier.TYPE_DISTRIBUTOR,
            status=Supplier.STATUS_ACTIVE,
            tax_id="TAX123456789",
            registration_number="REG987654321",
            address="123 Supplier Street",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            country="India",
            phone="022-12345678",
            email="info@premiumliquor.com",
            website="https://www.premiumliquor.com",
            credit_limit=Decimal('100000.00'),
            credit_period=30,
            notes="Premium supplier for high-end liquor brands",
            created_by=self.user_id
        )
        
        # Create supplier contact
        self.supplier_contact = SupplierContact.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            name="John Doe",
            designation="Sales Manager",
            department="Sales",
            phone="022-87654321",
            mobile="9876543210",
            email="john.doe@premiumliquor.com",
            is_primary=True,
            notes="Primary contact for orders",
            created_by=self.user_id
        )
        
        # Create supplier product
        self.supplier_product = SupplierProduct.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            supplier_product_code="PLD-JW-BL",
            supplier_product_name="JW Black Label 750ml",
            unit_price=Decimal('2500.00'),
            minimum_order_quantity=Decimal('6.000'),
            lead_time_days=5,
            is_preferred_supplier=True,
            notes="Premium scotch whisky",
            created_by=self.user_id
        )
        
        # Create supplier payment
        self.supplier_payment = SupplierPayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            payment_number="PAY-2023-001",
            payment_date=date(2023, 6, 15),
            amount=Decimal('50000.00'),
            payment_method=SupplierPayment.METHOD_BANK_TRANSFER,
            reference_number="BANK-REF-12345",
            status=SupplierPayment.STATUS_COMPLETED,
            notes="Payment for May 2023 invoices",
            created_by=self.user_id
        )
        
        # Create supplier invoice
        self.supplier_invoice = SupplierInvoice.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            invoice_number="INV-2023-001",
            invoice_date=date(2023, 6, 1),
            due_date=date(2023, 7, 1),
            subtotal=Decimal('42372.88'),
            tax_amount=Decimal('7627.12'),
            total_amount=Decimal('50000.00'),
            amount_paid=Decimal('50000.00'),
            balance_due=Decimal('0.00'),
            status=SupplierInvoice.STATUS_PAID,
            notes="Invoice for May 2023 orders",
            created_by=self.user_id
        )
        
        # Create supplier invoice payment
        self.invoice_payment = SupplierInvoicePayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier_payment=self.supplier_payment,
            supplier_invoice=self.supplier_invoice,
            amount=Decimal('50000.00'),
            notes="Full payment",
            created_by=self.user_id
        )
    
    def test_supplier_creation(self):
        """
        Test Supplier creation.
        """
        self.assertEqual(self.supplier.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier.code, "SUP001")
        self.assertEqual(self.supplier.name, "Premium Liquor Distributors")
        self.assertEqual(self.supplier.legal_name, "Premium Liquor Distributors Pvt Ltd")
        self.assertEqual(self.supplier.supplier_type, Supplier.TYPE_DISTRIBUTOR)
        self.assertEqual(self.supplier.status, Supplier.STATUS_ACTIVE)
        self.assertEqual(self.supplier.tax_id, "TAX123456789")
        self.assertEqual(self.supplier.registration_number, "REG987654321")
        self.assertEqual(self.supplier.address, "123 Supplier Street")
        self.assertEqual(self.supplier.city, "Mumbai")
        self.assertEqual(self.supplier.state, "Maharashtra")
        self.assertEqual(self.supplier.postal_code, "400001")
        self.assertEqual(self.supplier.country, "India")
        self.assertEqual(self.supplier.phone, "022-12345678")
        self.assertEqual(self.supplier.email, "info@premiumliquor.com")
        self.assertEqual(self.supplier.website, "https://www.premiumliquor.com")
        self.assertEqual(self.supplier.credit_limit, Decimal('100000.00'))
        self.assertEqual(self.supplier.credit_period, 30)
        self.assertEqual(self.supplier.notes, "Premium supplier for high-end liquor brands")
        self.assertEqual(self.supplier.created_by, self.user_id)
    
    def test_supplier_str(self):
        """
        Test Supplier string representation.
        """
        expected_str = "SUP001 - Premium Liquor Distributors"
        self.assertEqual(str(self.supplier), expected_str)
    
    def test_supplier_unique_code(self):
        """
        Test that supplier code must be unique.
        """
        # Try to create another supplier with the same code
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(
                tenant_id=self.tenant_id,
                code="SUP001",  # Same code as existing supplier
                name="Another Supplier",
                created_by=self.user_id
            )
    
    def test_supplier_contact_creation(self):
        """
        Test SupplierContact creation.
        """
        self.assertEqual(self.supplier_contact.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_contact.supplier, self.supplier)
        self.assertEqual(self.supplier_contact.name, "John Doe")
        self.assertEqual(self.supplier_contact.designation, "Sales Manager")
        self.assertEqual(self.supplier_contact.department, "Sales")
        self.assertEqual(self.supplier_contact.phone, "022-87654321")
        self.assertEqual(self.supplier_contact.mobile, "9876543210")
        self.assertEqual(self.supplier_contact.email, "john.doe@premiumliquor.com")
        self.assertTrue(self.supplier_contact.is_primary)
        self.assertEqual(self.supplier_contact.notes, "Primary contact for orders")
        self.assertEqual(self.supplier_contact.created_by, self.user_id)
    
    def test_supplier_contact_str(self):
        """
        Test SupplierContact string representation.
        """
        expected_str = "Premium Liquor Distributors - John Doe"
        self.assertEqual(str(self.supplier_contact), expected_str)
    
    def test_supplier_product_creation(self):
        """
        Test SupplierProduct creation.
        """
        self.assertEqual(self.supplier_product.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_product.shop_id, self.shop_id)
        self.assertEqual(self.supplier_product.supplier, self.supplier)
        self.assertEqual(self.supplier_product.product_id, self.product_id)
        self.assertEqual(self.supplier_product.product_name, "Johnnie Walker Black Label")
        self.assertEqual(self.supplier_product.product_code, "JW-BL")
        self.assertEqual(self.supplier_product.supplier_product_code, "PLD-JW-BL")
        self.assertEqual(self.supplier_product.supplier_product_name, "JW Black Label 750ml")
        self.assertEqual(self.supplier_product.unit_price, Decimal('2500.00'))
        self.assertEqual(self.supplier_product.minimum_order_quantity, Decimal('6.000'))
        self.assertEqual(self.supplier_product.lead_time_days, 5)
        self.assertTrue(self.supplier_product.is_preferred_supplier)
        self.assertEqual(self.supplier_product.notes, "Premium scotch whisky")
        self.assertEqual(self.supplier_product.created_by, self.user_id)
    
    def test_supplier_product_str(self):
        """
        Test SupplierProduct string representation.
        """
        expected_str = "Premium Liquor Distributors - Johnnie Walker Black Label"
        self.assertEqual(str(self.supplier_product), expected_str)
    
    def test_supplier_product_unique_constraint(self):
        """
        Test that supplier product must be unique per supplier, product, and shop.
        """
        # Try to create another supplier product with the same supplier, product, and shop
        with self.assertRaises(IntegrityError):
            SupplierProduct.objects.create(
                tenant_id=self.tenant_id,
                shop_id=self.shop_id,
                supplier=self.supplier,
                product_id=self.product_id,  # Same product ID
                product_name="Johnnie Walker Black Label",
                product_code="JW-BL",
                unit_price=Decimal('2600.00'),
                created_by=self.user_id
            )
        
        # Create a supplier product with the same supplier and product but different shop (should work)
        another_shop_id = uuid.uuid4()
        another_supplier_product = SupplierProduct.objects.create(
            tenant_id=self.tenant_id,
            shop_id=another_shop_id,  # Different shop
            supplier=self.supplier,
            product_id=self.product_id,
            product_name="Johnnie Walker Black Label",
            product_code="JW-BL",
            unit_price=Decimal('2600.00'),
            created_by=self.user_id
        )
        self.assertEqual(another_supplier_product.shop_id, another_shop_id)
    
    def test_supplier_payment_creation(self):
        """
        Test SupplierPayment creation.
        """
        self.assertEqual(self.supplier_payment.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_payment.shop_id, self.shop_id)
        self.assertEqual(self.supplier_payment.supplier, self.supplier)
        self.assertEqual(self.supplier_payment.payment_number, "PAY-2023-001")
        self.assertEqual(self.supplier_payment.payment_date, date(2023, 6, 15))
        self.assertEqual(self.supplier_payment.amount, Decimal('50000.00'))
        self.assertEqual(self.supplier_payment.payment_method, SupplierPayment.METHOD_BANK_TRANSFER)
        self.assertEqual(self.supplier_payment.reference_number, "BANK-REF-12345")
        self.assertEqual(self.supplier_payment.status, SupplierPayment.STATUS_COMPLETED)
        self.assertEqual(self.supplier_payment.notes, "Payment for May 2023 invoices")
        self.assertEqual(self.supplier_payment.created_by, self.user_id)
    
    def test_supplier_payment_str(self):
        """
        Test SupplierPayment string representation.
        """
        expected_str = "PAY-2023-001 - Premium Liquor Distributors - 50000.00"
        self.assertEqual(str(self.supplier_payment), expected_str)
    
    def test_supplier_payment_unique_number(self):
        """
        Test that supplier payment number must be unique.
        """
        # Try to create another supplier payment with the same payment number
        with self.assertRaises(IntegrityError):
            SupplierPayment.objects.create(
                tenant_id=self.tenant_id,
                shop_id=self.shop_id,
                supplier=self.supplier,
                payment_number="PAY-2023-001",  # Same payment number
                payment_date=date(2023, 6, 16),
                amount=Decimal('25000.00'),
                payment_method=SupplierPayment.METHOD_CASH,
                created_by=self.user_id
            )
    
    def test_supplier_invoice_creation(self):
        """
        Test SupplierInvoice creation.
        """
        self.assertEqual(self.supplier_invoice.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_invoice.shop_id, self.shop_id)
        self.assertEqual(self.supplier_invoice.supplier, self.supplier)
        self.assertEqual(self.supplier_invoice.invoice_number, "INV-2023-001")
        self.assertEqual(self.supplier_invoice.invoice_date, date(2023, 6, 1))
        self.assertEqual(self.supplier_invoice.due_date, date(2023, 7, 1))
        self.assertEqual(self.supplier_invoice.subtotal, Decimal('42372.88'))
        self.assertEqual(self.supplier_invoice.tax_amount, Decimal('7627.12'))
        self.assertEqual(self.supplier_invoice.total_amount, Decimal('50000.00'))
        self.assertEqual(self.supplier_invoice.amount_paid, Decimal('50000.00'))
        self.assertEqual(self.supplier_invoice.balance_due, Decimal('0.00'))
        self.assertEqual(self.supplier_invoice.status, SupplierInvoice.STATUS_PAID)
        self.assertEqual(self.supplier_invoice.notes, "Invoice for May 2023 orders")
        self.assertEqual(self.supplier_invoice.created_by, self.user_id)
    
    def test_supplier_invoice_str(self):
        """
        Test SupplierInvoice string representation.
        """
        expected_str = "INV-2023-001 - Premium Liquor Distributors - 50000.00"
        self.assertEqual(str(self.supplier_invoice), expected_str)
    
    def test_supplier_invoice_unique_constraint(self):
        """
        Test that supplier invoice must be unique per supplier and invoice number.
        """
        # Try to create another supplier invoice with the same supplier and invoice number
        with self.assertRaises(IntegrityError):
            SupplierInvoice.objects.create(
                tenant_id=self.tenant_id,
                shop_id=self.shop_id,
                supplier=self.supplier,
                invoice_number="INV-2023-001",  # Same invoice number
                invoice_date=date(2023, 6, 2),
                due_date=date(2023, 7, 2),
                subtotal=Decimal('25000.00'),
                total_amount=Decimal('25000.00'),
                balance_due=Decimal('25000.00'),
                created_by=self.user_id
            )
    
    def test_supplier_invoice_payment_creation(self):
        """
        Test SupplierInvoicePayment creation.
        """
        self.assertEqual(self.invoice_payment.tenant_id, self.tenant_id)
        self.assertEqual(self.invoice_payment.shop_id, self.shop_id)
        self.assertEqual(self.invoice_payment.supplier_payment, self.supplier_payment)
        self.assertEqual(self.invoice_payment.supplier_invoice, self.supplier_invoice)
        self.assertEqual(self.invoice_payment.amount, Decimal('50000.00'))
        self.assertEqual(self.invoice_payment.notes, "Full payment")
        self.assertEqual(self.invoice_payment.created_by, self.user_id)
    
    def test_supplier_invoice_payment_str(self):
        """
        Test SupplierInvoicePayment string representation.
        """
        expected_str = "PAY-2023-001 - INV-2023-001 - 50000.00"
        self.assertEqual(str(self.invoice_payment), expected_str)
    
    def test_supplier_invoice_payment_unique_constraint(self):
        """
        Test that supplier invoice payment must be unique per payment and invoice.
        """
        # Try to create another supplier invoice payment with the same payment and invoice
        with self.assertRaises(IntegrityError):
            SupplierInvoicePayment.objects.create(
                tenant_id=self.tenant_id,
                shop_id=self.shop_id,
                supplier_payment=self.supplier_payment,
                supplier_invoice=self.supplier_invoice,  # Same invoice
                amount=Decimal('10000.00'),
                created_by=self.user_id
            )
    
    def test_supplier_relationships(self):
        """
        Test relationships between Supplier and related models.
        """
        # Test contacts relationship
        self.assertEqual(self.supplier.contacts.count(), 1)
        self.assertEqual(self.supplier.contacts.first(), self.supplier_contact)
        
        # Test products relationship
        self.assertEqual(self.supplier.products.count(), 1)
        self.assertEqual(self.supplier.products.first(), self.supplier_product)
        
        # Test payments relationship
        self.assertEqual(self.supplier.payments.count(), 1)
        self.assertEqual(self.supplier.payments.first(), self.supplier_payment)
        
        # Test invoices relationship
        self.assertEqual(self.supplier.invoices.count(), 1)
        self.assertEqual(self.supplier.invoices.first(), self.supplier_invoice)
    
    def test_supplier_payment_relationships(self):
        """
        Test relationships between SupplierPayment and related models.
        """
        # Test invoice_payments relationship
        self.assertEqual(self.supplier_payment.invoice_payments.count(), 1)
        self.assertEqual(self.supplier_payment.invoice_payments.first(), self.invoice_payment)
    
    def test_supplier_invoice_relationships(self):
        """
        Test relationships between SupplierInvoice and related models.
        """
        # Test payments relationship
        self.assertEqual(self.supplier_invoice.payments.count(), 1)
        self.assertEqual(self.supplier_invoice.payments.first(), self.invoice_payment)
    
    def test_update_supplier(self):
        """
        Test updating a supplier.
        """
        # Update supplier
        self.supplier.name = "Premium Liquor Distributors Ltd"
        self.supplier.credit_limit = Decimal('150000.00')
        self.supplier.status = Supplier.STATUS_INACTIVE
        self.supplier.save()
        
        # Refresh from database
        self.supplier.refresh_from_db()
        
        # Check that the supplier was updated
        self.assertEqual(self.supplier.name, "Premium Liquor Distributors Ltd")
        self.assertEqual(self.supplier.credit_limit, Decimal('150000.00'))
        self.assertEqual(self.supplier.status, Supplier.STATUS_INACTIVE)
    
    def test_update_supplier_product(self):
        """
        Test updating a supplier product.
        """
        # Update supplier product
        self.supplier_product.unit_price = Decimal('2600.00')
        self.supplier_product.minimum_order_quantity = Decimal('12.000')
        self.supplier_product.save()
        
        # Refresh from database
        self.supplier_product.refresh_from_db()
        
        # Check that the supplier product was updated
        self.assertEqual(self.supplier_product.unit_price, Decimal('2600.00'))
        self.assertEqual(self.supplier_product.minimum_order_quantity, Decimal('12.000'))
    
    def test_update_supplier_invoice_status(self):
        """
        Test updating a supplier invoice status.
        """
        # Create a new invoice with pending status
        pending_invoice = SupplierInvoice.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            invoice_number="INV-2023-002",
            invoice_date=date(2023, 7, 1),
            due_date=date(2023, 8, 1),
            subtotal=Decimal('25000.00'),
            total_amount=Decimal('25000.00'),
            balance_due=Decimal('25000.00'),
            status=SupplierInvoice.STATUS_PENDING,
            created_by=self.user_id
        )
        
        # Update invoice to verified status
        pending_invoice.status = SupplierInvoice.STATUS_VERIFIED
        pending_invoice.verified_by = self.user_id
        pending_invoice.verified_at = datetime.now()
        pending_invoice.save()
        
        # Refresh from database
        pending_invoice.refresh_from_db()
        
        # Check that the invoice status was updated
        self.assertEqual(pending_invoice.status, SupplierInvoice.STATUS_VERIFIED)
        self.assertEqual(pending_invoice.verified_by, self.user_id)
        self.assertIsNotNone(pending_invoice.verified_at)
        
        # Create a payment for the invoice
        payment = SupplierPayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            payment_number="PAY-2023-002",
            payment_date=date(2023, 7, 15),
            amount=Decimal('15000.00'),
            payment_method=SupplierPayment.METHOD_BANK_TRANSFER,
            status=SupplierPayment.STATUS_COMPLETED,
            created_by=self.user_id
        )
        
        # Create invoice payment
        invoice_payment = SupplierInvoicePayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier_payment=payment,
            supplier_invoice=pending_invoice,
            amount=Decimal('15000.00'),
            created_by=self.user_id
        )
        
        # Update invoice to partially paid status
        pending_invoice.status = SupplierInvoice.STATUS_PARTIALLY_PAID
        pending_invoice.amount_paid = Decimal('15000.00')
        pending_invoice.balance_due = Decimal('10000.00')
        pending_invoice.save()
        
        # Refresh from database
        pending_invoice.refresh_from_db()
        
        # Check that the invoice was updated
        self.assertEqual(pending_invoice.status, SupplierInvoice.STATUS_PARTIALLY_PAID)
        self.assertEqual(pending_invoice.amount_paid, Decimal('15000.00'))
        self.assertEqual(pending_invoice.balance_due, Decimal('10000.00'))
    
    def test_multiple_supplier_contacts(self):
        """
        Test creating multiple contacts for a supplier.
        """
        # Create another contact for the supplier
        secondary_contact = SupplierContact.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            name="Jane Smith",
            designation="Accounts Manager",
            department="Accounts",
            phone="022-12345678",
            mobile="9876543211",
            email="jane.smith@premiumliquor.com",
            is_primary=False,
            notes="Contact for payment queries",
            created_by=self.user_id
        )
        
        # Check that both contacts exist
        self.assertEqual(self.supplier.contacts.count(), 2)
        
        # Check that contacts are ordered by is_primary (descending) and then name
        contacts = list(self.supplier.contacts.all())
        self.assertEqual(contacts[0], self.supplier_contact)  # Primary contact first
        self.assertEqual(contacts[1], secondary_contact)
    
    def test_multiple_supplier_products(self):
        """
        Test creating multiple products for a supplier.
        """
        # Create another product
        another_product_id = uuid.uuid4()
        
        # Create another supplier product
        another_supplier_product = SupplierProduct.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            product_id=another_product_id,
            product_name="Johnnie Walker Blue Label",
            product_code="JW-BL-BLUE",
            supplier_product_code="PLD-JW-BL-BLUE",
            unit_price=Decimal('12000.00'),
            minimum_order_quantity=Decimal('2.000'),
            is_preferred_supplier=True,
            created_by=self.user_id
        )
        
        # Check that both products exist
        self.assertEqual(self.supplier.products.count(), 2)
        
        # Check that products are ordered by product_name
        products = list(self.supplier.products.all())
        self.assertEqual(products[0].product_name, "Johnnie Walker Black Label")
        self.assertEqual(products[1].product_name, "Johnnie Walker Blue Label")