import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from purchase_orders.models import (
    PurchaseOrder, PurchaseOrderItem, PurchaseOrderAttachment, PurchaseOrderHistory
)
from common.jwt_auth import MicroserviceUser

class PurchaseOrdersAPITest(TestCase):
    """
    Test the purchase orders API endpoints.
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
        self.supplier_id = uuid.uuid4()
        self.product_id = uuid.uuid4()
        self.variant_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_purchase_orders', 'add_purchase_orders', 'change_purchase_orders']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
    
    def test_list_purchase_orders(self):
        """
        Test listing purchase orders.
        """
        url = reverse('purchaseorder-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['po_number'], 'PO-2023-0001')
        self.assertEqual(response.data['results'][0]['supplier_name'], 'United Spirits Ltd')
    
    def test_filter_purchase_orders_by_shop(self):
        """
        Test filtering purchase orders by shop.
        """
        url = reverse('purchaseorder-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_purchase_orders_by_supplier(self):
        """
        Test filtering purchase orders by supplier.
        """
        url = reverse('purchaseorder-list')
        response = self.client.get(url, {'supplier_id': self.supplier_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier_id'], str(self.supplier_id))
    
    def test_filter_purchase_orders_by_status(self):
        """
        Test filtering purchase orders by status.
        """
        url = reverse('purchaseorder-list')
        response = self.client.get(url, {'status': PurchaseOrder.STATUS_DRAFT})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], PurchaseOrder.STATUS_DRAFT)
    
    def test_filter_purchase_orders_by_date_range(self):
        """
        Test filtering purchase orders by date range.
        """
        url = reverse('purchaseorder-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['po_date'], '2023-04-15')
    
    @patch('purchase_orders.views.generate_po_number')
    def test_create_purchase_order(self, mock_generate_po_number):
        """
        Test creating a purchase order.
        """
        mock_generate_po_number.return_value = "PO-2023-0002"
        
        url = reverse('purchaseorder-list')
        data = {
            'shop_id': str(self.shop_id),
            'po_date': '2023-04-20',
            'supplier_id': str(self.supplier_id),
            'supplier_name': 'United Spirits Ltd',
            'supplier_code': 'USL',
            'expected_delivery_date': '2023-04-30',
            'delivery_address': '123 Main St, Bangalore',
            'status': PurchaseOrder.STATUS_DRAFT,
            'priority': PurchaseOrder.PRIORITY_HIGH,
            'payment_terms': 'Net 30',
            'shipping_terms': 'FOB',
            'notes': 'Urgent order',
            'items': [
                {
                    'product_id': str(self.product_id),
                    'product_name': 'Johnnie Walker Red Label',
                    'product_code': 'JW-RL',
                    'product_barcode': '5000267023663',
                    'variant_id': str(self.variant_id),
                    'variant_name': '750ml',
                    'quantity': '5.000',
                    'unit_price': '800.00',
                    'tax_rate': '18.00',
                    'discount_percentage': '5.00',
                    'notes': 'Standard whisky'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['po_number'], 'PO-2023-0002')
        self.assertEqual(response.data['po_date'], '2023-04-20')
        self.assertEqual(response.data['supplier_id'], str(self.supplier_id))
        self.assertEqual(response.data['supplier_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['supplier_code'], 'USL')
        self.assertEqual(response.data['expected_delivery_date'], '2023-04-30')
        self.assertEqual(response.data['delivery_address'], '123 Main St, Bangalore')
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_DRAFT)
        self.assertEqual(response.data['priority'], PurchaseOrder.PRIORITY_HIGH)
        self.assertEqual(response.data['payment_terms'], 'Net 30')
        self.assertEqual(response.data['shipping_terms'], 'FOB')
        self.assertEqual(response.data['notes'], 'Urgent order')
        
        # Check calculated fields
        self.assertEqual(Decimal(response.data['subtotal']), Decimal('4000.00'))  # 5 * 800
        self.assertEqual(Decimal(response.data['tax_amount']), Decimal('720.00'))  # 4000 * 0.18
        self.assertEqual(Decimal(response.data['discount_amount']), Decimal('200.00'))  # 4000 * 0.05
        self.assertEqual(Decimal(response.data['total_amount']), Decimal('4520.00'))  # 4000 + 720 - 200
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Red Label')
        self.assertEqual(response.data['items'][0]['quantity'], '5.000')
        self.assertEqual(response.data['items'][0]['unit_price'], '800.00')
        
        # Check that the purchase order was created in the database
        purchase_order = PurchaseOrder.objects.get(po_number='PO-2023-0002')
        self.assertEqual(purchase_order.supplier_name, 'United Spirits Ltd')
        self.assertEqual(purchase_order.tenant_id, self.tenant_id)
        self.assertEqual(purchase_order.created_by, self.user_id)
        
        # Check that the purchase order item was created
        items = purchase_order.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product_name, 'Johnnie Walker Red Label')
        self.assertEqual(items[0].quantity, Decimal('5.000'))
    
    def test_retrieve_purchase_order(self):
        """
        Test retrieving a purchase order.
        """
        url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO-2023-0001')
        self.assertEqual(response.data['po_date'], '2023-04-15')
        self.assertEqual(response.data['supplier_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_DRAFT)
        self.assertEqual(response.data['total_amount'], '11500.00')
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity'], '10.000')
        self.assertEqual(response.data['items'][0]['unit_price'], '1000.00')
    
    def test_update_purchase_order(self):
        """
        Test updating a purchase order.
        """
        url = reverse('purchaseorder-detail', args=[self.purchase_order.id])
        data = {
            'expected_delivery_date': '2023-04-28',
            'priority': PurchaseOrder.PRIORITY_HIGH,
            'notes': 'Updated order notes'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expected_delivery_date'], '2023-04-28')
        self.assertEqual(response.data['priority'], PurchaseOrder.PRIORITY_HIGH)
        self.assertEqual(response.data['notes'], 'Updated order notes')
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.expected_delivery_date, date(2023, 4, 28))
        self.assertEqual(self.purchase_order.priority, PurchaseOrder.PRIORITY_HIGH)
        self.assertEqual(self.purchase_order.notes, 'Updated order notes')
    
    def test_submit_purchase_order(self):
        """
        Test submitting a purchase order for approval.
        """
        url = reverse('purchaseorder-submit', args=[self.purchase_order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_PENDING)
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_PENDING)
        
        # Check that a history entry was created
        history = PurchaseOrderHistory.objects.filter(
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_UPDATED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_approve_purchase_order(self):
        """
        Test approving a purchase order.
        """
        # First set the purchase order to pending status
        self.purchase_order.status = PurchaseOrder.STATUS_PENDING
        self.purchase_order.save()
        
        url = reverse('purchaseorder-approve', args=[self.purchase_order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_APPROVED)
        self.assertEqual(response.data['approved_by'], str(self.user_id))
        self.assertIsNotNone(response.data['approved_at'])
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_APPROVED)
        self.assertEqual(self.purchase_order.approved_by, self.user_id)
        self.assertIsNotNone(self.purchase_order.approved_at)
        
        # Check that a history entry was created
        history = PurchaseOrderHistory.objects.filter(
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_APPROVED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_reject_purchase_order(self):
        """
        Test rejecting a purchase order.
        """
        # First set the purchase order to pending status
        self.purchase_order.status = PurchaseOrder.STATUS_PENDING
        self.purchase_order.save()
        
        url = reverse('purchaseorder-reject', args=[self.purchase_order.id])
        data = {
            'rejection_reason': 'Budget constraints'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_REJECTED)
        self.assertEqual(response.data['rejection_reason'], 'Budget constraints')
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_REJECTED)
        self.assertEqual(self.purchase_order.rejection_reason, 'Budget constraints')
        
        # Check that a history entry was created
        history = PurchaseOrderHistory.objects.filter(
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_REJECTED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
        self.assertEqual(history.notes, 'Budget constraints')
    
    def test_send_purchase_order(self):
        """
        Test sending a purchase order to supplier.
        """
        # First set the purchase order to approved status
        self.purchase_order.status = PurchaseOrder.STATUS_APPROVED
        self.purchase_order.approved_by = self.user_id
        self.purchase_order.approved_at = timezone.now()
        self.purchase_order.save()
        
        url = reverse('purchaseorder-send', args=[self.purchase_order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_SENT)
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_SENT)
        
        # Check that a history entry was created
        history = PurchaseOrderHistory.objects.filter(
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_SENT
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_cancel_purchase_order(self):
        """
        Test cancelling a purchase order.
        """
        url = reverse('purchaseorder-cancel', args=[self.purchase_order.id])
        data = {
            'notes': 'No longer needed'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], PurchaseOrder.STATUS_CANCELLED)
        
        # Check that the purchase order was updated in the database
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_CANCELLED)
        
        # Check that a history entry was created
        history = PurchaseOrderHistory.objects.filter(
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_CANCELLED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
        self.assertEqual(history.notes, 'No longer needed')
    
    def test_get_purchase_order_history(self):
        """
        Test getting purchase order history.
        """
        # Create some history entries
        PurchaseOrderHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_CREATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Purchase order created"
        )
        
        PurchaseOrderHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            purchase_order=self.purchase_order,
            action=PurchaseOrderHistory.ACTION_UPDATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Purchase order updated"
        )
        
        url = reverse('purchaseorder-history', args=[self.purchase_order.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['action'], PurchaseOrderHistory.ACTION_UPDATED)
        self.assertEqual(response.data[1]['action'], PurchaseOrderHistory.ACTION_CREATED)