import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from products.models import (
    Category, Brand, Product, ProductVariant
)
from stock.models import (
    Stock, StockMovement, StockAdjustment, StockAdjustmentItem,
    StockTransfer, StockTransferItem, Batch
)
from common.jwt_auth import MicroserviceUser

class StockAPITest(TestCase):
    """
    Test the stock API endpoints.
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
        self.shop_id2 = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_stock', 'add_stock', 'change_stock']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
        
        # Create batch
        self.batch = Batch.objects.create(
            tenant_id=self.tenant_id,
            product=self.product,
            product_variant=self.product_variant,
            batch_number="BL-2023-001",
            manufacturing_date=date(2023, 1, 1),
            expiry_date=date(2025, 1, 1),
            cost_price=Decimal('2800.00'),
            mrp=Decimal('3800.00'),
            created_by=self.user_id
        )
        
        # Create stock
        self.stock = Stock.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=50,
            available_quantity=50,
            created_by=self.user_id
        )
        
        # Create stock movement
        self.stock_movement = StockMovement.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=50,
            movement_type=StockMovement.MOVEMENT_TYPE_IN,
            reference_type=StockMovement.REFERENCE_TYPE_PURCHASE,
            reference_id=uuid.uuid4(),
            notes="Initial stock",
            created_by=self.user_id
        )
        
        # Create stock adjustment
        self.stock_adjustment = StockAdjustment.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            adjustment_number="ADJ-2023-001",
            adjustment_date=date(2023, 4, 15),
            adjustment_type=StockAdjustment.ADJUSTMENT_TYPE_LOSS,
            status=StockAdjustment.STATUS_PENDING,
            notes="Breakage adjustment",
            created_by=self.user_id
        )
        
        # Create stock adjustment item
        self.stock_adjustment_item = StockAdjustmentItem.objects.create(
            tenant_id=self.tenant_id,
            adjustment=self.stock_adjustment,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            current_quantity=50,
            adjusted_quantity=45,
            adjustment_quantity=5,
            reason="Breakage",
            created_by=self.user_id
        )
        
        # Create stock transfer
        self.stock_transfer = StockTransfer.objects.create(
            tenant_id=self.tenant_id,
            transfer_number="TRF-2023-001",
            transfer_date=date(2023, 4, 20),
            from_shop_id=self.shop_id,
            to_shop_id=self.shop_id2,
            status=StockTransfer.STATUS_PENDING,
            notes="Transfer to new shop",
            created_by=self.user_id
        )
        
        # Create stock transfer item
        self.stock_transfer_item = StockTransferItem.objects.create(
            tenant_id=self.tenant_id,
            transfer=self.stock_transfer,
            product=self.product,
            product_variant=self.product_variant,
            batch=self.batch,
            quantity=10,
            created_by=self.user_id
        )
    
    def test_list_batches(self):
        """
        Test listing batches.
        """
        url = reverse('batch-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['batch_number'], 'BL-2023-001')
    
    def test_filter_batches_by_product(self):
        """
        Test filtering batches by product.
        """
        url = reverse('batch-list')
        response = self.client.get(url, {'product': self.product.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], str(self.product.id))
    
    def test_create_batch(self):
        """
        Test creating a batch.
        """
        url = reverse('batch-list')
        data = {
            'product': str(self.product.id),
            'product_variant': str(self.product_variant.id),
            'batch_number': 'BL-2023-002',
            'manufacturing_date': '2023-02-01',
            'expiry_date': '2025-02-01',
            'cost_price': '2900.00',
            'mrp': '3900.00'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['batch_number'], 'BL-2023-002')
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['manufacturing_date'], '2023-02-01')
        self.assertEqual(response.data['expiry_date'], '2025-02-01')
        self.assertEqual(response.data['cost_price'], '2900.00')
        self.assertEqual(response.data['mrp'], '3900.00')
        
        # Check that the batch was created in the database
        batch = Batch.objects.get(batch_number='BL-2023-002')
        self.assertEqual(batch.product, self.product)
        self.assertEqual(batch.tenant_id, self.tenant_id)
        self.assertEqual(batch.created_by, self.user_id)
    
    def test_retrieve_batch(self):
        """
        Test retrieving a batch.
        """
        url = reverse('batch-detail', args=[self.batch.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['batch_number'], 'BL-2023-001')
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['manufacturing_date'], '2023-01-01')
        self.assertEqual(response.data['expiry_date'], '2025-01-01')
        self.assertEqual(response.data['cost_price'], '2800.00')
        self.assertEqual(response.data['mrp'], '3800.00')
    
    def test_list_stock(self):
        """
        Test listing stock.
        """
        url = reverse('stock-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['quantity'], '50.00')
    
    def test_filter_stock_by_shop(self):
        """
        Test filtering stock by shop.
        """
        url = reverse('stock-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_stock_by_product(self):
        """
        Test filtering stock by product.
        """
        url = reverse('stock-list')
        response = self.client.get(url, {'product': self.product.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], str(self.product.id))
    
    def test_create_stock(self):
        """
        Test creating stock.
        """
        url = reverse('stock-list')
        data = {
            'shop_id': str(self.shop_id2),
            'product': str(self.product.id),
            'product_variant': str(self.product_variant.id),
            'batch': str(self.batch.id),
            'quantity': '20.00',
            'available_quantity': '20.00'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop_id'], str(self.shop_id2))
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['batch'], str(self.batch.id))
        self.assertEqual(response.data['quantity'], '20.00')
        self.assertEqual(response.data['available_quantity'], '20.00')
        
        # Check that the stock was created in the database
        stock = Stock.objects.get(shop_id=self.shop_id2)
        self.assertEqual(stock.product, self.product)
        self.assertEqual(stock.quantity, Decimal('20.00'))
        self.assertEqual(stock.tenant_id, self.tenant_id)
        self.assertEqual(stock.created_by, self.user_id)
    
    def test_retrieve_stock(self):
        """
        Test retrieving stock.
        """
        url = reverse('stock-detail', args=[self.stock.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['batch'], str(self.batch.id))
        self.assertEqual(response.data['quantity'], '50.00')
        self.assertEqual(response.data['available_quantity'], '50.00')
    
    def test_update_stock(self):
        """
        Test updating stock.
        """
        url = reverse('stock-detail', args=[self.stock.id])
        data = {
            'quantity': '45.00',
            'available_quantity': '45.00'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], '45.00')
        self.assertEqual(response.data['available_quantity'], '45.00')
        
        # Check that the stock was updated in the database
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, Decimal('45.00'))
        self.assertEqual(self.stock.available_quantity, Decimal('45.00'))
    
    def test_list_stock_movements(self):
        """
        Test listing stock movements.
        """
        url = reverse('stockmovement-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['quantity'], '50.00')
        self.assertEqual(response.data['results'][0]['movement_type'], StockMovement.MOVEMENT_TYPE_IN)
    
    def test_filter_stock_movements_by_shop(self):
        """
        Test filtering stock movements by shop.
        """
        url = reverse('stockmovement-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_stock_movements_by_product(self):
        """
        Test filtering stock movements by product.
        """
        url = reverse('stockmovement-list')
        response = self.client.get(url, {'product': self.product.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['product'], str(self.product.id))
    
    def test_create_stock_movement(self):
        """
        Test creating a stock movement.
        """
        url = reverse('stockmovement-list')
        data = {
            'shop_id': str(self.shop_id),
            'product': str(self.product.id),
            'product_variant': str(self.product_variant.id),
            'batch': str(self.batch.id),
            'quantity': '10.00',
            'movement_type': StockMovement.MOVEMENT_TYPE_OUT,
            'reference_type': StockMovement.REFERENCE_TYPE_SALE,
            'reference_id': str(uuid.uuid4()),
            'notes': 'Sale movement'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['product'], str(self.product.id))
        self.assertEqual(response.data['product_variant'], str(self.product_variant.id))
        self.assertEqual(response.data['batch'], str(self.batch.id))
        self.assertEqual(response.data['quantity'], '10.00')
        self.assertEqual(response.data['movement_type'], StockMovement.MOVEMENT_TYPE_OUT)
        self.assertEqual(response.data['reference_type'], StockMovement.REFERENCE_TYPE_SALE)
        self.assertEqual(response.data['notes'], 'Sale movement')
        
        # Check that the stock movement was created in the database
        movement = StockMovement.objects.filter(movement_type=StockMovement.MOVEMENT_TYPE_OUT).first()
        self.assertEqual(movement.product, self.product)
        self.assertEqual(movement.quantity, Decimal('10.00'))
        self.assertEqual(movement.tenant_id, self.tenant_id)
        self.assertEqual(movement.created_by, self.user_id)
    
    def test_list_stock_adjustments(self):
        """
        Test listing stock adjustments.
        """
        url = reverse('stockadjustment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['adjustment_number'], 'ADJ-2023-001')
        self.assertEqual(response.data['results'][0]['adjustment_type'], StockAdjustment.ADJUSTMENT_TYPE_LOSS)
    
    def test_filter_stock_adjustments_by_shop(self):
        """
        Test filtering stock adjustments by shop.
        """
        url = reverse('stockadjustment-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_create_stock_adjustment(self):
        """
        Test creating a stock adjustment.
        """
        url = reverse('stockadjustment-list')
        data = {
            'shop_id': str(self.shop_id),
            'adjustment_number': 'ADJ-2023-002',
            'adjustment_date': '2023-04-20',
            'adjustment_type': StockAdjustment.ADJUSTMENT_TYPE_GAIN,
            'status': StockAdjustment.STATUS_PENDING,
            'notes': 'Found additional stock',
            'items': [
                {
                    'product': str(self.product.id),
                    'product_variant': str(self.product_variant.id),
                    'batch': str(self.batch.id),
                    'current_quantity': 50,
                    'adjusted_quantity': 55,
                    'adjustment_quantity': 5,
                    'reason': 'Found additional stock'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['adjustment_number'], 'ADJ-2023-002')
        self.assertEqual(response.data['adjustment_date'], '2023-04-20')
        self.assertEqual(response.data['adjustment_type'], StockAdjustment.ADJUSTMENT_TYPE_GAIN)
        self.assertEqual(response.data['status'], StockAdjustment.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Found additional stock')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product'], str(self.product.id))
        self.assertEqual(response.data['items'][0]['adjustment_quantity'], '5.00')
        
        # Check that the stock adjustment was created in the database
        adjustment = StockAdjustment.objects.get(adjustment_number='ADJ-2023-002')
        self.assertEqual(adjustment.adjustment_type, StockAdjustment.ADJUSTMENT_TYPE_GAIN)
        self.assertEqual(adjustment.tenant_id, self.tenant_id)
        self.assertEqual(adjustment.created_by, self.user_id)
        
        # Check that the stock adjustment item was created
        items = adjustment.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product, self.product)
        self.assertEqual(items[0].adjustment_quantity, Decimal('5.00'))
    
    def test_retrieve_stock_adjustment(self):
        """
        Test retrieving a stock adjustment.
        """
        url = reverse('stockadjustment-detail', args=[self.stock_adjustment.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['adjustment_number'], 'ADJ-2023-001')
        self.assertEqual(response.data['adjustment_date'], '2023-04-15')
        self.assertEqual(response.data['adjustment_type'], StockAdjustment.ADJUSTMENT_TYPE_LOSS)
        self.assertEqual(response.data['status'], StockAdjustment.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Breakage adjustment')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product'], str(self.product.id))
        self.assertEqual(response.data['items'][0]['adjustment_quantity'], '5.00')
    
    def test_approve_stock_adjustment(self):
        """
        Test approving a stock adjustment.
        """
        url = reverse('stockadjustment-approve', args=[self.stock_adjustment.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], StockAdjustment.STATUS_APPROVED)
        
        # Check that the stock adjustment was approved in the database
        self.stock_adjustment.refresh_from_db()
        self.assertEqual(self.stock_adjustment.status, StockAdjustment.STATUS_APPROVED)
        self.assertEqual(self.stock_adjustment.approved_by, self.user_id)
        self.assertIsNotNone(self.stock_adjustment.approved_at)
    
    def test_list_stock_transfers(self):
        """
        Test listing stock transfers.
        """
        url = reverse('stocktransfer-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['transfer_number'], 'TRF-2023-001')
    
    def test_filter_stock_transfers_by_shop(self):
        """
        Test filtering stock transfers by shop.
        """
        url = reverse('stocktransfer-list')
        response = self.client.get(url, {'from_shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['from_shop_id'], str(self.shop_id))
    
    def test_create_stock_transfer(self):
        """
        Test creating a stock transfer.
        """
        url = reverse('stocktransfer-list')
        data = {
            'transfer_number': 'TRF-2023-002',
            'transfer_date': '2023-04-25',
            'from_shop_id': str(self.shop_id),
            'to_shop_id': str(self.shop_id2),
            'status': StockTransfer.STATUS_PENDING,
            'notes': 'Another transfer',
            'items': [
                {
                    'product': str(self.product.id),
                    'product_variant': str(self.product_variant.id),
                    'batch': str(self.batch.id),
                    'quantity': 5
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transfer_number'], 'TRF-2023-002')
        self.assertEqual(response.data['transfer_date'], '2023-04-25')
        self.assertEqual(response.data['from_shop_id'], str(self.shop_id))
        self.assertEqual(response.data['to_shop_id'], str(self.shop_id2))
        self.assertEqual(response.data['status'], StockTransfer.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Another transfer')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product'], str(self.product.id))
        self.assertEqual(response.data['items'][0]['quantity'], '5.00')
        
        # Check that the stock transfer was created in the database
        transfer = StockTransfer.objects.get(transfer_number='TRF-2023-002')
        self.assertEqual(transfer.from_shop_id, self.shop_id)
        self.assertEqual(transfer.to_shop_id, self.shop_id2)
        self.assertEqual(transfer.tenant_id, self.tenant_id)
        self.assertEqual(transfer.created_by, self.user_id)
        
        # Check that the stock transfer item was created
        items = transfer.items.all()
        self.assertEqual(items.count(), 1)
        self.assertEqual(items[0].product, self.product)
        self.assertEqual(items[0].quantity, Decimal('5.00'))
    
    def test_retrieve_stock_transfer(self):
        """
        Test retrieving a stock transfer.
        """
        url = reverse('stocktransfer-detail', args=[self.stock_transfer.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transfer_number'], 'TRF-2023-001')
        self.assertEqual(response.data['transfer_date'], '2023-04-20')
        self.assertEqual(response.data['from_shop_id'], str(self.shop_id))
        self.assertEqual(response.data['to_shop_id'], str(self.shop_id2))
        self.assertEqual(response.data['status'], StockTransfer.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Transfer to new shop')
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product'], str(self.product.id))
        self.assertEqual(response.data['items'][0]['quantity'], '10.00')
    
    def test_approve_stock_transfer(self):
        """
        Test approving a stock transfer.
        """
        url = reverse('stocktransfer-approve', args=[self.stock_transfer.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], StockTransfer.STATUS_APPROVED)
        
        # Check that the stock transfer was approved in the database
        self.stock_transfer.refresh_from_db()
        self.assertEqual(self.stock_transfer.status, StockTransfer.STATUS_APPROVED)
        self.assertEqual(self.stock_transfer.approved_by, self.user_id)
        self.assertIsNotNone(self.stock_transfer.approved_at)
    
    def test_receive_stock_transfer(self):
        """
        Test receiving a stock transfer.
        """
        # First approve the transfer
        self.stock_transfer.status = StockTransfer.STATUS_APPROVED
        self.stock_transfer.approved_by = self.user_id
        self.stock_transfer.approved_at = timezone.now()
        self.stock_transfer.save()
        
        url = reverse('stocktransfer-receive', args=[self.stock_transfer.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], StockTransfer.STATUS_COMPLETED)
        
        # Check that the stock transfer was received in the database
        self.stock_transfer.refresh_from_db()
        self.assertEqual(self.stock_transfer.status, StockTransfer.STATUS_COMPLETED)
        self.assertEqual(self.stock_transfer.received_by, self.user_id)
        self.assertIsNotNone(self.stock_transfer.received_at)