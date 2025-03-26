import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from suppliers.models import (
    Supplier, SupplierContact, SupplierBankAccount,
    SupplierDocument, SupplierProduct
)
from products.models import (
    Category, Brand, Product, ProductVariant
)
from common.jwt_auth import MicroserviceUser

class SuppliersAPITest(TestCase):
    """
    Test the suppliers API endpoints.
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
            'permissions': ['view_suppliers', 'add_suppliers', 'change_suppliers']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
    
    def test_list_suppliers(self):
        """
        Test listing suppliers.
        """
        url = reverse('supplier-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'United Spirits Ltd')
        self.assertEqual(response.data['results'][0]['code'], 'USL')
    
    def test_filter_suppliers_by_type(self):
        """
        Test filtering suppliers by type.
        """
        url = reverse('supplier-list')
        response = self.client.get(url, {'supplier_type': Supplier.SUPPLIER_TYPE_DISTRIBUTOR})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier_type'], Supplier.SUPPLIER_TYPE_DISTRIBUTOR)
    
    def test_create_supplier(self):
        """
        Test creating a supplier.
        """
        url = reverse('supplier-list')
        data = {
            'name': 'Pernod Ricard',
            'code': 'PR',
            'supplier_type': Supplier.SUPPLIER_TYPE_MANUFACTURER,
            'tax_id': 'GSTIN987654321',
            'registration_number': 'REG987654',
            'address': '456 Park Ave, Mumbai',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'country': 'India',
            'postal_code': '400001',
            'phone': '9876543220',
            'email': 'contact@pernod-ricard.com',
            'website': 'www.pernod-ricard.com',
            'credit_limit': '1500000.00',
            'credit_period': 45,
            'status': Supplier.STATUS_ACTIVE,
            'notes': 'Global spirits manufacturer'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Pernod Ricard')
        self.assertEqual(response.data['code'], 'PR')
        self.assertEqual(response.data['supplier_type'], Supplier.SUPPLIER_TYPE_MANUFACTURER)
        self.assertEqual(response.data['tax_id'], 'GSTIN987654321')
        self.assertEqual(response.data['city'], 'Mumbai')
        self.assertEqual(response.data['credit_limit'], '1500000.00')
        self.assertEqual(response.data['credit_period'], 45)
        
        # Check that the supplier was created in the database
        supplier = Supplier.objects.get(code='PR')
        self.assertEqual(supplier.name, 'Pernod Ricard')
        self.assertEqual(supplier.tenant_id, self.tenant_id)
        self.assertEqual(supplier.created_by, self.user_id)
    
    def test_retrieve_supplier(self):
        """
        Test retrieving a supplier.
        """
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'United Spirits Ltd')
        self.assertEqual(response.data['code'], 'USL')
        self.assertEqual(response.data['supplier_type'], Supplier.SUPPLIER_TYPE_DISTRIBUTOR)
        self.assertEqual(response.data['tax_id'], 'GSTIN123456789')
        self.assertEqual(response.data['registration_number'], 'REG123456')
        self.assertEqual(response.data['address'], '123 Main St, Bangalore')
        self.assertEqual(response.data['city'], 'Bangalore')
        self.assertEqual(response.data['state'], 'Karnataka')
        self.assertEqual(response.data['country'], 'India')
        self.assertEqual(response.data['postal_code'], '560001')
        self.assertEqual(response.data['phone'], '9876543210')
        self.assertEqual(response.data['email'], 'contact@usl.com')
        self.assertEqual(response.data['website'], 'www.unitedspirits.com')
        self.assertEqual(response.data['credit_limit'], '1000000.00')
        self.assertEqual(response.data['credit_period'], 30)
        self.assertEqual(response.data['status'], Supplier.STATUS_ACTIVE)
        self.assertEqual(response.data['notes'], 'Major spirits distributor')
    
    def test_update_supplier(self):
        """
        Test updating a supplier.
        """
        url = reverse('supplier-detail', args=[self.supplier.id])
        data = {
            'credit_limit': '1200000.00',
            'credit_period': 45,
            'notes': 'Updated notes for major spirits distributor'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['credit_limit'], '1200000.00')
        self.assertEqual(response.data['credit_period'], 45)
        self.assertEqual(response.data['notes'], 'Updated notes for major spirits distributor')
        
        # Check that the supplier was updated in the database
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.credit_limit, Decimal('1200000.00'))
        self.assertEqual(self.supplier.credit_period, 45)
        self.assertEqual(self.supplier.notes, 'Updated notes for major spirits distributor')
    
    def test_list_supplier_contacts(self):
        """
        Test listing supplier contacts.
        """
        url = reverse('suppliercontact-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')
        self.assertEqual(response.data['results'][0]['designation'], 'Sales Manager')
    
    def test_filter_supplier_contacts_by_supplier(self):
        """
        Test filtering supplier contacts by supplier.
        """
        url = reverse('suppliercontact-list')
        response = self.client.get(url, {'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier'], str(self.supplier.id))
    
    def test_create_supplier_contact(self):
        """
        Test creating a supplier contact.
        """
        url = reverse('suppliercontact-list')
        data = {
            'supplier': str(self.supplier.id),
            'name': 'Jane Smith',
            'designation': 'Account Manager',
            'phone': '9876543212',
            'email': 'jane.smith@usl.com',
            'is_primary': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['name'], 'Jane Smith')
        self.assertEqual(response.data['designation'], 'Account Manager')
        self.assertEqual(response.data['phone'], '9876543212')
        self.assertEqual(response.data['email'], 'jane.smith@usl.com')
        self.assertFalse(response.data['is_primary'])
        
        # Check that the supplier contact was created in the database
        contact = SupplierContact.objects.get(name='Jane Smith')
        self.assertEqual(contact.supplier, self.supplier)
        self.assertEqual(contact.tenant_id, self.tenant_id)
        self.assertEqual(contact.created_by, self.user_id)
    
    def test_retrieve_supplier_contact(self):
        """
        Test retrieving a supplier contact.
        """
        url = reverse('suppliercontact-detail', args=[self.supplier_contact.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(response.data['designation'], 'Sales Manager')
        self.assertEqual(response.data['phone'], '9876543211')
        self.assertEqual(response.data['email'], 'john.doe@usl.com')
        self.assertTrue(response.data['is_primary'])
    
    def test_update_supplier_contact(self):
        """
        Test updating a supplier contact.
        """
        url = reverse('suppliercontact-detail', args=[self.supplier_contact.id])
        data = {
            'phone': '9876543213',
            'email': 'john.doe.updated@usl.com'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '9876543213')
        self.assertEqual(response.data['email'], 'john.doe.updated@usl.com')
        
        # Check that the supplier contact was updated in the database
        self.supplier_contact.refresh_from_db()
        self.assertEqual(self.supplier_contact.phone, '9876543213')
        self.assertEqual(self.supplier_contact.email, 'john.doe.updated@usl.com')
    
    def test_list_supplier_bank_accounts(self):
        """
        Test listing supplier bank accounts.
        """
        url = reverse('supplierbankaccount-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['bank_name'], 'HDFC Bank')
        self.assertEqual(response.data['results'][0]['account_number'], '12345678901234')
    
    def test_filter_supplier_bank_accounts_by_supplier(self):
        """
        Test filtering supplier bank accounts by supplier.
        """
        url = reverse('supplierbankaccount-list')
        response = self.client.get(url, {'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier'], str(self.supplier.id))
    
    def test_create_supplier_bank_account(self):
        """
        Test creating a supplier bank account.
        """
        url = reverse('supplierbankaccount-list')
        data = {
            'supplier': str(self.supplier.id),
            'bank_name': 'ICICI Bank',
            'account_number': '98765432109876',
            'account_name': 'United Spirits Ltd',
            'branch': 'Electronic City',
            'ifsc_code': 'ICIC0001234',
            'is_primary': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['bank_name'], 'ICICI Bank')
        self.assertEqual(response.data['account_number'], '98765432109876')
        self.assertEqual(response.data['account_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['branch'], 'Electronic City')
        self.assertEqual(response.data['ifsc_code'], 'ICIC0001234')
        self.assertFalse(response.data['is_primary'])
        
        # Check that the supplier bank account was created in the database
        bank_account = SupplierBankAccount.objects.get(account_number='98765432109876')
        self.assertEqual(bank_account.supplier, self.supplier)
        self.assertEqual(bank_account.tenant_id, self.tenant_id)
        self.assertEqual(bank_account.created_by, self.user_id)
    
    def test_retrieve_supplier_bank_account(self):
        """
        Test retrieving a supplier bank account.
        """
        url = reverse('supplierbankaccount-detail', args=[self.supplier_bank_account.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['bank_name'], 'HDFC Bank')
        self.assertEqual(response.data['account_number'], '12345678901234')
        self.assertEqual(response.data['account_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['branch'], 'MG Road')
        self.assertEqual(response.data['ifsc_code'], 'HDFC0001234')
        self.assertTrue(response.data['is_primary'])
    
    def test_update_supplier_bank_account(self):
        """
        Test updating a supplier bank account.
        """
        url = reverse('supplierbankaccount-detail', args=[self.supplier_bank_account.id])
        data = {
            'branch': 'Koramangala',
            'ifsc_code': 'HDFC0005678'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['branch'], 'Koramangala')
        self.assertEqual(response.data['ifsc_code'], 'HDFC0005678')
        
        # Check that the supplier bank account was updated in the database
        self.supplier_bank_account.refresh_from_db()
        self.assertEqual(self.supplier_bank_account.branch, 'Koramangala')
        self.assertEqual(self.supplier_bank_account.ifsc_code, 'HDFC0005678')
    
    def test_list_supplier_documents(self):
        """
        Test listing supplier documents.
        """
        url = reverse('supplierdocument-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['document_type'], SupplierDocument.DOCUMENT_TYPE_LICENSE)
        self.assertEqual(response.data['results'][0]['document_number'], 'LIC123456')
    
    def test_filter_supplier_documents_by_supplier(self):
        """
        Test filtering supplier documents by supplier.
        """
        url = reverse('supplierdocument-list')
        response = self.client.get(url, {'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier'], str(self.supplier.id))
    
    def test_create_supplier_document(self):
        """
        Test creating a supplier document.
        """
        url = reverse('supplierdocument-list')
        data = {
            'supplier': str(self.supplier.id),
            'document_type': SupplierDocument.DOCUMENT_TYPE_AGREEMENT,
            'document_number': 'AGR123456',
            'document_file': 'suppliers/usl_agreement.pdf',
            'issue_date': '2023-01-01',
            'expiry_date': '2024-12-31'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['document_type'], SupplierDocument.DOCUMENT_TYPE_AGREEMENT)
        self.assertEqual(response.data['document_number'], 'AGR123456')
        self.assertEqual(response.data['document_file'], 'suppliers/usl_agreement.pdf')
        self.assertEqual(response.data['issue_date'], '2023-01-01')
        self.assertEqual(response.data['expiry_date'], '2024-12-31')
        
        # Check that the supplier document was created in the database
        document = SupplierDocument.objects.get(document_number='AGR123456')
        self.assertEqual(document.supplier, self.supplier)
        self.assertEqual(document.tenant_id, self.tenant_id)
        self.assertEqual(document.created_by, self.user_id)
    
    def test_retrieve_supplier_document(self):
        """
        Test retrieving a supplier document.
        """
        url = reverse('supplierdocument-detail', args=[self.supplier_document.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['document_type'], SupplierDocument.DOCUMENT_TYPE_LICENSE)
        self.assertEqual(response.data['document_number'], 'LIC123456')
        self.assertEqual(response.data['document_file'], 'suppliers/usl_license.pdf')
        self.assertEqual(response.data['issue_date'], '2023-01-01')
        self.assertEqual(response.data['expiry_date'], '2024-12-31')
    
    def test_update_supplier_document(self):
        """
        Test updating a supplier document.
        """
        url = reverse('supplierdocument-detail', args=[self.supplier_document.id])
        data = {
            'expiry_date': '2025-12-31'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expiry_date'], '2025-12-31')
        
        # Check that the supplier document was updated in the database
        self.supplier_document.refresh_from_db()
        self.assertEqual(self.supplier_document.expiry_date, date(2025, 12, 31))
    
    def test_list_supplier_products(self):
        """
        Test listing supplier products.
        """
        url = reverse('supplierproduct-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier_product_code'], 'USL-JW-BL-750')
        self.assertEqual(response.data['results'][0]['purchase_price'], '2800.00')
    
    def test_filter_supplier_products_by_supplier(self):
        """
        Test filtering supplier products by supplier.
        """
        url = reverse('supplierproduct-list')
        response = self.client.get(url, {'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier'], str(self.supplier.id))
    
    def test_filter_supplier_products_by_product(self):
        """
        Test filtering supplier products by product.
        """
        url = reverse('supplierproduct-list')
        response = self.client.get(url, {'product': self.product.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], str(self.product.id))
    
    def test_create_supplier_product(self):
        """
        Test creating a supplier product.
        """
        # Create a new product and variant for this test
        new_product = Product.objects.create(
            tenant_id=self.tenant_id,
            name="Johnnie Walker Red Label",
            code="JW-RL",
            category=self.category,
            brand=self.brand,
            created_by=self.user_id
        )
        
        new_product_variant = ProductVariant.objects.create(
            tenant_id=self.tenant_id,
            product=new_product,
            name="750ml",
            sku="JW-RL-750",
            price=Decimal('2500.00'),
            cost_price=Decimal('2000.00'),
            created_by=self.user_id
        )
        
        url = reverse('supplierproduct-list')
        data = {
            'supplier': str(self.supplier.id),
            'product': str(new_product.id),
            'product_variant': str(new_product_variant.id),
            'supplier_product_code': 'USL-JW-RL-750',
            'purchase_price': '2000.00',
            'minimum_order_quantity': 6,
            'lead_time': 7,
            'is_preferred': True
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['product'], str(new_product.id))
        self.assertEqual(response.data['product_variant'], str(new_product_variant.id))
        self.assertEqual(response.data['supplier_product_code'], 'USL-JW-RL-750')
        self.assertEqual(response.data['purchase_price'], '2000.00')
        self.assertEqual(response.data['minimum_order_quantity'], 6)
        self.assertEqual(response.data['lead_time'], 7)
        self.assertTrue(response.data['is_preferred'])
        
        # Check that the supplier product was created in the database
        supplier_product = SupplierProduct.objects.get(supplier_product_code='USL-JW-RL-750')
        self.assertEqual(supplier_product.supplier, self.supplier)
        self.assertEqual(supplier_product.product, new_product)
        self.assertEqual(supplier_product.tenant_id, self.tenant_id)
        self.assertEqual(supplier_product.created_by, self.user_id)
    
    def test_retrieve_supplier_product(self):
        """
        Test retrieving a supplier product.
        """
        url = reverse('supplierproduct-detail', args=[self.supplier_product.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['supplier'], str(self.supplier.id))
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['supplier_product_code'], 'USL-JW-BL-750')
        self.assertEqual(response.data['purchase_price'], '2800.00')
        self.assertEqual(response.data['minimum_order_quantity'], 6)
        self.assertEqual(response.data['lead_time'], 7)
        self.assertTrue(response.data['is_preferred'])
    
    def test_update_supplier_product(self):
        """
        Test updating a supplier product.
        """
        url = reverse('supplierproduct-detail', args=[self.supplier_product.id])
        data = {
            'purchase_price': '2900.00',
            'lead_time': 10
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['purchase_price'], '2900.00')
        self.assertEqual(response.data['lead_time'], 10)
        
        # Check that the supplier product was updated in the database
        self.supplier_product.refresh_from_db()
        self.assertEqual(self.supplier_product.purchase_price, Decimal('2900.00'))
        self.assertEqual(self.supplier_product.lead_time, 10)