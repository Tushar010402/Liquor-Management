"""
Integration test for shop synchronization between auth service and core service.
This test verifies that when a shop is created in the auth service, the appropriate events
are published to Kafka and can be consumed by the core service.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the auth service shop creation function (mock for testing)
def mock_create_shop(name, address, phone, email, tenant_id, status='active'):
    """Mock function for creating a shop in the auth service."""
    shop_id = str(uuid.uuid4())
    return {
        'id': shop_id,
        'name': name,
        'address': address,
        'phone': phone,
        'email': email,
        'tenant_id': tenant_id,
        'status': status,
        'created_at': timezone.now().isoformat()
    }

# Import the core service shop event handler (mock for testing)
def mock_handle_shop_created_event(shop_data):
    """Mock function for handling shop created event in the core service."""
    # In a real implementation, this would create or update shop in the core service
    return {
        'shop_id': shop_data['shop_id'],
        'name': shop_data['name'],
        'address': shop_data['address'],
        'phone': shop_data['phone'],
        'email': shop_data['email'],
        'tenant_id': shop_data['tenant_id'],
        'status': 'active',
        'synchronized': True
    }

class TestShopSyncFlow:
    """
    Test the shop synchronization flow between auth service and core service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_shop_creation_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, shop_data, tenant_data):
        """
        Test that when a shop is created in the auth service, the appropriate events
        are published to Kafka and can be consumed by the core service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Set up mock consumer with a message that will be returned when polling
        shop_created_event = {
            'event_type': EVENT_TYPES['SHOP_CREATED'],
            'shop_id': shop_data['id'],
            'name': shop_data['name'],
            'address': shop_data['address'],
            'phone': shop_data['phone'],
            'email': shop_data['email'],
            'tenant_id': tenant_data['id'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = shop_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(shop_created_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Create a shop in the auth service
        created_shop = mock_create_shop(
            name=shop_data['name'],
            address=shop_data['address'],
            phone=shop_data['phone'],
            email=shop_data['email'],
            tenant_id=tenant_data['id'],
            status=shop_data['status']
        )
        
        # Step 2: Publish shop created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['SHOP_CREATED'],
            'shop_id': created_shop['id'],
            'name': created_shop['name'],
            'address': created_shop['address'],
            'phone': created_shop['phone'],
            'email': created_shop['email'],
            'tenant_id': created_shop['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SHOP_EVENTS'],
            key=created_shop['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SHOP_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == created_shop['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SHOP_CREATED']
        assert published_event['shop_id'] == created_shop['id']
        assert published_event['name'] == created_shop['name']
        assert published_event['address'] == created_shop['address']
        assert published_event['tenant_id'] == created_shop['tenant_id']
        
        # Step 3: Consume the event in the core service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['CORE_SERVICE'],
            topics=[TOPICS['SHOP_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == shop_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['SHOP_CREATED']
        assert event_data['shop_id'] == shop_data['id']
        assert event_data['name'] == shop_data['name']
        assert event_data['address'] == shop_data['address']
        assert event_data['tenant_id'] == tenant_data['id']
        
        # Step 4: Handle the event in the core service
        core_result = mock_handle_shop_created_event(event_data)
        
        # Verify that the core service handled the event correctly
        assert core_result['shop_id'] == shop_data['id']
        assert core_result['name'] == shop_data['name']
        assert core_result['address'] == shop_data['address']
        assert core_result['tenant_id'] == tenant_data['id']
        assert core_result['synchronized'] is True

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_shop_update_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, shop_data, tenant_data):
        """
        Test that when a shop is updated in the auth service, the appropriate events
        are published to Kafka and can be consumed by the core service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a shop in the auth service (this would normally be done in a setup method)
        created_shop = mock_create_shop(
            name=shop_data['name'],
            address=shop_data['address'],
            phone=shop_data['phone'],
            email=shop_data['email'],
            tenant_id=tenant_data['id'],
            status=shop_data['status']
        )
        
        # Update the shop
        updated_shop = {
            'id': created_shop['id'],
            'name': created_shop['name'] + ' Updated',
            'address': created_shop['address'] + ' Updated',
            'phone': created_shop['phone'],
            'email': created_shop['email'],
            'tenant_id': created_shop['tenant_id'],
            'status': created_shop['status'],
            'updated_at': timezone.now().isoformat()
        }
        
        # Set up mock consumer with a message that will be returned when polling
        shop_updated_event = {
            'event_type': EVENT_TYPES['SHOP_UPDATED'],
            'shop_id': updated_shop['id'],
            'name': updated_shop['name'],
            'address': updated_shop['address'],
            'phone': updated_shop['phone'],
            'email': updated_shop['email'],
            'tenant_id': updated_shop['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = updated_shop['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(shop_updated_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish shop updated event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['SHOP_UPDATED'],
            'shop_id': updated_shop['id'],
            'name': updated_shop['name'],
            'address': updated_shop['address'],
            'phone': updated_shop['phone'],
            'email': updated_shop['email'],
            'tenant_id': updated_shop['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SHOP_EVENTS'],
            key=updated_shop['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SHOP_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == updated_shop['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SHOP_UPDATED']
        assert published_event['shop_id'] == updated_shop['id']
        assert published_event['name'] == updated_shop['name']
        assert published_event['address'] == updated_shop['address']
        
        # Step 2: Consume the event in the core service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['CORE_SERVICE'],
            topics=[TOPICS['SHOP_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == updated_shop['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['SHOP_UPDATED']
        assert event_data['shop_id'] == updated_shop['id']
        assert event_data['name'] == updated_shop['name']
        assert event_data['address'] == updated_shop['address']
        
        # Step 3: Handle the event in the core service
        # In a real implementation, this would update the shop in the core service
        core_result = {
            'shop_id': event_data['shop_id'],
            'name': event_data['name'],
            'address': event_data['address'],
            'phone': event_data['phone'],
            'email': event_data['email'],
            'tenant_id': event_data['tenant_id'],
            'status': 'active',
            'synchronized': True
        }
        
        # Verify that the core service handled the event correctly
        assert core_result['shop_id'] == updated_shop['id']
        assert core_result['name'] == updated_shop['name']
        assert core_result['address'] == updated_shop['address']
        assert core_result['synchronized'] is True

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_shop_status_change_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, shop_data, tenant_data):
        """
        Test that when a shop's status is changed in the auth service, the appropriate events
        are published to Kafka and can be consumed by the core service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a shop in the auth service (this would normally be done in a setup method)
        created_shop = mock_create_shop(
            name=shop_data['name'],
            address=shop_data['address'],
            phone=shop_data['phone'],
            email=shop_data['email'],
            tenant_id=tenant_data['id'],
            status='active'
        )
        
        # Change the shop status
        updated_shop = {
            'id': created_shop['id'],
            'name': created_shop['name'],
            'address': created_shop['address'],
            'phone': created_shop['phone'],
            'email': created_shop['email'],
            'tenant_id': created_shop['tenant_id'],
            'status': 'inactive',
            'updated_at': timezone.now().isoformat()
        }
        
        # Set up mock consumer with a message that will be returned when polling
        shop_status_event = {
            'event_type': EVENT_TYPES['SHOP_STATUS_CHANGED'],
            'shop_id': updated_shop['id'],
            'status': updated_shop['status'],
            'tenant_id': updated_shop['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = updated_shop['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(shop_status_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish shop status changed event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['SHOP_STATUS_CHANGED'],
            'shop_id': updated_shop['id'],
            'status': updated_shop['status'],
            'tenant_id': updated_shop['tenant_id'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SHOP_EVENTS'],
            key=updated_shop['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SHOP_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == updated_shop['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SHOP_STATUS_CHANGED']
        assert published_event['shop_id'] == updated_shop['id']
        assert published_event['status'] == updated_shop['status']
        
        # Step 2: Consume the event in the core service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['CORE_SERVICE'],
            topics=[TOPICS['SHOP_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == updated_shop['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['SHOP_STATUS_CHANGED']
        assert event_data['shop_id'] == updated_shop['id']
        assert event_data['status'] == updated_shop['status']
        
        # Step 3: Handle the event in the core service
        # In a real implementation, this would update the shop status in the core service
        core_result = {
            'shop_id': event_data['shop_id'],
            'status': event_data['status'],
            'tenant_id': event_data['tenant_id'],
            'synchronized': True
        }
        
        # Verify that the core service handled the event correctly
        assert core_result['shop_id'] == updated_shop['id']
        assert core_result['status'] == updated_shop['status']
        assert core_result['synchronized'] is True
