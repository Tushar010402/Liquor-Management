import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from purchase_orders.models import PurchaseOrder, PurchaseOrderItem
from goods_receipt.models import (
    GoodsReceipt, GoodsReceiptItem, GoodsReceiptAttachment, 
    GoodsReceiptHistory, QualityCheck, QualityCheckItem
)
from common.jwt_auth import MicroserviceUser

class GoodsReceiptAPITest(TestCase):
    """
    Test the goods receipt API endpoints.
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
            'permissions': ['view_goods_receipt', 'add_goods_receipt', 'change_goods_receipt']
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
            status=PurchaseOrder.STATUS_SENT,
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
    
    def test_list_goods_receipts(self):
        """
        Test listing goods receipts.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['gr_number'], 'GR-2023-0001')
        self.assertEqual(response.data['results'][0]['supplier_name'], 'United Spirits Ltd')
    
    def test_filter_goods_receipts_by_shop(self):
        """
        Test filtering goods receipts by shop.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_goods_receipts_by_supplier(self):
        """
        Test filtering goods receipts by supplier.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url, {'supplier_id': self.supplier_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['supplier_id'], str(self.supplier_id))
    
    def test_filter_goods_receipts_by_purchase_order(self):
        """
        Test filtering goods receipts by purchase order.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url, {'purchase_order': self.purchase_order.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['purchase_order'], str(self.purchase_order.id))
    
    def test_filter_goods_receipts_by_status(self):
        """
        Test filtering goods receipts by status.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url, {'status': GoodsReceipt.STATUS_PENDING})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], GoodsReceipt.STATUS_PENDING)
    
    def test_filter_goods_receipts_by_date_range(self):
        """
        Test filtering goods receipts by date range.
        """
        url = reverse('goodsreceipt-list')
        response = self.client.get(url, {
            'start_date': '2023-04-20',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['gr_date'], '2023-04-25')
    
    @patch('goods_receipt.views.generate_gr_number')
    def test_create_goods_receipt(self, mock_generate_gr_number):
        """
        Test creating a goods receipt.
        """
        mock_generate_gr_number.return_value = "GR-2023-0002"
        
        url = reverse('goodsreceipt-list')
        data = {
            'shop_id': str(self.shop_id),
            'gr_date': '2023-04-26',
            'purchase_order': str(self.purchase_order.id),
            'supplier_id': str(self.supplier_id),
            'supplier_name': 'United Spirits Ltd',
            'supplier_code': 'USL',
            'delivery_date': '2023-04-26',
            'delivery_note_number': 'DN-2023-0002',
            'status': GoodsReceipt.STATUS_DRAFT,
            'notes': 'New delivery',
            'items': [
                {
                    'purchase_order_item': str(self.purchase_order_item.id),
                    'product_id': str(self.product_id),
                    'product_name': 'Johnnie Walker Black Label',
                    'product_code': 'JW-BL',
                    'product_barcode': '5000267023656',
                    'variant_id': str(self.variant_id),
                    'variant_name': '750ml',
                    'expected_quantity': '10.000',
                    'received_quantity': '8.000',
                    'accepted_quantity': '8.000',
                    'rejected_quantity': '0.000',
                    'unit_price': '1000.00',
                    'tax_rate': '18.00',
                    'discount_percentage': '5.00',
                    'batch_number': 'BL-2023-002',
                    'expiry_date': '2025-04-26',
                    'manufacturing_date': '2023-01-20',
                    'notes': 'Good condition'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['gr_number'], 'GR-2023-0002')
        self.assertEqual(response.data['gr_date'], '2023-04-26')
        self.assertEqual(response.data['purchase_order'], str(self.purchase_order.id))
        self.assertEqual(response.data['supplier_id'], str(self.supplier_id))
        self.assertEqual(response.data['supplier_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['supplier_code'], 'USL')
        self.assertEqual(response.data['delivery_date'], '2023-04-26')
        self.assertEqual(response.data['delivery_note_number'], 'DN-2023-0002')
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_DRAFT)
        self.assertEqual(response.data['notes'], 'New delivery')
        
        # Check calculated fields
        self.assertEqual(Decimal(response.data['subtotal']), Decimal('8000.00'))  # 8 * 1000
        self.assertEqual(Decimal(response.data['tax_amount']), Decimal('1440.00'))  # 8000 * 0.18
        self.assertEqual(Decimal(response.data['discount_amount']), Decimal('400.00'))  # 8000 * 0.05
        self.assertEqual(Decimal(response.data['total_amount']), Decimal('9040.00'))  # 8000 + 1440 - 400
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['received_quantity'], '8.000')
        self.assertEqual(response.data['items'][0]['accepted_quantity'], '8.000')
        self.assertEqual(response.data['items'][0]['batch_number'], 'BL-2023-002')
        
        # Check that the goods receipt was created in the database
        goods_receipt = GoodsReceipt.objects.get(gr_number='GR-2023-0002')
        self.assertEqual(goods_receipt.supplier_name, 'United Spirits Ltd')
        self.assertEqual(goods_receipt.tenant_id, self.tenant_id)
        self.assertEqual(goods_receipt.created_by, self.user_id)
        
        # Check that the goods receipt item was created
        items = goods_receipt.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product_name, 'Johnnie Walker Black Label')
        self.assertEqual(items[0].received_quantity, Decimal('8.000'))
        self.assertEqual(items[0].batch_number, 'BL-2023-002')
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=goods_receipt,
            action=GoodsReceiptHistory.ACTION_CREATED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_retrieve_goods_receipt(self):
        """
        Test retrieving a goods receipt.
        """
        url = reverse('goodsreceipt-detail', args=[self.goods_receipt.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['gr_number'], 'GR-2023-0001')
        self.assertEqual(response.data['gr_date'], '2023-04-25')
        self.assertEqual(response.data['purchase_order'], str(self.purchase_order.id))
        self.assertEqual(response.data['supplier_name'], 'United Spirits Ltd')
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_PENDING)
        self.assertEqual(response.data['total_amount'], '11500.00')
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['received_quantity'], '10.000')
        self.assertEqual(response.data['items'][0]['accepted_quantity'], '9.000')
        self.assertEqual(response.data['items'][0]['batch_number'], 'BL-2023-001')
    
    def test_update_goods_receipt(self):
        """
        Test updating a goods receipt.
        """
        url = reverse('goodsreceipt-detail', args=[self.goods_receipt.id])
        data = {
            'delivery_note_number': 'DN-2023-0001-A',
            'notes': 'Updated delivery notes'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_note_number'], 'DN-2023-0001-A')
        self.assertEqual(response.data['notes'], 'Updated delivery notes')
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.delivery_note_number, 'DN-2023-0001-A')
        self.assertEqual(self.goods_receipt.notes, 'Updated delivery notes')
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_UPDATED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_submit_goods_receipt(self):
        """
        Test submitting a goods receipt for approval.
        """
        # First set the goods receipt to draft status
        self.goods_receipt.status = GoodsReceipt.STATUS_DRAFT
        self.goods_receipt.save()
        
        url = reverse('goodsreceipt-submit', args=[self.goods_receipt.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_PENDING)
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_PENDING)
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_UPDATED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_approve_goods_receipt(self):
        """
        Test approving a goods receipt.
        """
        url = reverse('goodsreceipt-approve', args=[self.goods_receipt.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_APPROVED)
        self.assertEqual(response.data['approved_by'], str(self.user_id))
        self.assertIsNotNone(response.data['approved_at'])
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_APPROVED)
        self.assertEqual(self.goods_receipt.approved_by, self.user_id)
        self.assertIsNotNone(self.goods_receipt.approved_at)
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_APPROVED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
    
    def test_reject_goods_receipt(self):
        """
        Test rejecting a goods receipt.
        """
        url = reverse('goodsreceipt-reject', args=[self.goods_receipt.id])
        data = {
            'rejection_reason': 'Incorrect items'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_REJECTED)
        self.assertEqual(response.data['rejection_reason'], 'Incorrect items')
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_REJECTED)
        self.assertEqual(self.goods_receipt.rejection_reason, 'Incorrect items')
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_REJECTED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
        self.assertEqual(history.notes, 'Incorrect items')
    
    def test_complete_goods_receipt(self):
        """
        Test completing a goods receipt.
        """
        # First set the goods receipt to approved status
        self.goods_receipt.status = GoodsReceipt.STATUS_APPROVED
        self.goods_receipt.approved_by = self.user_id
        self.goods_receipt.approved_at = timezone.now()
        self.goods_receipt.save()
        
        url = reverse('goodsreceipt-complete', args=[self.goods_receipt.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_COMPLETED)
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_COMPLETED)
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_COMPLETED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
        
        # Check that the purchase order status was updated
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, PurchaseOrder.STATUS_RECEIVED)
    
    def test_cancel_goods_receipt(self):
        """
        Test cancelling a goods receipt.
        """
        url = reverse('goodsreceipt-cancel', args=[self.goods_receipt.id])
        data = {
            'notes': 'Duplicate entry'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], GoodsReceipt.STATUS_CANCELLED)
        
        # Check that the goods receipt was updated in the database
        self.goods_receipt.refresh_from_db()
        self.assertEqual(self.goods_receipt.status, GoodsReceipt.STATUS_CANCELLED)
        
        # Check that a history entry was created
        history = GoodsReceiptHistory.objects.filter(
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_CANCELLED
        ).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.user_id, self.user_id)
        self.assertEqual(history.notes, 'Duplicate entry')
    
    def test_get_goods_receipt_history(self):
        """
        Test getting goods receipt history.
        """
        # Create some history entries
        GoodsReceiptHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_CREATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Goods receipt created"
        )
        
        GoodsReceiptHistory.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            goods_receipt=self.goods_receipt,
            action=GoodsReceiptHistory.ACTION_UPDATED,
            user_id=self.user_id,
            user_name="John Doe",
            notes="Goods receipt updated"
        )
        
        url = reverse('goodsreceipt-history', args=[self.goods_receipt.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['action'], GoodsReceiptHistory.ACTION_UPDATED)
        self.assertEqual(response.data[1]['action'], GoodsReceiptHistory.ACTION_CREATED)
    
    def test_list_quality_checks(self):
        """
        Test listing quality checks.
        """
        url = reverse('qualitycheck-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['check_number'], 'QC-2023-0001')
        self.assertEqual(response.data['results'][0]['status'], QualityCheck.STATUS_PARTIALLY_PASSED)
    
    def test_filter_quality_checks_by_goods_receipt(self):
        """
        Test filtering quality checks by goods receipt.
        """
        url = reverse('qualitycheck-list')
        response = self.client.get(url, {'goods_receipt': self.goods_receipt.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['goods_receipt'], str(self.goods_receipt.id))
    
    @patch('goods_receipt.views.generate_qc_number')
    def test_create_quality_check(self, mock_generate_qc_number):
        """
        Test creating a quality check.
        """
        mock_generate_qc_number.return_value = "QC-2023-0002"
        
        url = reverse('qualitycheck-list')
        data = {
            'shop_id': str(self.shop_id),
            'goods_receipt': str(self.goods_receipt.id),
            'check_date': '2023-04-26',
            'notes': 'Second quality check',
            'items': [
                {
                    'goods_receipt_item': str(self.goods_receipt_item.id),
                    'product_id': str(self.product_id),
                    'product_name': 'Johnnie Walker Black Label',
                    'quantity_checked': '9.000',
                    'quantity_passed': '9.000',
                    'quantity_failed': '0.000',
                    'status': QualityCheckItem.STATUS_PASSED,
                    'notes': 'All bottles in good condition'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['check_number'], 'QC-2023-0002')
        self.assertEqual(response.data['goods_receipt'], str(self.goods_receipt.id))
        self.assertEqual(response.data['check_date'], '2023-04-26')
        self.assertEqual(response.data['status'], QualityCheck.STATUS_PASSED)
        self.assertEqual(response.data['notes'], 'Second quality check')
        self.assertEqual(response.data['checked_by'], str(self.user_id))
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity_checked'], '9.000')
        self.assertEqual(response.data['items'][0]['quantity_passed'], '9.000')
        self.assertEqual(response.data['items'][0]['status'], QualityCheckItem.STATUS_PASSED)
        
        # Check that the quality check was created in the database
        quality_check = QualityCheck.objects.get(check_number='QC-2023-0002')
        self.assertEqual(quality_check.goods_receipt, self.goods_receipt)
        self.assertEqual(quality_check.tenant_id, self.tenant_id)
        self.assertEqual(quality_check.checked_by, self.user_id)
        
        # Check that the quality check item was created
        items = quality_check.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product_name, 'Johnnie Walker Black Label')
        self.assertEqual(items[0].quantity_checked, Decimal('9.000'))
    
    def test_retrieve_quality_check(self):
        """
        Test retrieving a quality check.
        """
        url = reverse('qualitycheck-detail', args=[self.quality_check.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['check_number'], 'QC-2023-0001')
        self.assertEqual(response.data['goods_receipt'], str(self.goods_receipt.id))
        self.assertEqual(response.data['check_date'], '2023-04-25')
        self.assertEqual(response.data['status'], QualityCheck.STATUS_PARTIALLY_PASSED)
        self.assertEqual(response.data['notes'], 'Quality check performed')
        
        # Check items
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['items'][0]['quantity_checked'], '10.000')
        self.assertEqual(response.data['items'][0]['quantity_passed'], '9.000')
        self.assertEqual(response.data['items'][0]['quantity_failed'], '1.000')
        self.assertEqual(response.data['items'][0]['status'], QualityCheckItem.STATUS_PARTIALLY_PASSED)
        self.assertEqual(response.data['items'][0]['failure_reason'], 'One bottle damaged')
    
    def test_update_quality_check(self):
        """
        Test updating a quality check.
        """
        url = reverse('qualitycheck-detail', args=[self.quality_check.id])
        data = {
            'notes': 'Updated quality check notes'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Updated quality check notes')
        
        # Check that the quality check was updated in the database
        self.quality_check.refresh_from_db()
        self.assertEqual(self.quality_check.notes, 'Updated quality check notes')