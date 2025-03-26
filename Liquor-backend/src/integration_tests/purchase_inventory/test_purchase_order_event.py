"""
Integration test for purchase order events between purchase service and inventory service.
This test verifies that when a purchase order is created or updated in the purchase service, the appropriate events
are published to Kafka and can be consumed by the inventory service.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the purchase service purchase order creation function (mock for testing)
def mock_create_purchase_order(shop_id, tenant_id, supplier_id, items, user_id):
    """Mock function for creating a purchase order in the purchase service."""
    purchase_order_id = str(uuid.uuid4())
    po_number = f"PO-{timezone.now().strftime('%Y%m%d')}-{purchase_order_id[:4]}"
    
    # Calculate totals
    subtotal = sum(item['quantity'] * item['purchase_price'] for item in items)
    tax_amount = subtotal * 0.18  # Assuming 18% tax
    total_amount = subtotal + tax_amount
    
    return {
        'id': purchase_order_id,
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

# Import the inventory service brand lookup function (mock for testing)
def mock_lookup_brands(brand_ids, tenant_id):
    """Mock function for looking up brands in the inventory service."""
    return [
        {
            'id': brand_id,
            'name': f'Brand {i+1}',
            'category': 'whisky',
            'size': '750ml',
            'tenant_id': tenant_id,
            'status': 'active'
        }
        for i, brand_id in enumerate(brand_ids)
    ]

class TestPurchaseOrderEventFlow:
    """
    Test the purchase order event flow between purchase service and inventory service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_purchase_order_created_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data, shop_data, user_data):
        """
        Test that when a purchase order is created in the purchase service, the appropriate events
        are published to Kafka and can be consumed by the inventory service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a purchase order
        supplier_id = str(uuid.uuid4())
        brand_id = str(uuid.uuid4())
        
        purchase_order_items = [
            {
                'brand_id': brand_id,
                'quantity': 10,
                'purchase_price': 400.0,
                'total_price': 4000.0
            }
        ]
        
        purchase_order = mock_create_purchase_order(
            shop_id=shop_data['id'],
            tenant_id=tenant_data['id'],
            supplier_id=supplier_id,
            items=purchase_order_items,
            user_id=user_data['id']
        )
        
        # Set up mock consumer with a message that will be returned when polling
        purchase_order_created_event = {
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
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = purchase_order['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(purchase_order_created_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish purchase order created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
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
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_order['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['PURCHASE_ORDER_CREATED']
        assert published_event['purchase_order_id'] == purchase_order['id']
        assert published_event['po_number'] == purchase_order['po_number']
        assert published_event['supplier_id'] == purchase_order['supplier_id']
        assert len(published_event['items']) == len(purchase_order['items'])
        
        # Step 2: Consume the event in the inventory service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['INVENTORY_SERVICE'],
            topics=[TOPICS['PURCHASE_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == purchase_order['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['PURCHASE_ORDER_CREATED']
        assert event_data['purchase_order_id'] == purchase_order['id']
        assert event_data['po_number'] == purchase_order['po_number']
        assert event_data['supplier_id'] == purchase_order['supplier_id']
        assert len(event_data['items']) == len(purchase_order['items'])
        
        # Step 3: Look up brands in the inventory service
        brand_ids = [item['brand_id'] for item in event_data['items']]
        brands = mock_lookup_brands(brand_ids, event_data['tenant_id'])
        
        # Verify that the brands were looked up correctly
        assert len(brands) == len(brand_ids)
        assert brands[0]['id'] == brand_ids[0]
        assert brands[0]['tenant_id'] == event_data['tenant_id']
        
        # Step 4: Create a purchase order reference in the inventory service
        inventory_purchase_order = {
            'id': event_data['purchase_order_id'],
            'po_number': event_data['po_number'],
            'shop_id': event_data['shop_id'],
            'tenant_id': event_data['tenant_id'],
            'supplier_id': event_data['supplier_id'],
            'items': [
                {
                    'brand_id': item['brand_id'],
                    'brand_name': brands[i]['name'],
                    'quantity': item['quantity'],
                    'purchase_price': item['purchase_price']
                }
                for i, item in enumerate(event_data['items'])
            ],
            'total_amount': event_data['total_amount'],
            'status': event_data['status'],
            'synchronized': True,
            'created_at': timezone.now().isoformat()
        }
        
        # Verify that the purchase order reference was created correctly
        assert inventory_purchase_order['id'] == purchase_order['id']
        assert inventory_purchase_order['po_number'] == purchase_order['po_number']
        assert inventory_purchase_order['supplier_id'] == purchase_order['supplier_id']
        assert len(inventory_purchase_order['items']) == len(purchase_order['items'])
        assert inventory_purchase_order['synchronized'] is True

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_purchase_order_approved_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, purchase_order_data, tenant_data, shop_data, user_data):
        """
        Test that when a purchase order is approved in the purchase service, the appropriate events
        are published to Kafka and can be consumed by the inventory service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Update purchase order status to approved
        approved_purchase_order = purchase_order_data.copy()
        approved_purchase_order['status'] = 'approved'
        approved_purchase_order['approved_by'] = user_data['id']
        approved_purchase_order['approved_at'] = timezone.now().isoformat()
        
        # Set up mock consumer with a message that will be returned when polling
        purchase_order_approved_event = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_APPROVED'],
            'purchase_order_id': approved_purchase_order['id'],
            'po_number': approved_purchase_order['po_number'],
            'shop_id': approved_purchase_order['shop_id'],
            'tenant_id': approved_purchase_order['tenant_id'],
            'supplier_id': approved_purchase_order['supplier_id'],
            'status': approved_purchase_order['status'],
            'approved_by': approved_purchase_order['approved_by'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = approved_purchase_order['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(purchase_order_approved_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish purchase order approved event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_APPROVED'],
            'purchase_order_id': approved_purchase_order['id'],
            'po_number': approved_purchase_order['po_number'],
            'shop_id': approved_purchase_order['shop_id'],
            'tenant_id': approved_purchase_order['tenant_id'],
            'supplier_id': approved_purchase_order['supplier_id'],
            'status': approved_purchase_order['status'],
            'approved_by': approved_purchase_order['approved_by'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['PURCHASE_EVENTS'],
            key=approved_purchase_order['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['PURCHASE_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == approved_purchase_order['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['PURCHASE_ORDER_APPROVED']
        assert published_event['purchase_order_id'] == approved_purchase_order['id']
        assert published_event['po_number'] == approved_purchase_order['po_number']
        assert published_event['status'] == 'approved'
        
        # Step 2: Consume the event in the inventory service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['INVENTORY_SERVICE'],
            topics=[TOPICS['PURCHASE_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == approved_purchase_order['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['PURCHASE_ORDER_APPROVED']
        assert event_data['purchase_order_id'] == approved_purchase_order['id']
        assert event_data['po_number'] == approved_purchase_order['po_number']
        assert event_data['status'] == 'approved'
        
        # Step 3: Update the purchase order status in the inventory service
        inventory_purchase_order = {
            'id': event_data['purchase_order_id'],
            'po_number': event_data['po_number'],
            'status': event_data['status'],
            'approved_by': event_data['approved_by'],
            'approved_at': timezone.now().isoformat(),
            'synchronized': True,
            'updated_at': timezone.now().isoformat()
        }
        
        # Verify that the purchase order status was updated correctly
        assert inventory_purchase_order['id'] == approved_purchase_order['id']
        assert inventory_purchase_order['status'] == 'approved'
        assert inventory_purchase_order['synchronized'] is True
