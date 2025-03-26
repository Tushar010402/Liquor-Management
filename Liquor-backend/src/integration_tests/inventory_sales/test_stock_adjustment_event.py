"""
Integration test for stock adjustment event flow between inventory service and sales service.
This test verifies that when a stock adjustment is made in the inventory service, the appropriate
events are published to Kafka and can be consumed by the sales service.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the inventory service stock adjustment function (mock for testing)
def mock_create_stock_adjustment(shop_id, items, reason, user_id, tenant_id):
    """Mock function for creating a stock adjustment in the inventory service."""
    adjustment_id = str(uuid.uuid4())
    return {
        'id': adjustment_id,
        'shop_id': shop_id,
        'items': items,
        'reason': reason,
        'status': 'pending',
        'created_by': user_id,
        'tenant_id': tenant_id,
        'created_at': timezone.now().isoformat()
    }

# Import the sales service stock adjustment event handler (mock for testing)
def mock_handle_stock_adjustment_event(adjustment_data):
    """Mock function for handling stock adjustment event in the sales service."""
    # In a real implementation, this would update available stock for sales in the sales service
    return {
        'adjustment_id': adjustment_data['adjustment_id'],
        'shop_id': adjustment_data['shop_id'],
        'items_processed': len(adjustment_data['items']),
        'stock_updated': True
    }

class TestStockAdjustmentEventFlow:
    """
    Test the stock adjustment event flow between inventory service and sales service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_stock_adjustment_event_flow(self, mock_get_consumer, mock_get_producer, 
                                         mock_kafka_producer, mock_kafka_consumer, 
                                         shop_data, brand_data, user_data):
        """
        Test that when a stock adjustment is made in the inventory service, the appropriate
        events are published to Kafka and can be consumed by the sales service.
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
                'previous_quantity': 50,
                'new_quantity': 45,
                'reason': 'breakage'
            }
        ]
        
        # Set up mock consumer with a message that will be returned when polling
        stock_adjustment_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': str(uuid.uuid4()),
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'items': items,
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = stock_adjustment_event['adjustment_id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(stock_adjustment_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Create a stock adjustment in the inventory service
        adjustment = mock_create_stock_adjustment(
            shop_id=shop_id,
            items=items,
            reason='Daily stock count',
            user_id=user_id,
            tenant_id=tenant_id
        )
        
        # Step 2: Publish stock adjustment event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': adjustment['id'],
            'shop_id': adjustment['shop_id'],
            'tenant_id': adjustment['tenant_id'],
            'items': adjustment['items'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=adjustment['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == adjustment['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert published_event['adjustment_id'] == adjustment['id']
        assert published_event['shop_id'] == adjustment['shop_id']
        assert published_event['tenant_id'] == adjustment['tenant_id']
        assert len(published_event['items']) == len(adjustment['items'])
        
        # Step 3: Consume the event in the sales service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['SALES_SERVICE'],
            topics=[TOPICS['STOCK_ADJUSTMENT_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == stock_adjustment_event['adjustment_id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert event_data['adjustment_id'] == stock_adjustment_event['adjustment_id']
        assert event_data['shop_id'] == stock_adjustment_event['shop_id']
        assert event_data['tenant_id'] == stock_adjustment_event['tenant_id']
        assert len(event_data['items']) == len(stock_adjustment_event['items'])
        
        # Step 4: Handle the event in the sales service
        sales_result = mock_handle_stock_adjustment_event(event_data)
        
        # Verify that the sales service handled the event correctly
        assert sales_result['adjustment_id'] == stock_adjustment_event['adjustment_id']
        assert sales_result['shop_id'] == stock_adjustment_event['shop_id']
        assert sales_result['items_processed'] == len(stock_adjustment_event['items'])
        assert sales_result['stock_updated'] is True
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_stock_adjustment_approval_event(self, mock_get_producer, mock_kafka_producer, 
                                            shop_data, brand_data, user_data):
        """
        Test that when a stock adjustment is approved, the appropriate events are published to Kafka.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        brand_id = brand_data['id']
        user_id = user_data['id']
        tenant_id = user_data['tenant_id']
        adjustment_id = str(uuid.uuid4())
        
        # Create stock adjustment items
        items = [
            {
                'brand_id': brand_id,
                'previous_quantity': 50,
                'new_quantity': 45,
                'reason': 'breakage'
            }
        ]
        
        # Mock the approval of a stock adjustment
        approval_data = {
            'id': adjustment_id,
            'shop_id': shop_id,
            'items': items,
            'status': 'approved',
            'approved_by': user_id,
            'approved_at': timezone.now().isoformat(),
            'tenant_id': tenant_id
        }
        
        # Publish stock adjustment approved event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': approval_data['id'],
            'shop_id': approval_data['shop_id'],
            'tenant_id': approval_data['tenant_id'],
            'items': approval_data['items'],
            'status': approval_data['status'],
            'approved_by': approval_data['approved_by'],
            'approved_at': approval_data['approved_at'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=approval_data['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == approval_data['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert published_event['adjustment_id'] == approval_data['id']
        assert published_event['shop_id'] == approval_data['shop_id']
        assert published_event['tenant_id'] == approval_data['tenant_id']
        assert published_event['status'] == 'approved'
        assert published_event['approved_by'] == approval_data['approved_by']
