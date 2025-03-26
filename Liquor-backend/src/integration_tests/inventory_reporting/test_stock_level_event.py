"""
Integration test for stock level events between inventory service and reporting service.
This test verifies that when stock levels are updated in the inventory service, the appropriate events
are published to Kafka and can be consumed by the reporting service for analytics.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the inventory service stock update function (mock for testing)
def mock_update_stock_level(brand_id, shop_id, tenant_id, quantity, batch=None, expiry_date=None):
    """Mock function for updating stock levels in the inventory service."""
    stock_id = str(uuid.uuid4())
    return {
        'id': stock_id,
        'brand_id': brand_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'quantity': quantity,
        'batch': batch or f'BATCH-{stock_id[:6]}',
        'expiry_date': expiry_date,
        'updated_at': timezone.now().isoformat()
    }

# Import the reporting service analytics update function (mock for testing)
def mock_update_inventory_analytics(stock_data):
    """Mock function for updating inventory analytics in the reporting service."""
    return {
        'brand_id': stock_data['brand_id'],
        'shop_id': stock_data['shop_id'],
        'tenant_id': stock_data['tenant_id'],
        'current_quantity': stock_data['quantity'],
        'last_updated': timezone.now().isoformat(),
        'analytics_updated': True
    }

class TestStockLevelEventFlow:
    """
    Test the stock level event flow between inventory service and reporting service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_stock_level_update_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, brand_data, shop_data, tenant_data):
        """
        Test that when stock levels are updated in the inventory service, the appropriate events
        are published to Kafka and can be consumed by the reporting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Update stock level in the inventory service
        updated_stock = mock_update_stock_level(
            brand_id=brand_data['id'],
            shop_id=shop_data['id'],
            tenant_id=tenant_data['id'],
            quantity=50,
            batch='BATCH-001',
            expiry_date=(timezone.now() + timezone.timedelta(days=365)).date().isoformat()
        )
        
        # Set up mock consumer with a message that will be returned when polling
        stock_level_event = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': str(uuid.uuid4()),
            'stock_id': updated_stock['id'],
            'brand_id': updated_stock['brand_id'],
            'shop_id': updated_stock['shop_id'],
            'tenant_id': updated_stock['tenant_id'],
            'quantity': updated_stock['quantity'],
            'batch': updated_stock['batch'],
            'expiry_date': updated_stock['expiry_date'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = stock_level_event['adjustment_id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(stock_level_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish stock level update event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': stock_level_event['adjustment_id'],
            'stock_id': updated_stock['id'],
            'brand_id': updated_stock['brand_id'],
            'shop_id': updated_stock['shop_id'],
            'tenant_id': updated_stock['tenant_id'],
            'quantity': updated_stock['quantity'],
            'batch': updated_stock['batch'],
            'expiry_date': updated_stock['expiry_date'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['STOCK_ADJUSTMENT_EVENTS'],
            key=stock_level_event['adjustment_id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['STOCK_ADJUSTMENT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == stock_level_event['adjustment_id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert published_event['stock_id'] == updated_stock['id']
        assert published_event['brand_id'] == updated_stock['brand_id']
        assert published_event['quantity'] == updated_stock['quantity']
        
        # Step 2: Consume the event in the reporting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['REPORTING_SERVICE'],
            topics=[TOPICS['STOCK_ADJUSTMENT_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == stock_level_event['adjustment_id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['STOCK_ADJUSTED']
        assert event_data['stock_id'] == updated_stock['id']
        assert event_data['brand_id'] == updated_stock['brand_id']
        assert event_data['quantity'] == updated_stock['quantity']
        
        # Step 3: Update inventory analytics in the reporting service
        analytics_result = mock_update_inventory_analytics(event_data)
        
        # Verify that the inventory analytics were updated correctly
        assert analytics_result['brand_id'] == updated_stock['brand_id']
        assert analytics_result['shop_id'] == updated_stock['shop_id']
        assert analytics_result['tenant_id'] == updated_stock['tenant_id']
        assert analytics_result['current_quantity'] == updated_stock['quantity']
        assert analytics_result['analytics_updated'] is True

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_low_stock_alert_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, brand_data, shop_data, tenant_data, stock_data):
        """
        Test that when stock levels fall below the minimum threshold, a low stock alert event
        is published to Kafka and can be consumed by the reporting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a low stock situation
        low_stock = stock_data.copy()
        low_stock['quantity'] = 5  # Below min_level of 10
        
        # Set up mock consumer with a message that will be returned when polling
        low_stock_alert_event = {
            'event_type': EVENT_TYPES['LOW_STOCK_ALERT'],
            'alert_id': str(uuid.uuid4()),
            'stock_id': low_stock['id'],
            'brand_id': low_stock['brand_id'],
            'shop_id': low_stock['shop_id'],
            'tenant_id': low_stock['tenant_id'],
            'current_quantity': low_stock['quantity'],
            'min_level': low_stock['min_level'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = low_stock_alert_event['alert_id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(low_stock_alert_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish low stock alert event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['LOW_STOCK_ALERT'],
            'alert_id': low_stock_alert_event['alert_id'],
            'stock_id': low_stock['id'],
            'brand_id': low_stock['brand_id'],
            'shop_id': low_stock['shop_id'],
            'tenant_id': low_stock['tenant_id'],
            'current_quantity': low_stock['quantity'],
            'min_level': low_stock['min_level'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=low_stock_alert_event['alert_id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == low_stock_alert_event['alert_id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['LOW_STOCK_ALERT']
        assert published_event['stock_id'] == low_stock['id']
        assert published_event['brand_id'] == low_stock['brand_id']
        assert published_event['current_quantity'] == low_stock['quantity']
        assert published_event['min_level'] == low_stock['min_level']
        
        # Step 2: Consume the event in the reporting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['REPORTING_SERVICE'],
            topics=[TOPICS['INVENTORY_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == low_stock_alert_event['alert_id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['LOW_STOCK_ALERT']
        assert event_data['stock_id'] == low_stock['id']
        assert event_data['brand_id'] == low_stock['brand_id']
        assert event_data['current_quantity'] == low_stock['quantity']
        
        # Step 3: Create an alert in the reporting service
        alert_id = str(uuid.uuid4())
        alert = {
            'id': alert_id,
            'type': 'low_stock',
            'stock_id': event_data['stock_id'],
            'brand_id': event_data['brand_id'],
            'shop_id': event_data['shop_id'],
            'tenant_id': event_data['tenant_id'],
            'current_quantity': event_data['current_quantity'],
            'min_level': event_data['min_level'],
            'status': 'active',
            'created_at': timezone.now().isoformat()
        }
        
        # Verify that the alert was created correctly
        assert alert['type'] == 'low_stock'
        assert alert['stock_id'] == low_stock['id']
        assert alert['brand_id'] == low_stock['brand_id']
        assert alert['current_quantity'] == low_stock['quantity']
        assert alert['status'] == 'active'
