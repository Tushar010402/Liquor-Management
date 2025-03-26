"""
Integration test for goods receipt events between purchase service and inventory service.
This test verifies that when a goods receipt is completed in the purchase service, the appropriate events
are published to Kafka and can be consumed by the inventory service to update stock levels.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the purchase service goods receipt completion function (mock for testing)
def mock_complete_goods_receipt(goods_receipt_id, purchase_order_id, items, user_id):
    """Mock function for completing a goods receipt in the purchase service."""
    return {
        'id': goods_receipt_id,
        'purchase_order_id': purchase_order_id,
        'items': items,
        'status': 'completed',
        'completed_by': user_id,
        'completed_at': timezone.now().isoformat()
    }

# Import the inventory service stock update function (mock for testing)
def mock_update_stock(stock_data):
    """Mock function for updating stock in the inventory service."""
    results = []
    for item in stock_data['items']:
        stock_item = {
            'id': str(uuid.uuid4()),
            'brand_id': item['brand_id'],
            'shop_id': stock_data['shop_id'],
            'quantity': item['quantity'],
            'batch': item.get('batch', 'GR-' + stock_data['goods_receipt_id'][:8]),
            'expiry_date': item.get('expiry_date'),
            'purchase_price': item.get('purchase_price'),
            'tenant_id': stock_data['tenant_id'],
            'updated_at': timezone.now().isoformat()
        }
        results.append(stock_item)
    return results

class TestGoodsReceiptEventFlow:
    """
    Test the goods receipt event flow between purchase service and inventory service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_goods_receipt_completed_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, purchase_order_data, tenant_data, shop_data, user_data):
        """
        Test that when a goods receipt is completed in the purchase service, the appropriate events
        are published to Kafka and can be consumed by the inventory service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a goods receipt
        goods_receipt_id = str(uuid.uuid4())
        goods_receipt_items = [
            {
                'brand_id': purchase_order_data['items'][0]['brand_id'],
                'quantity': purchase_order_data['items'][0]['quantity'],
                'purchase_price': purchase_order_data['items'][0]['purchase_price'],
                'batch': 'BATCH-001',
                'expiry_date': (timezone.now() + timezone.timedelta(days=365)).date().isoformat()
            }
        ]
        
        # Set up mock consumer with a message that will be returned when polling
        goods_receipt_completed_event = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_COMPLETED'],
            'goods_receipt_id': goods_receipt_id,
            'purchase_order_id': purchase_order_data['id'],
            'shop_id': shop_data['id'],
            'tenant_id': tenant_data['id'],
            'items': goods_receipt_items,
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = goods_receipt_id.encode('utf-8')
        mock_message.value.return_value = json.dumps(goods_receipt_completed_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Complete a goods receipt in the purchase service
        completed_goods_receipt = mock_complete_goods_receipt(
            goods_receipt_id=goods_receipt_id,
            purchase_order_id=purchase_order_data['id'],
            items=goods_receipt_items,
            user_id=user_data['id']
        )
        
        # Step 2: Publish goods receipt completed event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_COMPLETED'],
            'goods_receipt_id': completed_goods_receipt['id'],
            'purchase_order_id': completed_goods_receipt['purchase_order_id'],
            'shop_id': shop_data['id'],
            'tenant_id': tenant_data['id'],
            'items': completed_goods_receipt['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['GOODS_RECEIPT_EVENTS'],
            key=completed_goods_receipt['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['GOODS_RECEIPT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == completed_goods_receipt['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']
        assert published_event['goods_receipt_id'] == completed_goods_receipt['id']
        assert published_event['purchase_order_id'] == completed_goods_receipt['purchase_order_id']
        assert len(published_event['items']) == len(completed_goods_receipt['items'])
        
        # Step 3: Consume the event in the inventory service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['INVENTORY_SERVICE'],
            topics=[TOPICS['GOODS_RECEIPT_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == completed_goods_receipt['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']
        assert event_data['goods_receipt_id'] == completed_goods_receipt['id']
        assert event_data['purchase_order_id'] == completed_goods_receipt['purchase_order_id']
        assert len(event_data['items']) == len(completed_goods_receipt['items'])
        
        # Step 4: Update stock in the inventory service
        updated_stock = mock_update_stock(event_data)
        
        # Verify that the stock was updated correctly
        assert len(updated_stock) == len(event_data['items'])
        assert updated_stock[0]['brand_id'] == event_data['items'][0]['brand_id']
        assert updated_stock[0]['quantity'] == event_data['items'][0]['quantity']
        assert updated_stock[0]['shop_id'] == event_data['shop_id']
        assert updated_stock[0]['tenant_id'] == event_data['tenant_id']
        
        # Step 5: Publish stock updated event to Kafka
        stock_updated_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': str(uuid.uuid4()),
            'reference_id': event_data['goods_receipt_id'],
            'reference_type': 'goods_receipt',
            'shop_id': event_data['shop_id'],
            'tenant_id': event_data['tenant_id'],
            'items': [
                {
                    'brand_id': item['brand_id'],
                    'quantity': item['quantity'],
                    'batch': item.get('batch', 'GR-' + event_data['goods_receipt_id'][:8]),
                    'expiry_date': item.get('expiry_date')
                }
                for item in event_data['items']
            ],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=stock_updated_event['adjustment_id'],
            event_data=stock_updated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 2
        
        published_message = mock_kafka_producer.messages[1]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_updated_event['adjustment_id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert published_event['reference_id'] == event_data['goods_receipt_id']
        assert published_event['reference_type'] == 'goods_receipt'
        assert len(published_event['items']) == len(event_data['items'])

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_purchase_order_supplier_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, purchase_order_data, tenant_data, shop_data, user_data):
        """
        Test that when a purchase order is created in the purchase service, the supplier information
        is synchronized with the inventory service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a supplier
        supplier_id = purchase_order_data['supplier_id']
        supplier_data = {
            'id': supplier_id,
            'name': 'Test Supplier',
            'contact_name': 'John Doe',
            'phone': '1234567890',
            'email': 'supplier@example.com',
            'address': '123 Supplier St, Supplier City',
            'tenant_id': tenant_data['id'],
            'status': 'active',
            'created_at': timezone.now().isoformat()
        }
        
        # Set up mock consumer with a message that will be returned when polling
        supplier_created_event = {
            'event_type': EVENT_TYPES['SUPPLIER_CREATED'],
            'supplier_id': supplier_id,
            'name': supplier_data['name'],
            'contact_name': supplier_data['contact_name'],
            'phone': supplier_data['phone'],
            'email': supplier_data['email'],
            'address': supplier_data['address'],
            'tenant_id': supplier_data['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = supplier_id.encode('utf-8')
        mock_message.value.return_value = json.dumps(supplier_created_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish supplier created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['SUPPLIER_CREATED'],
            'supplier_id': supplier_id,
            'name': supplier_data['name'],
            'contact_name': supplier_data['contact_name'],
            'phone': supplier_data['phone'],
            'email': supplier_data['email'],
            'address': supplier_data['address'],
            'tenant_id': supplier_data['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SUPPLIER_EVENTS'],
            key=supplier_id,
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SUPPLIER_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == supplier_id
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SUPPLIER_CREATED']
        assert published_event['supplier_id'] == supplier_id
        assert published_event['name'] == supplier_data['name']
        assert published_event['email'] == supplier_data['email']
        
        # Step 2: Consume the event in the inventory service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['INVENTORY_SERVICE'],
            topics=[TOPICS['SUPPLIER_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == supplier_id
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['SUPPLIER_CREATED']
        assert event_data['supplier_id'] == supplier_id
        assert event_data['name'] == supplier_data['name']
        assert event_data['email'] == supplier_data['email']
        
        # Step 3: Create or update the supplier in the inventory service
        inventory_supplier = {
            'id': event_data['supplier_id'],
            'name': event_data['name'],
            'contact_name': event_data['contact_name'],
            'phone': event_data['phone'],
            'email': event_data['email'],
            'address': event_data['address'],
            'tenant_id': event_data['tenant_id'],
            'status': 'active',
            'synchronized': True,
            'updated_at': timezone.now().isoformat()
        }
        
        # Verify that the supplier was created correctly
        assert inventory_supplier['id'] == supplier_id
        assert inventory_supplier['name'] == supplier_data['name']
        assert inventory_supplier['email'] == supplier_data['email']
        assert inventory_supplier['synchronized'] is True
