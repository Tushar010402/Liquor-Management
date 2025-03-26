import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from sales.models import (
    Sale, SaleItem, SalePayment, SaleReturn, SaleReturnItem,
    Customer, CustomerGroup, CustomerLoyalty, CustomerCredit
)
from common.jwt_auth import MicroserviceUser

class SalesAPITest(TestCase):
    """
    Test the sales API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        self.product_variant_id = uuid.uuid4()
        self.batch_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_sales', 'add_sales', 'change_sales']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
    
    def test_list_customer_groups(self):
        """
        Test listing customer groups.
        """
        url = reverse('customergroup-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Regular Customers')
        self.assertEqual(response.data['results'][0]['code'], 'REG')
    
    def test_create_customer_group(self):
        """
        Test creating a customer group.
        """
        url = reverse('customergroup-list')
        data = {
            'name': 'VIP Customers',
            'code': 'VIP',
            'description': 'VIP customers with premium discounts',
            'discount_percentage': '10.00'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'VIP Customers')
        self.assertEqual(response.data['code'], 'VIP')
        self.assertEqual(response.data['description'], 'VIP customers with premium discounts')
        self.assertEqual(response.data['discount_percentage'], '10.00')
        
        # Check that the customer group was created in the database
        group = CustomerGroup.objects.get(code='VIP')
        self.assertEqual(group.name, 'VIP Customers')
        self.assertEqual(group.tenant_id, self.tenant_id)
        self.assertEqual(group.created_by, self.user_id)
    
    def test_retrieve_customer_group(self):
        """
        Test retrieving a customer group.
        """
        url = reverse('customergroup-detail', args=[self.customer_group.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Regular Customers')
        self.assertEqual(response.data['code'], 'REG')
        self.assertEqual(response.data['description'], 'Regular customers with standard discounts')
        self.assertEqual(response.data['discount_percentage'], '5.00')
    
    def test_update_customer_group(self):
        """
        Test updating a customer group.
        """
        url = reverse('customergroup-detail', args=[self.customer_group.id])
        data = {
            'discount_percentage': '7.50',
            'description': 'Updated description for regular customers'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['discount_percentage'], '7.50')
        self.assertEqual(response.data['description'], 'Updated description for regular customers')
        
        # Check that the customer group was updated in the database
        self.customer_group.refresh_from_db()
        self.assertEqual(self.customer_group.discount_percentage, Decimal('7.50'))
        self.assertEqual(self.customer_group.description, 'Updated description for regular customers')
    
    def test_list_customers(self):
        """
        Test listing customers.
        """
        url = reverse('customer-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Smith')
        self.assertEqual(response.data['results'][0]['phone'], '9876543210')
    
    def test_filter_customers_by_group(self):
        """
        Test filtering customers by group.
        """
        url = reverse('customer-list')
        response = self.client.get(url, {'customer_group': self.customer_group.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['customer_group'], str(self.customer_group.id))
    
    def test_create_customer(self):
        """
        Test creating a customer.
        """
        url = reverse('customer-list')
        data = {
            'name': 'Jane Doe',
            'customer_type': Customer.CUSTOMER_TYPE_INDIVIDUAL,
            'customer_group': str(self.customer_group.id),
            'phone': '9876543211',
            'email': 'jane.doe@example.com',
            'address': '456 Park Ave, City',
            'tax_id': 'TAXPAN654321',
            'credit_limit': '5000.00',
            'status': Customer.STATUS_ACTIVE
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jane Doe')
        self.assertEqual(response.data['customer_type'], Customer.CUSTOMER_TYPE_INDIVIDUAL)
        self.assertEqual(response.data['customer_group'], str(self.customer_group.id))
        self.assertEqual(response.data['phone'], '9876543211')
        self.assertEqual(response.data['email'], 'jane.doe@example.com')
        self.assertEqual(response.data['address'], '456 Park Ave, City')
        self.assertEqual(response.data['tax_id'], 'TAXPAN654321')
        self.assertEqual(response.data['credit_limit'], '5000.00')
        self.assertEqual(response.data['status'], Customer.STATUS_ACTIVE)
        
        # Check that the customer was created in the database
        customer = Customer.objects.get(phone='9876543211')
        self.assertEqual(customer.name, 'Jane Doe')
        self.assertEqual(customer.tenant_id, self.tenant_id)
        self.assertEqual(customer.created_by, self.user_id)
    
    def test_retrieve_customer(self):
        """
        Test retrieving a customer.
        """
        url = reverse('customer-detail', args=[self.customer.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Smith')
        self.assertEqual(response.data['customer_type'], Customer.CUSTOMER_TYPE_INDIVIDUAL)
        self.assertEqual(response.data['customer_group'], str(self.customer_group.id))
        self.assertEqual(response.data['phone'], '9876543210')
        self.assertEqual(response.data['email'], 'john.smith@example.com')
        self.assertEqual(response.data['address'], '123 Main St, City')
        self.assertEqual(response.data['tax_id'], 'TAXPAN123456')
        self.assertEqual(response.data['credit_limit'], '10000.00')
        self.assertEqual(response.data['status'], Customer.STATUS_ACTIVE)
    
    def test_update_customer(self):
        """
        Test updating a customer.
        """
        url = reverse('customer-detail', args=[self.customer.id])
        data = {
            'phone': '9876543212',
            'email': 'john.smith.updated@example.com',
            'address': '123 Main St, Updated City'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '9876543212')
        self.assertEqual(response.data['email'], 'john.smith.updated@example.com')
        self.assertEqual(response.data['address'], '123 Main St, Updated City')
        
        # Check that the customer was updated in the database
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, '9876543212')
        self.assertEqual(self.customer.email, 'john.smith.updated@example.com')
        self.assertEqual(self.customer.address, '123 Main St, Updated City')
    
    def test_list_customer_loyalty(self):
        """
        Test listing customer loyalty.
        """
        url = reverse('customerloyalty-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['loyalty_number'], 'LOY123456')
        self.assertEqual(response.data['results'][0]['points_balance'], 100)
    
    def test_filter_customer_loyalty_by_customer(self):
        """
        Test filtering customer loyalty by customer.
        """
        url = reverse('customerloyalty-list')
        response = self.client.get(url, {'customer': self.customer.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['customer'], str(self.customer.id))
    
    def test_create_customer_loyalty(self):
        """
        Test creating a customer loyalty.
        """
        # Create a new customer for this test
        new_customer = Customer.objects.create(
            tenant_id=self.tenant_id,
            name="New Customer",
            customer_type=Customer.CUSTOMER_TYPE_INDIVIDUAL,
            customer_group=self.customer_group,
            phone="9876543213",
            email="new.customer@example.com",
            created_by=self.user_id
        )
        
        url = reverse('customerloyalty-list')
        data = {
            'customer': str(new_customer.id),
            'loyalty_number': 'LOY654321',
            'points_balance': 50,
            'tier': 'Bronze'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer'], str(new_customer.id))
        self.assertEqual(response.data['loyalty_number'], 'LOY654321')
        self.assertEqual(response.data['points_balance'], 50)
        self.assertEqual(response.data['tier'], 'Bronze')
        
        # Check that the customer loyalty was created in the database
        loyalty = CustomerLoyalty.objects.get(loyalty_number='LOY654321')
        self.assertEqual(loyalty.customer, new_customer)
        self.assertEqual(loyalty.tenant_id, self.tenant_id)
        self.assertEqual(loyalty.created_by, self.user_id)
    
    def test_retrieve_customer_loyalty(self):
        """
        Test retrieving a customer loyalty.
        """
        url = reverse('customerloyalty-detail', args=[self.customer_loyalty.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer'], str(self.customer.id))
        self.assertEqual(response.data['loyalty_number'], 'LOY123456')
        self.assertEqual(response.data['points_balance'], 100)
        self.assertEqual(response.data['tier'], 'Silver')
    
    def test_update_customer_loyalty(self):
        """
        Test updating a customer loyalty.
        """
        url = reverse('customerloyalty-detail', args=[self.customer_loyalty.id])
        data = {
            'points_balance': 150,
            'tier': 'Gold'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['points_balance'], 150)
        self.assertEqual(response.data['tier'], 'Gold')
        
        # Check that the customer loyalty was updated in the database
        self.customer_loyalty.refresh_from_db()
        self.assertEqual(self.customer_loyalty.points_balance, 150)
        self.assertEqual(self.customer_loyalty.tier, 'Gold')
    
    def test_list_sales(self):
        """
        Test listing sales.
        """
        url = reverse('sale-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_number'], 'INV-2023-0001')
        self.assertEqual(response.data['results'][0]['total_amount'], '3955.00')
    
    def test_filter_sales_by_shop(self):
        """
        Test filtering sales by shop.
        """
        url = reverse('sale-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_sales_by_customer(self):
        """
        Test filtering sales by customer.
        """
        url = reverse('sale-list')
        response = self.client.get(url, {'customer': self.customer.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['customer'], str(self.customer.id))
    
    def test_filter_sales_by_date_range(self):
        """
        Test filtering sales by date range.
        """
        url = reverse('sale-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['invoice_date'], '2023-04-15')
    
    @patch('sales.views.generate_invoice_number')
    def test_create_sale(self, mock_generate_invoice_number):
        """
        Test creating a sale.
        """
        mock_generate_invoice_number.return_value = "INV-2023-0002"
        
        url = reverse('sale-list')
        data = {
            'shop_id': str(self.shop_id),
            'invoice_date': '2023-04-20',
            'customer': str(self.customer.id),
            'sale_type': Sale.SALE_TYPE_RETAIL,
            'items': [
                {
                    'product_id': str(self.product_id),
                    'product_variant_id': str(self.product_variant_id),
                    'batch_id': str(self.batch_id),
                    'product_name': 'Johnnie Walker Red Label',
                    'variant_name': '750ml',
                    'quantity': 1,
                    'unit_price': '2500.00',
                    'discount_percentage': '5.00',
                    'tax_percentage': '18.00'
                }
            ],
            'payments': [
                {
                    'payment_method': SalePayment.PAYMENT_METHOD_CASH,
                    'amount': '2800.00'
                }
            ],
            'notes': 'New sale'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['invoice_number'], 'INV-2023-0002')
        self.assertEqual(response.data['invoice_date'], '2023-04-20')
        self.assertEqual(response.data['customer'], str(self.customer.id))
        self.assertEqual(response.data['sale_type'], Sale.SALE_TYPE_RETAIL)
        self.assertEqual(response.data['subtotal'], '2500.00')
        self.assertEqual(response.data['discount_amount'], '125.00')
        self.assertEqual(response.data['tax_amount'], '450.00')
        self.assertEqual(response.data['total_amount'], '2825.00')
        self.assertEqual(response.data['paid_amount'], '2800.00')
        self.assertEqual(response.data['change_amount'], '0.00')
        self.assertEqual(response.data['notes'], 'New sale')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Red Label')
        self.assertEqual(response.data['items'][0]['quantity'], 1)
        self.assertEqual(response.data['items'][0]['unit_price'], '2500.00')
        self.assertEqual(len(response.data['payments']), 1)
        self.assertEqual(response.data['payments'][0]['payment_method'], SalePayment.PAYMENT_METHOD_CASH)
        self.assertEqual(response.data['payments'][0]['amount'], '2800.00')
        
        # Check that the sale was created in the database
        sale = Sale.objects.get(invoice_number='INV-2023-0002')
        self.assertEqual(sale.customer, self.customer)
        self.assertEqual(sale.total_amount, Decimal('2825.00'))
        self.assertEqual(sale.tenant_id, self.tenant_id)
        self.assertEqual(sale.created_by, self.user_id)
        
        # Check that the sale items were created
        items = sale.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product_name, 'Johnnie Walker Red Label')
        self.assertEqual(items[0].quantity, 1)
        self.assertEqual(items[0].unit_price, Decimal('2500.00'))
        
        # Check that the sale payments were created
        payments = sale.payments.all()
        self.assertEqual(payments.count(), 1)
        self.assertEqual(payments[0].payment_method, SalePayment.PAYMENT_METHOD_CASH)
        self.assertEqual(payments[0].amount, Decimal('2800.00'))
    
    def test_retrieve_sale(self):
        """
        Test retrieving a sale.
        """
        url = reverse('sale-detail', args=[self.sale.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_number'], 'INV-2023-0001')
        self.assertEqual(response.data['invoice_date'], '2023-04-15')
        self.assertEqual(response.data['customer'], str(self.customer.id))
        self.assertEqual(response.data['sale_type'], Sale.SALE_TYPE_RETAIL)
        self.assertEqual(response.data['status'], Sale.STATUS_COMPLETED)
        self.assertEqual(response.data['subtotal'], '3500.00')
        self.assertEqual(response.data['discount_amount'], '175.00')
        self.assertEqual(response.data['tax_amount'], '630.00')
        self.assertEqual(response.data['total_amount'], '3955.00')
        self.assertEqual(response.data['paid_amount'], '4000.00')
        self.assertEqual(response.data['change_amount'], '45.00')
        self.assertEqual(response.data['notes'], 'Regular sale')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity'], 1)
        self.assertEqual(response.data['items'][0]['unit_price'], '3500.00')
        self.assertEqual(len(response.data['payments']), 1)
        self.assertEqual(response.data['payments'][0]['payment_method'], SalePayment.PAYMENT_METHOD_CASH)
        self.assertEqual(response.data['payments'][0]['amount'], '4000.00')
    
    def test_list_sale_returns(self):
        """
        Test listing sale returns.
        """
        url = reverse('salereturn-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['return_number'], 'RET-2023-0001')
        self.assertEqual(response.data['results'][0]['total_amount'], '3955.00')
    
    def test_filter_sale_returns_by_shop(self):
        """
        Test filtering sale returns by shop.
        """
        url = reverse('salereturn-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_sale_returns_by_customer(self):
        """
        Test filtering sale returns by customer.
        """
        url = reverse('salereturn-list')
        response = self.client.get(url, {'customer': self.customer.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['customer'], str(self.customer.id))
    
    def test_filter_sale_returns_by_sale(self):
        """
        Test filtering sale returns by sale.
        """
        url = reverse('salereturn-list')
        response = self.client.get(url, {'sale': self.sale.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['sale'], str(self.sale.id))
    
    @patch('sales.views.generate_return_number')
    def test_create_sale_return(self, mock_generate_return_number):
        """
        Test creating a sale return.
        """
        mock_generate_return_number.return_value = "RET-2023-0002"
        
        url = reverse('salereturn-list')
        data = {
            'shop_id': str(self.shop_id),
            'return_date': '2023-04-25',
            'sale': str(self.sale.id),
            'customer': str(self.customer.id),
            'items': [
                {
                    'sale_item': str(self.sale_item.id),
                    'product_id': str(self.product_id),
                    'product_variant_id': str(self.product_variant_id),
                    'batch_id': str(self.batch_id),
                    'product_name': 'Johnnie Walker Black Label',
                    'variant_name': '750ml',
                    'quantity': 1,
                    'unit_price': '3500.00',
                    'discount_percentage': '5.00',
                    'tax_percentage': '18.00',
                    'reason': 'Defective product'
                }
            ],
            'reason': 'Defective product',
            'notes': 'Return for defective product'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['return_number'], 'RET-2023-0002')
        self.assertEqual(response.data['return_date'], '2023-04-25')
        self.assertEqual(response.data['sale'], str(self.sale.id))
        self.assertEqual(response.data['customer'], str(self.customer.id))
        self.assertEqual(response.data['subtotal'], '3500.00')
        self.assertEqual(response.data['discount_amount'], '175.00')
        self.assertEqual(response.data['tax_amount'], '630.00')
        self.assertEqual(response.data['total_amount'], '3955.00')
        self.assertEqual(response.data['refund_amount'], '3955.00')
        self.assertEqual(response.data['reason'], 'Defective product')
        self.assertEqual(response.data['notes'], 'Return for defective product')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity'], 1)
        self.assertEqual(response.data['items'][0]['unit_price'], '3500.00')
        self.assertEqual(response.data['items'][0]['reason'], 'Defective product')
        
        # Check that the sale return was created in the database
        sale_return = SaleReturn.objects.get(return_number='RET-2023-0002')
        self.assertEqual(sale_return.sale, self.sale)
        self.assertEqual(sale_return.customer, self.customer)
        self.assertEqual(sale_return.total_amount, Decimal('3955.00'))
        self.assertEqual(sale_return.tenant_id, self.tenant_id)
        self.assertEqual(sale_return.created_by, self.user_id)
        
        # Check that the sale return items were created
        items = sale_return.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product_name, 'Johnnie Walker Black Label')
        self.assertEqual(items[0].quantity, 1)
        self.assertEqual(items[0].unit_price, Decimal('3500.00'))
        self.assertEqual(items[0].reason, 'Defective product')
    
    def test_retrieve_sale_return(self):
        """
        Test retrieving a sale return.
        """
        url = reverse('salereturn-detail', args=[self.sale_return.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['return_number'], 'RET-2023-0001')
        self.assertEqual(response.data['return_date'], '2023-04-20')
        self.assertEqual(response.data['sale'], str(self.sale.id))
        self.assertEqual(response.data['customer'], str(self.customer.id))
        self.assertEqual(response.data['status'], SaleReturn.STATUS_COMPLETED)
        self.assertEqual(response.data['subtotal'], '3500.00')
        self.assertEqual(response.data['discount_amount'], '175.00')
        self.assertEqual(response.data['tax_amount'], '630.00')
        self.assertEqual(response.data['total_amount'], '3955.00')
        self.assertEqual(response.data['refund_amount'], '3955.00')
        self.assertEqual(response.data['reason'], 'Customer changed mind')
        self.assertEqual(response.data['notes'], 'Full return')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity'], 1)
        self.assertEqual(response.data['items'][0]['unit_price'], '3500.00')
        self.assertEqual(response.data['items'][0]['reason'], 'Customer changed mind')