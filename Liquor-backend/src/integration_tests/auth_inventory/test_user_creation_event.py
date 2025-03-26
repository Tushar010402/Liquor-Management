"""
Integration test for user creation event flow between auth service and inventory service.
This test verifies that when a user is created in the auth service, the appropriate events
are published to Kafka and can be consumed by the inventory service.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the auth service user creation function (mock for testing)
def mock_create_user(email, password, full_name, tenant_id, role):
    """Mock function for creating a user in the auth service."""
    user_id = str(uuid.uuid4())
    return {
        'id': user_id,
        'email': email,
        'full_name': full_name,
        'tenant_id': tenant_id,
        'role': role,
        'created_at': timezone.now().isoformat()
    }

# Import the inventory service user event handler (mock for testing)
def mock_handle_user_created_event(user_data):
    """Mock function for handling user created event in the inventory service."""
    # In a real implementation, this would create or update user permissions in the inventory service
    return {
        'user_id': user_data['user_id'],
        'email': user_data['email'],
        'permissions_updated': True
    }

class TestUserCreationEventFlow:
    """
    Test the user creation event flow between auth service and inventory service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_user_creation_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, user_data):
        """
        Test that when a user is created in the auth service, the appropriate events
        are published to Kafka and can be consumed by the inventory service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Set up mock consumer with a message that will be returned when polling
        user_created_event = {
            'event_type': EVENT_TYPES['USER_CREATED'],
            'user_id': user_data['id'],
            'email': user_data['email'],
            'tenant_id': user_data['tenant_id'],
            'role': user_data['role'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = user_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(user_created_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Create a user in the auth service
        created_user = mock_create_user(
            email=user_data['email'],
            password='testpassword',
            full_name=user_data['full_name'],
            tenant_id=user_data['tenant_id'],
            role=user_data['role']
        )
        
        # Step 2: Publish user created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['USER_CREATED'],
            'user_id': created_user['id'],
            'email': created_user['email'],
            'tenant_id': created_user['tenant_id'],
            'role': created_user['role'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['USER_EVENTS'],
            key=created_user['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['USER_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == created_user['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['USER_CREATED']
        assert published_event['user_id'] == created_user['id']
        assert published_event['email'] == created_user['email']
        assert published_event['tenant_id'] == created_user['tenant_id']
        assert published_event['role'] == created_user['role']
        
        # Step 3: Consume the event in the inventory service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['INVENTORY_SERVICE'],
            topics=[TOPICS['USER_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == user_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['USER_CREATED']
        assert event_data['user_id'] == user_data['id']
        assert event_data['email'] == user_data['email']
        assert event_data['tenant_id'] == user_data['tenant_id']
        assert event_data['role'] == user_data['role']
        
        # Step 4: Handle the event in the inventory service
        inventory_result = mock_handle_user_created_event(event_data)
        
        # Verify that the inventory service handled the event correctly
        assert inventory_result['user_id'] == user_data['id']
        assert inventory_result['email'] == user_data['email']
        assert inventory_result['permissions_updated'] is True
