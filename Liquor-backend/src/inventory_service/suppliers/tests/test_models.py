import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from suppliers.models import (
    Supplier, SupplierContact, SupplierBankAccount,
    SupplierDocument, SupplierProduct
)
from products.models import (
    Category, Brand, Product, ProductVariant
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
        self.user_id = uuid.uuid4()
        
        # Create supplier
        self.supplier = Supplier.objects.create(
            tenant_id=self.tenant_id,
            name="United Spirits Ltd",
            code="USL",
            supplier_type=Supplier.SUPPLIER_TYPE_DISTRIBUTOR,
            tax_id="GSTIN123456789",
            registration_number="REG123456",
            address="123 Main St, Bangalore",
            city="Bangalore",
            state="Karnataka",
            country="India",
            postal_code="560001",
            phone="9876543210",
            email="contact@usl.com",
            website="www.unitedspirits.com",
            credit_limit=Decimal('1000000.00'),
            credit_period=30,
            status=Supplier.STATUS_ACTIVE,
            notes="Major spirits distributor",
            created_by=self.user_id
        )
        
        # Create supplier contact
        self.supplier_contact = SupplierContact.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            name="John Doe",
            designation="Sales Manager",
            phone="9876543211",
            email="john.doe@usl.com",
            is_primary=True,
            created_by=self.user_id
        )
        
        # Create supplier bank account
        self.supplier_bank_account = SupplierBankAccount.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            bank_name="HDFC Bank",
            account_number="12345678901234",
            account_name="United Spirits Ltd",
            branch="MG Road",
            ifsc_code="HDFC0001234",
            is_primary=True,
            created_by=self.user_id
        )
        
        # Create supplier document
        self.supplier_document = SupplierDocument.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            document_type=SupplierDocument.DOCUMENT_TYPE_LICENSE,
            document_number="LIC123456",
            document_file="suppliers/usl_license.pdf",
            issue_date=date(2023, 1, 1),
            expiry_date=date(2024, 12, 31),
            created_by=self.user_id
        )
        
        # Create category
        self.category = Category.objects.create(
            tenant_id=self.tenant_id,
            name="Whisky",
            code="WHSK",
            created_by=self.user_id
        )
        
        # Create brand
        self.brand = Brand.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker",
            code="JW",
            created_by=self.user_id
        )
        
        # Create product
        self.product = Product.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker Black Label",
            code="JW-BL",
            category=self.category,
            brand=self.brand,
            created_by=self.user_id
        )
        
        # Create product variant
        self.product_variant = ProductVariant.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            name="750ml",
            sku="JW-BL-750",
            price=Decimal('3500.00'),
            cost_price=Decimal('2800.00'),
            created_by=self.user_id
        )
        
        # Create supplier product
        self.supplier_product = SupplierProduct.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            product=self.product,
            product_variant=self.product_variant,
            supplier_product_code="USL-JW-BL-750",
            purchase_price=Decimal('2800.00'),
            minimum_order_quantity=6,
            lead_time=7,
            is_preferred=True,
            created_by=self.user_id
        )
    
    def test_supplier_creation(self):
        """
        Test Supplier creation.
        """
        self.assertEqual(self.supplier.name, "United Spirits Ltd")
        self.assertEqual(self.supplier.code, "USL")
        self.assertEqual(self.supplier.supplier_type, Supplier.SUPPLIER_TYPE_DISTRIBUTOR)
        self.assertEqual(self.supplier.tax_id, "GSTIN123456789")
        self.assertEqual(self.supplier.registration_number, "REG123456")
        self.assertEqual(self.supplier.address, "123 Main St, Bangalore")
        self.assertEqual(self.supplier.city, "Bangalore")
        self.assertEqual(self.supplier.state, "Karnataka")
        self.assertEqual(self.supplier.country, "India")
        self.assertEqual(self.supplier.postal_code, "560001")
        self.assertEqual(self.supplier.phone, "9876543210")
        self.assertEqual(self.supplier.email, "contact@usl.com")
        self.assertEqual(self.supplier.website, "www.unitedspirits.com")
        self.assertEqual(self.supplier.credit_limit, Decimal('1000000.00'))
        self.assertEqual(self.supplier.credit_period, 30)
        self.assertEqual(self.supplier.status, Supplier.STATUS_ACTIVE)
        self.assertEqual(self.supplier.notes, "Major spirits distributor")
        self.assertEqual(self.supplier.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier.created_by, self.user_id)
        self.assertTrue(self.supplier.is_active)
    
    def test_supplier_str(self):
        """
        Test Supplier string representation.
        """
        self.assertEqual(str(self.supplier), "USL - United Spirits Ltd")
    
    def test_supplier_contact_creation(self):
        """
        Test SupplierContact creation.
        """
        self.assertEqual(self.supplier_contact.supplier, self.supplier)
        self.assertEqual(self.supplier_contact.name, "John Doe")
        self.assertEqual(self.supplier_contact.designation, "Sales Manager")
        self.assertEqual(self.supplier_contact.phone, "9876543211")
        self.assertEqual(self.supplier_contact.email, "john.doe@usl.com")
        self.assertTrue(self.supplier_contact.is_primary)
        self.assertEqual(self.supplier_contact.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_contact.created_by, self.user_id)
        self.assertTrue(self.supplier_contact.is_active)
    
    def test_supplier_contact_str(self):
        """
        Test SupplierContact string representation.
        """
        self.assertEqual(str(self.supplier_contact), "John Doe - Sales Manager")
    
    def test_supplier_bank_account_creation(self):
        """
        Test SupplierBankAccount creation.
        """
        self.assertEqual(self.supplier_bank_account.supplier, self.supplier)
        self.assertEqual(self.supplier_bank_account.bank_name, "HDFC Bank")
        self.assertEqual(self.supplier_bank_account.account_number, "12345678901234")
        self.assertEqual(self.supplier_bank_account.account_name, "United Spirits Ltd")
        self.assertEqual(self.supplier_bank_account.branch, "MG Road")
        self.assertEqual(self.supplier_bank_account.ifsc_code, "HDFC0001234")
        self.assertTrue(self.supplier_bank_account.is_primary)
        self.assertEqual(self.supplier_bank_account.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_bank_account.created_by, self.user_id)
        self.assertTrue(self.supplier_bank_account.is_active)
    
    def test_supplier_bank_account_str(self):
        """
        Test SupplierBankAccount string representation.
        """
        self.assertEqual(str(self.supplier_bank_account), "HDFC Bank - 12345678901234")
    
    def test_supplier_document_creation(self):
        """
        Test SupplierDocument creation.
        """
        self.assertEqual(self.supplier_document.supplier, self.supplier)
        self.assertEqual(self.supplier_document.document_type, SupplierDocument.DOCUMENT_TYPE_LICENSE)
        self.assertEqual(self.supplier_document.document_number, "LIC123456")
        self.assertEqual(self.supplier_document.document_file, "suppliers/usl_license.pdf")
        self.assertEqual(self.supplier_document.issue_date, date(2023, 1, 1))
        self.assertEqual(self.supplier_document.expiry_date, date(2024, 12, 31))
        self.assertEqual(self.supplier_document.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_document.created_by, self.user_id)
        self.assertTrue(self.supplier_document.is_active)
    
    def test_supplier_document_str(self):
        """
        Test SupplierDocument string representation.
        """
        self.assertEqual(str(self.supplier_document), "License - LIC123456")
    
    def test_supplier_product_creation(self):
        """
        Test SupplierProduct creation.
        """
        self.assertEqual(self.supplier_product.supplier, self.supplier)
        self.assertEqual(self.supplier_product.product, self.product)
        self.assertEqual(self.supplier_product.product_variant, self.product_variant)
        self.assertEqual(self.supplier_product.supplier_product_code, "USL-JW-BL-750")
        self.assertEqual(self.supplier_product.purchase_price, Decimal('2800.00'))
        self.assertEqual(self.supplier_product.minimum_order_quantity, 6)
        self.assertEqual(self.supplier_product.lead_time, 7)
        self.assertTrue(self.supplier_product.is_preferred)
        self.assertEqual(self.supplier_product.tenant_id, self.tenant_id)
        self.assertEqual(self.supplier_product.created_by, self.user_id)
        self.assertTrue(self.supplier_product.is_active)
    
    def test_supplier_product_str(self):
        """
        Test SupplierProduct string representation.
        """
        self.assertEqual(str(self.supplier_product), "United Spirits Ltd - Johnnie Walker Black Label (750ml)")