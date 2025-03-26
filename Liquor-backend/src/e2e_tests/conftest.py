"""
Configuration file for end-to-end tests.
This file contains fixtures and utilities for e2e testing.
"""

import os
import pytest
import json
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from confluent_kafka import Producer, Consumer, KafkaError

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Mock Kafka producer for testing
class MockKafkaProducer:
    def __init__(self):
        self.messages = []
        self.callbacks = []
    
    def produce(self, topic, value, key=None, callback=None):
        message = {
            'topic': topic,
            'value': value,
            'key': key
        }
        self.messages.append(message)
        if callback:
            self.callbacks.append(callback)
    
    def flush(self, timeout=None):
        # Simulate successful delivery for all messages
        for callback in self.callbacks:
            callback(None, MockKafkaMessage(topic='test-topic', partition=0, offset=0))
        self.callbacks = []
        return len(self.messages)

# Mock Kafka message for testing
class MockKafkaMessage:
    def __init__(self, topic, partition, offset, error=None, key=None, value=None):
        self._topic = topic
        self._partition = partition
        self._offset = offset
        self._error = error
        self._key = key
        self._value = value
    
    def topic(self):
        return self._topic
    
    def partition(self):
        return self._partition
    
    def offset(self):
        return self._offset
    
    def error(self):
        return self._error
    
    def key(self):
        return self._key
    
    def value(self):
        return self._value

# Mock Kafka consumer for testing
class MockKafkaConsumer:
    def __init__(self, messages=None):
        self.messages = messages or []
        self.subscribed_topics = []
        self.position = 0
    
    def subscribe(self, topics):
        self.subscribed_topics = topics
    
    def poll(self, timeout=None):
        if self.position < len(self.messages):
            message = self.messages[self.position]
            self.position += 1
            return message
        return None
    
    def close(self):
        pass

@pytest.fixture
def mock_kafka_producer():
    """
    Fixture for a mock Kafka producer.
    """
    return MockKafkaProducer()

@pytest.fixture
def mock_kafka_consumer():
    """
    Fixture for a mock Kafka consumer.
    """
    return MockKafkaConsumer()

@pytest.fixture
def mock_kafka_message():
    """
    Fixture for a mock Kafka message.
    """
    def _create_message(topic='test-topic', partition=0, offset=0, error=None, key=None, value=None):
        return MockKafkaMessage(
            topic=topic,
            partition=partition,
            offset=offset,
            error=error,
            key=key,
            value=value
        )
    return _create_message

@pytest.fixture
def tenant_data():
    """
    Fixture for tenant test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'name': 'Test Tenant',
        'slug': 'test-tenant',
        'domain': 'test-tenant.com',
        'status': 'active',
        'business_name': 'Test Business',
        'business_address': '123 Test St, Test City',
        'business_phone': '1234567890',
        'business_email': 'info@test-tenant.com',
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def user_data():
    """
    Fixture for user test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'email': 'test@test-tenant.com',
        'full_name': 'Test User',
        'role': 'manager',
        'tenant_id': str(uuid.uuid4()),
        'is_active': True,
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def shop_data():
    """
    Fixture for shop test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'name': 'Test Shop',
        'address': '456 Shop St, Shop City',
        'phone': '0987654321',
        'email': 'shop@test-tenant.com',
        'tenant_id': str(uuid.uuid4()),
        'status': 'active',
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def brand_data():
    """
    Fixture for brand test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'name': 'Test Brand',
        'category': 'whisky',
        'size': '750ml',
        'regular_price': 500.0,
        'discount_price': 450.0,
        'purchase_price': 400.0,
        'mrp': 550.0,
        'tax_rate': 18.0,
        'tenant_id': str(uuid.uuid4()),
        'status': 'active',
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def stock_data():
    """
    Fixture for stock test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'brand_id': str(uuid.uuid4()),
        'shop_id': str(uuid.uuid4()),
        'quantity': 50,
        'min_level': 10,
        'batch': 'BATCH123',
        'expiry_date': (timezone.now() + timedelta(days=365)).date().isoformat(),
        'tenant_id': str(uuid.uuid4()),
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def sale_data():
    """
    Fixture for sale test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'invoice_number': f'INV-{timezone.now().strftime("%Y%m%d")}-001',
        'shop_id': str(uuid.uuid4()),
        'items': [
            {
                'brand_id': str(uuid.uuid4()),
                'quantity': 2,
                'price_type': 'regular',
                'unit_price': 500.0,
                'total_price': 1000.0,
                'tax_amount': 180.0
            }
        ],
        'subtotal': 1000.0,
        'tax_total': 180.0,
        'grand_total': 1180.0,
        'payment_method': 'cash',
        'status': 'pending',
        'tenant_id': str(uuid.uuid4()),
        'created_by': str(uuid.uuid4()),
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def purchase_order_data():
    """
    Fixture for purchase order test data.
    """
    return {
        'id': str(uuid.uuid4()),
        'po_number': f'PO-{timezone.now().strftime("%Y%m%d")}-001',
        'supplier_id': str(uuid.uuid4()),
        'shop_id': str(uuid.uuid4()),
        'items': [
            {
                'brand_id': str(uuid.uuid4()),
                'quantity': 10,
                'purchase_price': 400.0,
                'total_price': 4000.0
            }
        ],
        'subtotal': 4000.0,
        'tax_amount': 720.0,
        'total_amount': 4720.0,
        'status': 'draft',
        'tenant_id': str(uuid.uuid4()),
        'created_by': str(uuid.uuid4()),
        'created_at': timezone.now().isoformat()
    }

@pytest.fixture
def supplier_data():
    """
    Fixture to provide supplier data for tests.
    """
    return {
        'id': str(uuid.uuid4()),
        'name': 'Test Supplier',
        'contact_name': 'John Supplier',
        'email': 'supplier@example.com',
        'phone': '9876543210',
        'address': '789 Supplier St, Supplier City',
        'tax_id': 'SUPP123456',
        'payment_terms': 'Net 30',
        'tenant_id': str(uuid.uuid4()),
        'shop_id': str(uuid.uuid4()),
        'status': 'active',
        'created_at': timezone.now().isoformat(),
        'updated_at': timezone.now().isoformat()
    }
