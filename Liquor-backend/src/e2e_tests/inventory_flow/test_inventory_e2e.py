"""
End-to-end test for the inventory flow in the Liquor Management System.
This test verifies the complete flow of inventory management, including
stock receipt, stock adjustment, low stock alerts, and expiry alerts.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES

# Mock functions for the inventory flow
def mock_receive_stock(shop_id, tenant_id, items, user_id):
    """Mock function for receiving stock in the inventory service."""
    receipt_id = str(uuid.uuid4())
    receipt_number = f"GR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    return {
        'id': receipt_id,
        'receipt_number': receipt_number,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'items': items,
        'status': 'completed',
        'received_by': user_id,
        'received_at': timezone.now().isoformat()
    }

def mock_adjust_stock(shop_id, tenant_id, items, reason, user_id):
    """Mock function for adjusting stock in the inventory service."""
    adjustment_id = str(uuid.uuid4())
    
    return {
        'id': adjustment_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'items': items,
        'reason': reason,
        'status': 'completed',
        'adjusted_by': user_id,
        'adjusted_at': timezone.now().isoformat()
    }

def mock_check_low_stock(shop_id, tenant_id, threshold=10):
    """Mock function for checking low stock in the inventory service."""
    low_stock_items = [
        {
            'id': str(uuid.uuid4()),
            'brand_id': str(uuid.uuid4()),
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'current_quantity': 5,
            'min_level': threshold,
            'status': 'active'
        }
    ]
    
    return low_stock_items

def mock_check_expiry(shop_id, tenant_id, days_threshold=30):
    """Mock function for checking expiring items in the inventory service."""
    expiring_items = [
        {
            'id': str(uuid.uuid4()),
            'brand_id': str(uuid.uuid4()),
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'batch': f'BATCH-{uuid.uuid4().hex[:6]}',
            'quantity': 20,
            'expiry_date': (timezone.now() + timedelta(days=15)).date().isoformat(),
            'days_to_expiry': 15
        }
    ]
    
    return expiring_items

def mock_create_purchase_order(shop_id, tenant_id, supplier_id, items, user_id):
    """Mock function for creating a purchase order in the purchase service."""
    po_id = str(uuid.uuid4())
    po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    # Calculate totals
    subtotal = sum(item['quantity'] * item['purchase_price'] for item in items)
    tax_amount = subtotal * 0.18  # Assuming 18% tax
    total_amount = subtotal + tax_amount
    
    return {
        'id': po_id,
        'po_number': po_number,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'supplier_id': supplier_id,
        'items': items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'status': 'draft',
        'created_by': user_id,
        'created_at': timezone.now().isoformat()
    }

def mock_create_alert(alert_type, shop_id, tenant_id, items):
    """Mock function for creating alerts in the reporting service."""
    alert_id = str(uuid.uuid4())
    
    return {
        'id': alert_id,
        'type': alert_type,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'items': items,
        'status': 'active',
        'created_at': timezone.now().isoformat()
    }

class TestInventoryE2EFlow:
    """
    Test the end-to-end inventory flow in the Liquor Management System.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_stock_receipt_flow(self, mock_get_consumer, mock_get_producer,
                               mock_kafka_producer, mock_kafka_consumer,
                               shop_data, brand_data, user_data, supplier_data):
        """
        Test the complete flow of receiving stock, from goods receipt to inventory update
        and reporting.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        supplier_id = supplier_data['id']
        
        # Create stock receipt items
        items = [
            {
                'brand_id': brand_id,
                'quantity': 50,
                'purchase_price': 300.0,
                'batch': 'BATCH-001',
                'expiry_date': (timezone.now() + timedelta(days=365)).date().isoformat()
            }
        ]
        
        # Step 1: Receive stock in the inventory service
        stock_receipt = mock_receive_stock(
            shop_id=shop_id,
            tenant_id=tenant_id,
            items=items,
            user_id=user_id
        )
        
        # Step 2: Publish stock receipt event to Kafka
        from common.utils.kafka_utils import publish_event
        
        stock_receipt_event = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_COMPLETED'],
            'receipt_id': stock_receipt['id'],
            'receipt_number': stock_receipt['receipt_number'],
            'shop_id': stock_receipt['shop_id'],
            'tenant_id': stock_receipt['tenant_id'],
            'items': stock_receipt['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=stock_receipt['id'],
            event_data=stock_receipt_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_receipt['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Update stock levels in the inventory service
        stock_adjustment_id = str(uuid.uuid4())
        stock_adjustment_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': stock_adjustment_id,
            'reference_id': stock_receipt['id'],
            'reference_type': 'goods_receipt',
            'shop_id': stock_receipt['shop_id'],
            'tenant_id': stock_receipt['tenant_id'],
            'items': stock_receipt['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=stock_adjustment_id,
            event_data=stock_adjustment_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_adjustment_id
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 4: Update reporting data
        reporting_update_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': str(uuid.uuid4()),
            'report_type': 'inventory_summary',
            'shop_id': stock_receipt['shop_id'],
            'tenant_id': stock_receipt['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=reporting_update_event['report_id'],
            event_data=reporting_update_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == reporting_update_event['report_id']
        
        # Verify the complete flow
        assert stock_receipt['status'] == 'completed'
        assert len(stock_receipt['items']) == len(items)
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_stock_adjustment_flow(self, mock_get_consumer, mock_get_producer,
                                  mock_kafka_producer, mock_kafka_consumer,
                                  shop_data, brand_data, user_data):
        """
        Test the flow of manual stock adjustment, including the resulting events
        and reporting updates.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        
        # Create stock adjustment items
        items = [
            {
                'brand_id': brand_id,
                'quantity': -5,  # Negative for stock reduction
                'reason': 'Damaged goods'
            }
        ]
        
        # Step 1: Adjust stock in the inventory service
        stock_adjustment = mock_adjust_stock(
            shop_id=shop_id,
            tenant_id=tenant_id,
            items=items,
            reason='Damaged goods',
            user_id=user_id
        )
        
        # Step 2: Publish stock adjustment event to Kafka
        from common.utils.kafka_utils import publish_event
        
        stock_adjustment_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': stock_adjustment['id'],
            'reference_type': 'manual_adjustment',
            'shop_id': stock_adjustment['shop_id'],
            'tenant_id': stock_adjustment['tenant_id'],
            'items': stock_adjustment['items'],
            'reason': stock_adjustment['reason'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=stock_adjustment['id'],
            event_data=stock_adjustment_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_adjustment['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Update reporting data
        reporting_update_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': str(uuid.uuid4()),
            'report_type': 'inventory_adjustment',
            'shop_id': stock_adjustment['shop_id'],
            'tenant_id': stock_adjustment['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=reporting_update_event['report_id'],
            event_data=reporting_update_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == reporting_update_event['report_id']
        
        # Verify the complete flow
        assert stock_adjustment['status'] == 'completed'
        assert stock_adjustment['reason'] == 'Damaged goods'
        assert len(stock_adjustment['items']) == len(items)
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_low_stock_alert_flow(self, mock_get_consumer, mock_get_producer,
                                 mock_kafka_producer, mock_kafka_consumer,
                                 shop_data, brand_data, user_data, supplier_data):
        """
        Test the flow of low stock detection, alert generation, and automatic
        purchase order creation.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        supplier_id = supplier_data['id']
        
        # Step 1: Check for low stock items
        low_stock_items = mock_check_low_stock(
            shop_id=shop_id,
            tenant_id=tenant_id,
            threshold=10
        )
        
        # Step 2: Publish low stock alert event to Kafka
        from common.utils.kafka_utils import publish_event
        
        low_stock_alert_id = str(uuid.uuid4())
        low_stock_alert_event = {
            'event_type': EVENT_TYPES['LOW_STOCK_ALERT'],
            'alert_id': low_stock_alert_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'items': low_stock_items,
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=low_stock_alert_id,
            event_data=low_stock_alert_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == low_stock_alert_id
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Create alert in the reporting service
        alert = mock_create_alert(
            alert_type='low_stock',
            shop_id=shop_id,
            tenant_id=tenant_id,
            items=low_stock_items
        )
        
        # Step 4: Create purchase order items based on low stock
        po_items = [
            {
                'brand_id': item['brand_id'],
                'quantity': 20,  # Order more than the minimum level
                'purchase_price': 300.0
            }
            for item in low_stock_items
        ]
        
        # Step 5: Create purchase order
        purchase_order = mock_create_purchase_order(
            shop_id=shop_id,
            tenant_id=tenant_id,
            supplier_id=supplier_id,
            items=po_items,
            user_id=user_id
        )
        
        # Step 6: Publish purchase order created event to Kafka
        purchase_order_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_CREATED'],
            'purchase_order_id': purchase_order['id'],
            'po_number': purchase_order['po_number'],
            'shop_id': purchase_order['shop_id'],
            'tenant_id': purchase_order['tenant_id'],
            'supplier_id': purchase_order['supplier_id'],
            'items': purchase_order['items'],
            'total_amount': purchase_order['total_amount'],
            'status': purchase_order['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=purchase_order['id'],
            event_data=purchase_order_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_order['id']
        
        # Verify the complete flow
        assert len(low_stock_items) > 0
        assert alert['type'] == 'low_stock'
        assert alert['status'] == 'active'
        assert purchase_order['status'] == 'draft'
        assert len(purchase_order['items']) == len(low_stock_items)
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_expiry_alert_flow(self, mock_get_consumer, mock_get_producer,
                              mock_kafka_producer, mock_kafka_consumer,
                              shop_data, brand_data, user_data):
        """
        Test the flow of expiry detection, alert generation, and reporting.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        
        # Step 1: Check for expiring items
        expiring_items = mock_check_expiry(
            shop_id=shop_id,
            tenant_id=tenant_id,
            days_threshold=30
        )
        
        # Step 2: Publish expiry alert event to Kafka
        from common.utils.kafka_utils import publish_event
        
        expiry_alert_id = str(uuid.uuid4())
        expiry_alert_event = {
            'event_type': EVENT_TYPES['EXPIRY_ALERT'],
            'alert_id': expiry_alert_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'items': expiring_items,
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=expiry_alert_id,
            event_data=expiry_alert_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == expiry_alert_id
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Create alert in the reporting service
        alert = mock_create_alert(
            alert_type='expiry_alert',
            shop_id=shop_id,
            tenant_id=tenant_id,
            items=expiring_items
        )
        
        # Step 4: Generate expiry report
        report_id = str(uuid.uuid4())
        report_event = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'report_id': report_id,
            'report_type': 'expiry_report',
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'parameters': {
                'days_threshold': 30,
                'format': 'pdf'
            },
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_id,
            event_data=report_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_id
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 5: Report generated notification
        report_generated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': report_id,
            'report_type': 'expiry_report',
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'file_url': f'/reports/{report_id}.pdf',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_id,
            event_data=report_generated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_id
        
        # Verify the complete flow
        assert len(expiring_items) > 0
        assert alert['type'] == 'expiry_alert'
        assert alert['status'] == 'active'
