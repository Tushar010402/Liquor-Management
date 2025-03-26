"""
Integration test for expiry alert events between inventory service and reporting service.
This test verifies that when products are nearing expiry in the inventory service, the appropriate events
are published to Kafka and can be consumed by the reporting service for analytics and alerts.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the inventory service expiry check function (mock for testing)
def mock_check_expiry(days_threshold=30):
    """Mock function for checking expiry dates in the inventory service."""
    expiring_items = [
        {
            'id': str(uuid.uuid4()),
            'brand_id': str(uuid.uuid4()),
            'shop_id': str(uuid.uuid4()),
            'tenant_id': str(uuid.uuid4()),
            'batch': f'BATCH-{uuid.uuid4().hex[:6]}',
            'quantity': 20,
            'expiry_date': (timezone.now() + timedelta(days=15)).date().isoformat(),  # 15 days to expiry
            'days_to_expiry': 15
        },
        {
            'id': str(uuid.uuid4()),
            'brand_id': str(uuid.uuid4()),
            'shop_id': str(uuid.uuid4()),
            'tenant_id': str(uuid.uuid4()),
            'batch': f'BATCH-{uuid.uuid4().hex[:6]}',
            'quantity': 10,
            'expiry_date': (timezone.now() + timedelta(days=7)).date().isoformat(),  # 7 days to expiry
            'days_to_expiry': 7
        }
    ]
    return expiring_items

# Import the reporting service alert creation function (mock for testing)
def mock_create_expiry_alert(expiry_data):
    """Mock function for creating expiry alerts in the reporting service."""
    alert_id = str(uuid.uuid4())
    return {
        'id': alert_id,
        'type': 'expiry_alert',
        'stock_id': expiry_data['stock_id'],
        'brand_id': expiry_data['brand_id'],
        'shop_id': expiry_data['shop_id'],
        'tenant_id': expiry_data['tenant_id'],
        'batch': expiry_data['batch'],
        'quantity': expiry_data['quantity'],
        'expiry_date': expiry_data['expiry_date'],
        'days_to_expiry': expiry_data['days_to_expiry'],
        'status': 'active',
        'created_at': timezone.now().isoformat()
    }

class TestExpiryAlertEventFlow:
    """
    Test the expiry alert event flow between inventory service and reporting service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_expiry_alert_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer):
        """
        Test that when products are nearing expiry in the inventory service, the appropriate events
        are published to Kafka and can be consumed by the reporting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Check for expiring items in the inventory service
        expiring_items = mock_check_expiry(days_threshold=30)
        
        # We'll test with the first expiring item
        expiring_item = expiring_items[0]
        
        # Set up mock consumer with a message that will be returned when polling
        expiry_alert_event = {
            'event_type': EVENT_TYPES['EXPIRY_ALERT'],
            'alert_id': str(uuid.uuid4()),
            'stock_id': expiring_item['id'],
            'brand_id': expiring_item['brand_id'],
            'shop_id': expiring_item['shop_id'],
            'tenant_id': expiring_item['tenant_id'],
            'batch': expiring_item['batch'],
            'quantity': expiring_item['quantity'],
            'expiry_date': expiring_item['expiry_date'],
            'days_to_expiry': expiring_item['days_to_expiry'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = expiry_alert_event['alert_id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(expiry_alert_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish expiry alert event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['EXPIRY_ALERT'],
            'alert_id': expiry_alert_event['alert_id'],
            'stock_id': expiring_item['id'],
            'brand_id': expiring_item['brand_id'],
            'shop_id': expiring_item['shop_id'],
            'tenant_id': expiring_item['tenant_id'],
            'batch': expiring_item['batch'],
            'quantity': expiring_item['quantity'],
            'expiry_date': expiring_item['expiry_date'],
            'days_to_expiry': expiring_item['days_to_expiry'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['INVENTORY_EVENTS'],
            key=expiry_alert_event['alert_id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['INVENTORY_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == expiry_alert_event['alert_id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['EXPIRY_ALERT']
        assert published_event['stock_id'] == expiring_item['id']
        assert published_event['brand_id'] == expiring_item['brand_id']
        assert published_event['batch'] == expiring_item['batch']
        assert published_event['days_to_expiry'] == expiring_item['days_to_expiry']
        
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
        assert args[0] == expiry_alert_event['alert_id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['EXPIRY_ALERT']
        assert event_data['stock_id'] == expiring_item['id']
        assert event_data['brand_id'] == expiring_item['brand_id']
        assert event_data['days_to_expiry'] == expiring_item['days_to_expiry']
        
        # Step 3: Create an alert in the reporting service
        alert = mock_create_expiry_alert(event_data)
        
        # Verify that the alert was created correctly
        assert alert['type'] == 'expiry_alert'
        assert alert['stock_id'] == expiring_item['id']
        assert alert['brand_id'] == expiring_item['brand_id']
        assert alert['batch'] == expiring_item['batch']
        assert alert['days_to_expiry'] == expiring_item['days_to_expiry']
        assert alert['status'] == 'active'
        
        # Step 4: Publish notification event to Kafka
        notification_id = str(uuid.uuid4())
        notification_event = {
            'event_type': EVENT_TYPES['NOTIFICATION_CREATED'],
            'notification_id': notification_id,
            'alert_id': alert['id'],
            'type': 'expiry_alert',
            'title': 'Product Expiry Alert',
            'message': f'Products in batch {alert["batch"]} will expire in {alert["days_to_expiry"]} days',
            'shop_id': alert['shop_id'],
            'tenant_id': alert['tenant_id'],
            'priority': 'high',
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['NOTIFICATION_EVENTS'],
            key=notification_id,
            event_data=notification_event
        )
        
        # Verify that the notification event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 2
        
        published_message = mock_kafka_producer.messages[1]
        assert published_message['topic'] == TOPICS['NOTIFICATION_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == notification_id
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['NOTIFICATION_CREATED']
        assert published_event['notification_id'] == notification_id
        assert published_event['alert_id'] == alert['id']
        assert published_event['type'] == 'expiry_alert'
        assert 'expire in' in published_event['message']
        assert published_event['priority'] == 'high'

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_batch_expiry_report_generation(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data, shop_data):
        """
        Test that the reporting service can generate batch expiry reports based on inventory data.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Check for expiring items in the inventory service
        expiring_items = mock_check_expiry(days_threshold=30)
        
        # Create a report generation request event
        report_request_id = str(uuid.uuid4())
        report_request_event = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'report_id': report_request_id,
            'report_type': 'expiry_report',
            'tenant_id': tenant_data['id'],
            'shop_id': shop_data['id'],
            'parameters': {
                'days_threshold': 30,
                'format': 'pdf'
            },
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = report_request_id.encode('utf-8')
        mock_message.value.return_value = json.dumps(report_request_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish report request event to Kafka
        from common.utils.kafka_utils import publish_event
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_request_id,
            event_data=report_request_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_request_id
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['REPORT_SCHEDULED']
        assert published_event['report_id'] == report_request_id
        assert published_event['report_type'] == 'expiry_report'
        assert published_event['parameters']['days_threshold'] == 30
        
        # Step 2: Consume the event in the reporting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['REPORTING_SERVICE'],
            topics=[TOPICS['REPORTING_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == report_request_id
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['REPORT_SCHEDULED']
        assert event_data['report_id'] == report_request_id
        assert event_data['report_type'] == 'expiry_report'
        
        # Step 3: Generate the report in the reporting service
        # In a real implementation, this would query the inventory service for expiring items
        # and generate a report. For testing, we'll use our mock data.
        report_data = {
            'id': report_request_id,
            'type': 'expiry_report',
            'tenant_id': tenant_data['id'],
            'shop_id': shop_data['id'],
            'generated_at': timezone.now().isoformat(),
            'parameters': event_data['parameters'],
            'data': {
                'expiring_items': [
                    {
                        'brand_id': item['brand_id'],
                        'batch': item['batch'],
                        'quantity': item['quantity'],
                        'expiry_date': item['expiry_date'],
                        'days_to_expiry': item['days_to_expiry']
                    }
                    for item in expiring_items
                ],
                'total_items': len(expiring_items),
                'total_quantity': sum(item['quantity'] for item in expiring_items)
            },
            'status': 'completed',
            'file_url': f'/reports/{report_request_id}.pdf'
        }
        
        # Step 4: Publish report generated event to Kafka
        report_generated_event = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': report_data['id'],
            'report_type': report_data['type'],
            'tenant_id': report_data['tenant_id'],
            'shop_id': report_data['shop_id'],
            'file_url': report_data['file_url'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['REPORTING_EVENTS'],
            key=report_data['id'],
            event_data=report_generated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 2
        
        published_message = mock_kafka_producer.messages[1]
        assert published_message['topic'] == TOPICS['REPORTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == report_data['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['REPORT_GENERATED']
        assert published_event['report_id'] == report_data['id']
        assert published_event['report_type'] == report_data['type']
        assert published_event['file_url'] == report_data['file_url']
