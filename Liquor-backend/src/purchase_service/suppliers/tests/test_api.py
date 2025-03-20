import uuid
import json
from decimal import Decimal
from datetime import date, datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from common.jwt_auth import MicroserviceUser
from purchase_service.suppliers.models import (
    Supplier, SupplierContact, SupplierProduct, 
    SupplierPayment, SupplierInvoice, SupplierInvoicePayment
)

class SupplierAPITest(TestCase):
    """
    Test the supplier API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_supplier', 'add_supplier', 'change_supplier', 'delete_supplier',
                           'view_suppliercontact', 'add_suppliercontact', 'change_suppliercontact', 'delete_suppliercontact',
                           'view_supplierproduct', 'add_supplierproduct', 'change_supplierproduct', 'delete_supplierproduct',
                           'view_supplierpayment', 'add_supplierpayment', 'change_supplierpayment', 'delete_supplierpayment',
                           'view_supplierinvoice', 'add_supplierinvoice', 'change_supplierinvoice', 'delete_supplierinvoice']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
        
        # Create another supplier
        self.supplier2 = Supplier.objects.create(
            tenant_id=self.tenant_id,
            code="SUP002",
            name="Budget Liquor Wholesalers",
            supplier_type=Supplier.TYPE_WHOLESALER,
            status=Supplier.STATUS_ACTIVE,
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
    
    def test_list_suppliers(self):
        """
        Test listing suppliers.
        """
        url = reverse('supplier-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "Budget Liquor Wholesalers")
        self.assertEqual(response.data['results'][1]['name'], "Premium Liquor Distributors")
    
    def test_retrieve_supplier(self):
        """
        Test retrieving a supplier.
        """
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], "SUP001")
        self.assertEqual(response.data['name'], "Premium Liquor Distributors")
        self.assertEqual(response.data['legal_name'], "Premium Liquor Distributors Pvt Ltd")
        self.assertEqual(response.data['supplier_type'], Supplier.TYPE_DISTRIBUTOR)
        self.assertEqual(response.data['status'], Supplier.STATUS_ACTIVE)
        self.assertEqual(response.data['tax_id'], "TAX123456789")
        self.assertEqual(response.data['registration_number'], "REG987654321")
        self.assertEqual(response.data['address'], "123 Supplier Street")
        self.assertEqual(response.data['city'], "Mumbai")
        self.assertEqual(response.data['state'], "Maharashtra")
        self.assertEqual(response.data['postal_code'], "400001")
        self.assertEqual(response.data['country'], "India")
        self.assertEqual(response.data['phone'], "022-12345678")
        self.assertEqual(response.data['email'], "info@premiumliquor.com")
        self.assertEqual(response.data['website'], "https://www.premiumliquor.com")
        self.assertEqual(response.data['credit_limit'], '100000.00')
        self.assertEqual(response.data['credit_period'], 30)
        self.assertEqual(response.data['notes'], "Premium supplier for high-end liquor brands")
    
    def test_create_supplier(self):
        """
        Test creating a supplier.
        """
        url = reverse('supplier-list')
        data = {
            'code': "SUP003",
            'name': "Imported Spirits Inc",
            'legal_name': "Imported Spirits Incorporated",
            'supplier_type': Supplier.TYPE_IMPORTER,
            'status': Supplier.STATUS_ACTIVE,
            'tax_id': "TAX987654321",
            'registration_number': "REG123456789",
            'address': "456 Import Avenue",
            'city': "Delhi",
            'state': "Delhi",
            'postal_code': "110001",
            'country': "India",
            'phone': "011-12345678",
            'email': "info@importedspirits.com",
            'website': "https://www.importedspirits.com",
            'credit_limit': '200000.00',
            'credit_period': 45,
            'notes': "Importer of premium international spirits"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['code'], "SUP003")
        self.assertEqual(response.data['name'], "Imported Spirits Inc")
        
        # Check that the supplier was created in the database
        supplier = Supplier.objects.get(code="SUP003")
        self.assertEqual(supplier.name, "Imported Spirits Inc")
        self.assertEqual(supplier.tenant_id, self.tenant_id)
        self.assertEqual(supplier.created_by, self.user_id)
    
    def test_update_supplier(self):
        """
        Test updating a supplier.
        """
        url = reverse('supplier-detail', args=[self.supplier.id])
        data = {
            'name': "Premium Liquor Distributors Ltd",
            'credit_limit': '150000.00',
            'credit_period': 45,
            'notes': "Updated notes"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Premium Liquor Distributors Ltd")
        self.assertEqual(response.data['credit_limit'], '150000.00')
        self.assertEqual(response.data['credit_period'], 45)
        self.assertEqual(response.data['notes'], "Updated notes")
        
        # Check that the supplier was updated in the database
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, "Premium Liquor Distributors Ltd")
        self.assertEqual(self.supplier.credit_limit, Decimal('150000.00'))
        self.assertEqual(self.supplier.credit_period, 45)
        self.assertEqual(self.supplier.notes, "Updated notes")
    
    def test_delete_supplier(self):
        """
        Test deleting a supplier.
        """
        url = reverse('supplier-detail', args=[self.supplier2.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the supplier was deleted from the database
        with self.assertRaises(Supplier.DoesNotExist):
            Supplier.objects.get(id=self.supplier2.id)
    
    def test_list_supplier_contacts(self):
        """
        Test listing supplier contacts.
        """
        url = reverse('supplier-contacts-list', args=[self.supplier.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "John Doe")
        self.assertEqual(response.data[0]['designation'], "Sales Manager")
        self.assertEqual(response.data[0]['department'], "Sales")
        self.assertEqual(response.data[0]['phone'], "022-87654321")
        self.assertEqual(response.data[0]['mobile'], "9876543210")
        self.assertEqual(response.data[0]['email'], "john.doe@premiumliquor.com")
        self.assertTrue(response.data[0]['is_primary'])
    
    def test_create_supplier_contact(self):
        """
        Test creating a supplier contact.
        """
        url = reverse('supplier-contacts-list', args=[self.supplier.id])
        data = {
            'name': "Jane Smith",
            'designation': "Accounts Manager",
            'department': "Accounts",
            'phone': "022-12345678",
            'mobile': "9876543211",
            'email': "jane.smith@premiumliquor.com",
            'is_primary': False,
            'notes': "Contact for payment queries"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Jane Smith")
        self.assertEqual(response.data['designation'], "Accounts Manager")
        self.assertEqual(response.data['department'], "Accounts")
        
        # Check that the contact was created in the database
        contact = SupplierContact.objects.get(supplier=self.supplier, name="Jane Smith")
        self.assertEqual(contact.designation, "Accounts Manager")
        self.assertEqual(contact.tenant_id, self.tenant_id)
        self.assertEqual(contact.created_by, self.user_id)
    
    def test_update_supplier_contact(self):
        """
        Test updating a supplier contact.
        """
        url = reverse('supplier-contacts-detail', args=[self.supplier.id, self.supplier_contact.id])
        data = {
            'designation': "Senior Sales Manager",
            'mobile': "9876543212",
            'notes': "Updated notes"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['designation'], "Senior Sales Manager")
        self.assertEqual(response.data['mobile'], "9876543212")
        self.assertEqual(response.data['notes'], "Updated notes")
        
        # Check that the contact was updated in the database
        self.supplier_contact.refresh_from_db()
        self.assertEqual(self.supplier_contact.designation, "Senior Sales Manager")
        self.assertEqual(self.supplier_contact.mobile, "9876543212")
        self.assertEqual(self.supplier_contact.notes, "Updated notes")
    
    def test_delete_supplier_contact(self):
        """
        Test deleting a supplier contact.
        """
        # Create another contact to delete
        contact = SupplierContact.objects.create(
            tenant_id=self.tenant_id,
            supplier=self.supplier,
            name="Jane Smith",
            designation="Accounts Manager",
            department="Accounts",
            is_primary=False,
            created_by=self.user_id
        )
        
        url = reverse('supplier-contacts-detail', args=[self.supplier.id, contact.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the contact was deleted from the database
        with self.assertRaises(SupplierContact.DoesNotExist):
            SupplierContact.objects.get(id=contact.id)
    
    def test_list_supplier_products(self):
        """
        Test listing supplier products.
        """
        url = reverse('supplier-products-list')
        response = self.client.get(url, {'shop_id': str(self.shop_id)})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product_name'], "Johnnie Walker Black Label")
        self.assertEqual(response.data['results'][0]['product_code'], "JW-BL")
        self.assertEqual(response.data['results'][0]['supplier_product_code'], "PLD-JW-BL")
        self.assertEqual(response.data['results'][0]['unit_price'], '2500.00')
        self.assertEqual(response.data['results'][0]['minimum_order_quantity'], '6.000')
        self.assertEqual(response.data['results'][0]['lead_time_days'], 5)
        self.assertTrue(response.data['results'][0]['is_preferred_supplier'])
    
    def test_create_supplier_product(self):
        """
        Test creating a supplier product.
        """
        url = reverse('supplier-products-list')
        data = {
            'shop_id': str(self.shop_id),
            'supplier': self.supplier.id,
            'product_id': str(uuid.uuid4()),
            'product_name': "Johnnie Walker Blue Label",
            'product_code': "JW-BL-BLUE",
            'supplier_product_code': "PLD-JW-BL-BLUE",
            'supplier_product_name': "JW Blue Label 750ml",
            'unit_price': '12000.00',
            'minimum_order_quantity': '2.000',
            'lead_time_days': 7,
            'is_preferred_supplier': True,
            'notes': "Premium scotch whisky - Blue Label"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_name'], "Johnnie Walker Blue Label")
        self.assertEqual(response.data['product_code'], "JW-BL-BLUE")
        self.assertEqual(response.data['supplier_product_code'], "PLD-JW-BL-BLUE")
        self.assertEqual(response.data['unit_price'], '12000.00')
        
        # Check that the product was created in the database
        product = SupplierProduct.objects.get(product_code="JW-BL-BLUE")
        self.assertEqual(product.product_name, "Johnnie Walker Blue Label")
        self.assertEqual(product.tenant_id, self.tenant_id)
        self.assertEqual(product.shop_id, self.shop_id)
        self.assertEqual(product.created_by, self.user_id)
    
    def test_update_supplier_product(self):
        """
        Test updating a supplier product.
        """
        url = reverse('supplier-products-detail', args=[self.supplier_product.id])
        data = {
            'unit_price': '2600.00',
            'minimum_order_quantity': '12.000',
            'lead_time_days': 7,
            'notes': "Updated notes"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unit_price'], '2600.00')
        self.assertEqual(response.data['minimum_order_quantity'], '12.000')
        self.assertEqual(response.data['lead_time_days'], 7)
        self.assertEqual(response.data['notes'], "Updated notes")
        
        # Check that the product was updated in the database
        self.supplier_product.refresh_from_db()
        self.assertEqual(self.supplier_product.unit_price, Decimal('2600.00'))
        self.assertEqual(self.supplier_product.minimum_order_quantity, Decimal('12.000'))
        self.assertEqual(self.supplier_product.lead_time_days, 7)
        self.assertEqual(self.supplier_product.notes, "Updated notes")
    
    def test_delete_supplier_product(self):
        """
        Test deleting a supplier product.
        """
        url = reverse('supplier-products-detail', args=[self.supplier_product.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the product was deleted from the database
        with self.assertRaises(SupplierProduct.DoesNotExist):
            SupplierProduct.objects.get(id=self.supplier_product.id)
    
    def test_list_supplier_payments(self):
        """
        Test listing supplier payments.
        """
        url = reverse('supplier-payments-list')
        response = self.client.get(url, {'shop_id': str(self.shop_id)})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['payment_number'], "PAY-2023-001")
        self.assertEqual(response.data['results'][0]['payment_date'], "2023-06-15")
        self.assertEqual(response.data['results'][0]['amount'], '50000.00')
        self.assertEqual(response.data['results'][0]['payment_method'], SupplierPayment.METHOD_BANK_TRANSFER)
        self.assertEqual(response.data['results'][0]['reference_number'], "BANK-REF-12345")
        self.assertEqual(response.data['results'][0]['status'], SupplierPayment.STATUS_COMPLETED)
    
    def test_create_supplier_payment(self):
        """
        Test creating a supplier payment.
        """
        url = reverse('supplier-payments-list')
        data = {
            'shop_id': str(self.shop_id),
            'supplier': self.supplier.id,
            'payment_number': "PAY-2023-002",
            'payment_date': "2023-07-15",
            'amount': '25000.00',
            'payment_method': SupplierPayment.METHOD_CHEQUE,
            'reference_number': "CHQ-12345",
            'cheque_number': "123456",
            'status': SupplierPayment.STATUS_PENDING,
            'notes': "Payment for June 2023 invoices"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['payment_number'], "PAY-2023-002")
        self.assertEqual(response.data['payment_date'], "2023-07-15")
        self.assertEqual(response.data['amount'], '25000.00')
        self.assertEqual(response.data['payment_method'], SupplierPayment.METHOD_CHEQUE)
        self.assertEqual(response.data['reference_number'], "CHQ-12345")
        self.assertEqual(response.data['cheque_number'], "123456")
        self.assertEqual(response.data['status'], SupplierPayment.STATUS_PENDING)
        
        # Check that the payment was created in the database
        payment = SupplierPayment.objects.get(payment_number="PAY-2023-002")
        self.assertEqual(payment.amount, Decimal('25000.00'))
        self.assertEqual(payment.tenant_id, self.tenant_id)
        self.assertEqual(payment.shop_id, self.shop_id)
        self.assertEqual(payment.created_by, self.user_id)
    
    def test_update_supplier_payment(self):
        """
        Test updating a supplier payment.
        """
        url = reverse('supplier-payments-detail', args=[self.supplier_payment.id])
        data = {
            'status': SupplierPayment.STATUS_COMPLETED,
            'notes': "Updated notes"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], SupplierPayment.STATUS_COMPLETED)
        self.assertEqual(response.data['notes'], "Updated notes")
        
        # Check that the payment was updated in the database
        self.supplier_payment.refresh_from_db()
        self.assertEqual(self.supplier_payment.status, SupplierPayment.STATUS_COMPLETED)
        self.assertEqual(self.supplier_payment.notes, "Updated notes")
    
    def test_delete_supplier_payment(self):
        """
        Test deleting a supplier payment.
        """
        # Create a new payment to delete
        payment = SupplierPayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            payment_number="PAY-2023-003",
            payment_date=date(2023, 8, 15),
            amount=Decimal('10000.00'),
            payment_method=SupplierPayment.METHOD_CASH,
            status=SupplierPayment.STATUS_PENDING,
            created_by=self.user_id
        )
        
        url = reverse('supplier-payments-detail', args=[payment.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the payment was deleted from the database
        with self.assertRaises(SupplierPayment.DoesNotExist):
            SupplierPayment.objects.get(id=payment.id)
    
    def test_list_supplier_invoices(self):
        """
        Test listing supplier invoices.
        """
        url = reverse('supplier-invoices-list')
        response = self.client.get(url, {'shop_id': str(self.shop_id)})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_number'], "INV-2023-001")
        self.assertEqual(response.data['results'][0]['invoice_date'], "2023-06-01")
        self.assertEqual(response.data['results'][0]['due_date'], "2023-07-01")
        self.assertEqual(response.data['results'][0]['subtotal'], '42372.88')
        self.assertEqual(response.data['results'][0]['tax_amount'], '7627.12')
        self.assertEqual(response.data['results'][0]['total_amount'], '50000.00')
        self.assertEqual(response.data['results'][0]['amount_paid'], '50000.00')
        self.assertEqual(response.data['results'][0]['balance_due'], '0.00')
        self.assertEqual(response.data['results'][0]['status'], SupplierInvoice.STATUS_PAID)
    
    def test_create_supplier_invoice(self):
        """
        Test creating a supplier invoice.
        """
        url = reverse('supplier-invoices-list')
        data = {
            'shop_id': str(self.shop_id),
            'supplier': self.supplier.id,
            'invoice_number': "INV-2023-002",
            'invoice_date': "2023-07-01",
            'due_date': "2023-08-01",
            'subtotal': '25000.00',
            'tax_amount': '4500.00',
            'total_amount': '29500.00',
            'balance_due': '29500.00',
            'status': SupplierInvoice.STATUS_PENDING,
            'notes': "Invoice for June 2023 orders"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['invoice_number'], "INV-2023-002")
        self.assertEqual(response.data['invoice_date'], "2023-07-01")
        self.assertEqual(response.data['due_date'], "2023-08-01")
        self.assertEqual(response.data['subtotal'], '25000.00')
        self.assertEqual(response.data['tax_amount'], '4500.00')
        self.assertEqual(response.data['total_amount'], '29500.00')
        self.assertEqual(response.data['balance_due'], '29500.00')
        self.assertEqual(response.data['status'], SupplierInvoice.STATUS_PENDING)
        
        # Check that the invoice was created in the database
        invoice = SupplierInvoice.objects.get(invoice_number="INV-2023-002")
        self.assertEqual(invoice.total_amount, Decimal('29500.00'))
        self.assertEqual(invoice.tenant_id, self.tenant_id)
        self.assertEqual(invoice.shop_id, self.shop_id)
        self.assertEqual(invoice.created_by, self.user_id)
    
    def test_update_supplier_invoice(self):
        """
        Test updating a supplier invoice.
        """
        url = reverse('supplier-invoices-detail', args=[self.supplier_invoice.id])
        data = {
            'status': SupplierInvoice.STATUS_PAID,
            'amount_paid': '50000.00',
            'balance_due': '0.00',
            'notes': "Updated notes"
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], SupplierInvoice.STATUS_PAID)
        self.assertEqual(response.data['amount_paid'], '50000.00')
        self.assertEqual(response.data['balance_due'], '0.00')
        self.assertEqual(response.data['notes'], "Updated notes")
        
        # Check that the invoice was updated in the database
        self.supplier_invoice.refresh_from_db()
        self.assertEqual(self.supplier_invoice.status, SupplierInvoice.STATUS_PAID)
        self.assertEqual(self.supplier_invoice.amount_paid, Decimal('50000.00'))
        self.assertEqual(self.supplier_invoice.balance_due, Decimal('0.00'))
        self.assertEqual(self.supplier_invoice.notes, "Updated notes")
    
    def test_delete_supplier_invoice(self):
        """
        Test deleting a supplier invoice.
        """
        # Create a new invoice to delete
        invoice = SupplierInvoice.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            invoice_number="INV-2023-003",
            invoice_date=date(2023, 8, 1),
            due_date=date(2023, 9, 1),
            subtotal=Decimal('10000.00'),
            total_amount=Decimal('10000.00'),
            balance_due=Decimal('10000.00'),
            status=SupplierInvoice.STATUS_PENDING,
            created_by=self.user_id
        )
        
        url = reverse('supplier-invoices-detail', args=[invoice.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the invoice was deleted from the database
        with self.assertRaises(SupplierInvoice.DoesNotExist):
            SupplierInvoice.objects.get(id=invoice.id)
    
    def test_create_invoice_payment(self):
        """
        Test creating an invoice payment.
        """
        # Create a new invoice
        invoice = SupplierInvoice.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            invoice_number="INV-2023-004",
            invoice_date=date(2023, 8, 1),
            due_date=date(2023, 9, 1),
            subtotal=Decimal('20000.00'),
            total_amount=Decimal('20000.00'),
            balance_due=Decimal('20000.00'),
            status=SupplierInvoice.STATUS_PENDING,
            created_by=self.user_id
        )
        
        # Create a new payment
        payment = SupplierPayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            payment_number="PAY-2023-004",
            payment_date=date(2023, 8, 15),
            amount=Decimal('20000.00'),
            payment_method=SupplierPayment.METHOD_BANK_TRANSFER,
            status=SupplierPayment.STATUS_COMPLETED,
            created_by=self.user_id
        )
        
        # Create invoice payment
        url = reverse('supplier-invoice-payments-list')
        data = {
            'shop_id': str(self.shop_id),
            'supplier_payment': payment.id,
            'supplier_invoice': invoice.id,
            'amount': '20000.00',
            'notes': "Full payment for invoice"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['supplier_payment'], payment.id)
        self.assertEqual(response.data['supplier_invoice'], invoice.id)
        self.assertEqual(response.data['amount'], '20000.00')
        self.assertEqual(response.data['notes'], "Full payment for invoice")
        
        # Check that the invoice payment was created in the database
        invoice_payment = SupplierInvoicePayment.objects.get(supplier_payment=payment, supplier_invoice=invoice)
        self.assertEqual(invoice_payment.amount, Decimal('20000.00'))
        self.assertEqual(invoice_payment.tenant_id, self.tenant_id)
        self.assertEqual(invoice_payment.shop_id, self.shop_id)
        self.assertEqual(invoice_payment.created_by, self.user_id)
        
        # Update the invoice status and amounts
        invoice.status = SupplierInvoice.STATUS_PAID
        invoice.amount_paid = Decimal('20000.00')
        invoice.balance_due = Decimal('0.00')
        invoice.save()
        
        # Check that the invoice was updated
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, SupplierInvoice.STATUS_PAID)
        self.assertEqual(invoice.amount_paid, Decimal('20000.00'))
        self.assertEqual(invoice.balance_due, Decimal('0.00'))
    
    def test_search_suppliers(self):
        """
        Test searching for suppliers.
        """
        url = reverse('supplier-list')
        response = self.client.get(url, {'search': 'Premium'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Premium Liquor Distributors")
        
        # Search by code
        response = self.client.get(url, {'search': 'SUP002'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Budget Liquor Wholesalers")
        
        # Search with no results
        response = self.client.get(url, {'search': 'Nonexistent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_filter_suppliers(self):
        """
        Test filtering suppliers.
        """
        url = reverse('supplier-list')
        
        # Filter by supplier_type
        response = self.client.get(url, {'supplier_type': Supplier.TYPE_DISTRIBUTOR})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Premium Liquor Distributors")
        
        # Filter by status
        response = self.client.get(url, {'status': Supplier.STATUS_ACTIVE})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Change status of one supplier
        self.supplier2.status = Supplier.STATUS_INACTIVE
        self.supplier2.save()
        
        # Filter by inactive status
        response = self.client.get(url, {'status': Supplier.STATUS_INACTIVE})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Budget Liquor Wholesalers")
    
    def test_filter_supplier_invoices(self):
        """
        Test filtering supplier invoices.
        """
        # Create another invoice with different status
        SupplierInvoice.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            invoice_number="INV-2023-005",
            invoice_date=date(2023, 8, 1),
            due_date=date(2023, 9, 1),
            subtotal=Decimal('15000.00'),
            total_amount=Decimal('15000.00'),
            balance_due=Decimal('15000.00'),
            status=SupplierInvoice.STATUS_PENDING,
            created_by=self.user_id
        )
        
        url = reverse('supplier-invoices-list')
        
        # Filter by status
        response = self.client.get(url, {'shop_id': str(self.shop_id), 'status': SupplierInvoice.STATUS_PAID})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_number'], "INV-2023-001")
        
        # Filter by supplier
        response = self.client.get(url, {'shop_id': str(self.shop_id), 'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by date range
        response = self.client.get(url, {
            'shop_id': str(self.shop_id),
            'start_date': '2023-08-01',
            'end_date': '2023-08-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_number'], "INV-2023-005")
    
    def test_filter_supplier_payments(self):
        """
        Test filtering supplier payments.
        """
        # Create another payment with different method
        SupplierPayment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            supplier=self.supplier,
            payment_number="PAY-2023-005",
            payment_date=date(2023, 8, 15),
            amount=Decimal('15000.00'),
            payment_method=SupplierPayment.METHOD_CASH,
            status=SupplierPayment.STATUS_COMPLETED,
            created_by=self.user_id
        )
        
        url = reverse('supplier-payments-list')
        
        # Filter by payment_method
        response = self.client.get(url, {'shop_id': str(self.shop_id), 'payment_method': SupplierPayment.METHOD_BANK_TRANSFER})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['payment_number'], "PAY-2023-001")
        
        # Filter by supplier
        response = self.client.get(url, {'shop_id': str(self.shop_id), 'supplier': self.supplier.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Filter by date range
        response = self.client.get(url, {
            'shop_id': str(self.shop_id),
            'start_date': '2023-08-01',
            'end_date': '2023-08-31'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['payment_number'], "PAY-2023-005")
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to supplier endpoints.
        """
        # Create a user without supplier permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'cashier',
            'permissions': ['view_supplier']  # Only has view permission
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        # Try to create a supplier (should fail)
        url = reverse('supplier-list')
        data = {
            'code': "SUP004",
            'name': "Test Supplier"
        }
        response = client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to update a supplier (should fail)
        url = reverse('supplier-detail', args=[self.supplier.id])
        data = {
            'name': "Updated Name"
        }
        response = client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try to delete a supplier (should fail)
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # View a supplier (should succeed)
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_tenant_isolation(self):
        """
        Test that suppliers are isolated by tenant.
        """
        # Create a supplier for another tenant
        another_tenant_id = uuid.uuid4()
        another_supplier = Supplier.objects.create(
            tenant_id=another_tenant_id,
            code="SUP001",  # Same code but different tenant
            name="Another Tenant's Supplier",
            created_by=uuid.uuid4()
        )
        
        # Create a user for the other tenant
        other_tenant_user = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'other@example.com',
            'tenant_id': str(another_tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_supplier', 'add_supplier', 'change_supplier', 'delete_supplier']
        })
        
        # Set up client with the other tenant user
        client = APIClient()
        client.force_authenticate(user=other_tenant_user)
        
        # List suppliers (should only see suppliers for their tenant)
        url = reverse('supplier-list')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Another Tenant's Supplier")
        
        # Try to access a supplier from a different tenant (should return 404)
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)