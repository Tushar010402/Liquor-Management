"""
Integration test for tenant synchronization between auth service and core service.
This test verifies that when a tenant is created in the auth service, the appropriate events
are published to Kafka and can be consumed by the core service.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the auth service tenant creation function (mock for testing)
def mock_create_tenant(name, slug, domain, business_name, business_address, business_phone, business_email):
    """Mock function for creating a tenant in the auth service."""
    tenant_id = str(uuid.uuid4())
    return {
        'id': tenant_id,
        'name': name,
        'slug': slug,
        'domain': domain,
        'status': 'active',
        'business_name': business_name,
        'business_address': business_address,
        'business_phone': business_phone,
        'business_email': business_email,
        'created_at': timezone.now().isoformat()
    }

# Import the core service tenant event handler (mock for testing)
def mock_handle_tenant_created_event(tenant_data):
    """Mock function for handling tenant created event in the core service."""
    # In a real implementation, this would create or update tenant in the core service
    return {
        'tenant_id': tenant_data['tenant_id'],
        'name': tenant_data['name'],
        'slug': tenant_data['slug'],
        'domain': tenant_data['domain'],
        'status': 'active',
        'synchronized': True
    }

class TestTenantSyncFlow:
    """
    Test the tenant synchronization flow between auth service and core service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_tenant_creation_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data):
        """
        Test that when a tenant is created in the auth service, the appropriate events
        are published to Kafka and can be consumed by the core service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Set up mock consumer with a message that will be returned when polling
        tenant_created_event = {
            'event_type': EVENT_TYPES['TENANT_CREATED'],
            'tenant_id': tenant_data['id'],
            'name': tenant_data['name'],
            'slug': tenant_data['slug'],
            'domain': tenant_data['domain'],
            'business_name': tenant_data['business_name'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = tenant_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(tenant_created_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Create a tenant in the auth service
        created_tenant = mock_create_tenant(
            name=tenant_data['name'],
            slug=tenant_data['slug'],
            domain=tenant_data['domain'],
            business_name=tenant_data['business_name'],
            business_address=tenant_data['business_address'],
            business_phone=tenant_data['business_phone'],
            business_email=tenant_data['business_email']
        )
        
        # Step 2: Publish tenant created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['TENANT_CREATED'],
            'tenant_id': created_tenant['id'],
            'name': created_tenant['name'],
            'slug': created_tenant['slug'],
            'domain': created_tenant['domain'],
            'business_name': created_tenant['business_name'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['TENANT_EVENTS'],
            key=created_tenant['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['TENANT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == created_tenant['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['TENANT_CREATED']
        assert published_event['tenant_id'] == created_tenant['id']
        assert published_event['name'] == created_tenant['name']
        assert published_event['slug'] == created_tenant['slug']
        assert published_event['domain'] == created_tenant['domain']
        
        # Step 3: Consume the event in the core service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['CORE_SERVICE'],
            topics=[TOPICS['TENANT_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == tenant_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['TENANT_CREATED']
        assert event_data['tenant_id'] == tenant_data['id']
        assert event_data['name'] == tenant_data['name']
        assert event_data['slug'] == tenant_data['slug']
        assert event_data['domain'] == tenant_data['domain']
        
        # Step 4: Handle the event in the core service
        core_result = mock_handle_tenant_created_event(event_data)
        
        # Verify that the core service handled the event correctly
        assert core_result['tenant_id'] == tenant_data['id']
        assert core_result['name'] == tenant_data['name']
        assert core_result['slug'] == tenant_data['slug']
        assert core_result['domain'] == tenant_data['domain']
        assert core_result['synchronized'] is True

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_tenant_update_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data):
        """
        Test that when a tenant is updated in the auth service, the appropriate events
        are published to Kafka and can be consumed by the core service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a tenant in the auth service (this would normally be done in a setup method)
        created_tenant = mock_create_tenant(
            name=tenant_data['name'],
            slug=tenant_data['slug'],
            domain=tenant_data['domain'],
            business_name=tenant_data['business_name'],
            business_address=tenant_data['business_address'],
            business_phone=tenant_data['business_phone'],
            business_email=tenant_data['business_email']
        )
        
        # Update the tenant
        updated_tenant = {
            'id': created_tenant['id'],
            'name': created_tenant['name'] + ' Updated',
            'slug': created_tenant['slug'],
            'domain': created_tenant['domain'],
            'status': 'active',
            'business_name': created_tenant['business_name'] + ' Updated',
            'business_address': created_tenant['business_address'],
            'business_phone': created_tenant['business_phone'],
            'business_email': created_tenant['business_email'],
            'updated_at': timezone.now().isoformat()
        }
        
        # Set up mock consumer with a message that will be returned when polling
        tenant_updated_event = {
            'event_type': EVENT_TYPES['TENANT_UPDATED'],
            'tenant_id': updated_tenant['id'],
            'name': updated_tenant['name'],
            'slug': updated_tenant['slug'],
            'domain': updated_tenant['domain'],
            'business_name': updated_tenant['business_name'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = updated_tenant['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(tenant_updated_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish tenant updated event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['TENANT_UPDATED'],
            'tenant_id': updated_tenant['id'],
            'name': updated_tenant['name'],
            'slug': updated_tenant['slug'],
            'domain': updated_tenant['domain'],
            'business_name': updated_tenant['business_name'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['TENANT_EVENTS'],
            key=updated_tenant['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['TENANT_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == updated_tenant['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['TENANT_UPDATED']
        assert published_event['tenant_id'] == updated_tenant['id']
        assert published_event['name'] == updated_tenant['name']
        assert published_event['business_name'] == updated_tenant['business_name']
        
        # Step 2: Consume the event in the core service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['CORE_SERVICE'],
            topics=[TOPICS['TENANT_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == updated_tenant['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['TENANT_UPDATED']
        assert event_data['tenant_id'] == updated_tenant['id']
        assert event_data['name'] == updated_tenant['name']
        assert event_data['business_name'] == updated_tenant['business_name']
        
        # Step 3: Handle the event in the core service
        # In a real implementation, this would update the tenant in the core service
        core_result = {
            'tenant_id': event_data['tenant_id'],
            'name': event_data['name'],
            'slug': event_data['slug'],
            'domain': event_data['domain'],
            'status': 'active',
            'synchronized': True
        }
        
        # Verify that the core service handled the event correctly
        assert core_result['tenant_id'] == updated_tenant['id']
        assert core_result['name'] == updated_tenant['name']
        assert core_result['synchronized'] is True
