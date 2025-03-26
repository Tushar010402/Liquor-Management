"""
Integration test for sales transaction events between sales service and accounting service.
This test verifies that when a sale is completed in the sales service, the appropriate events
are published to Kafka and can be consumed by the accounting service to create journal entries.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the sales service sale completion function (mock for testing)
def mock_complete_sale(sale_id, payment_method, amount_paid, change_amount):
    """Mock function for completing a sale in the sales service."""
    return {
        'id': sale_id,
        'status': 'completed',
        'payment_method': payment_method,
        'amount_paid': amount_paid,
        'change_amount': change_amount,
        'completed_at': timezone.now().isoformat()
    }

# Import the accounting service journal entry creation function (mock for testing)
def mock_create_journal_entry(transaction_data):
    """Mock function for creating a journal entry in the accounting service."""
    journal_id = str(uuid.uuid4())
    return {
        'id': journal_id,
        'reference_id': transaction_data['sale_id'],
        'reference_type': 'sale',
        'description': f"Sale {transaction_data['invoice_number']} - {transaction_data['payment_method']}",
        'amount': transaction_data['grand_total'],
        'tenant_id': transaction_data['tenant_id'],
        'shop_id': transaction_data['shop_id'],
        'entries': [
            {
                'account_id': 'cash',
                'debit': transaction_data['grand_total'],
                'credit': 0
            },
            {
                'account_id': 'sales_revenue',
                'debit': 0,
                'credit': transaction_data['subtotal']
            },
            {
                'account_id': 'sales_tax',
                'debit': 0,
                'credit': transaction_data['tax_total']
            }
        ],
        'status': 'posted',
        'created_at': timezone.now().isoformat()
    }

class TestSalesTransactionEventFlow:
    """
    Test the sales transaction event flow between sales service and accounting service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_sale_completed_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, sale_data, tenant_data, shop_data):
        """
        Test that when a sale is completed in the sales service, the appropriate events
        are published to Kafka and can be consumed by the accounting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Update sale data to completed status
        completed_sale = sale_data.copy()
        completed_sale['status'] = 'completed'
        completed_sale['payment_method'] = 'cash'
        completed_sale['amount_paid'] = 1200.0
        completed_sale['change_amount'] = 20.0
        completed_sale['completed_at'] = timezone.now().isoformat()
        
        # Set up mock consumer with a message that will be returned when polling
        sale_completed_event = {
            'event_type': EVENT_TYPES['SALE_COMPLETED'],
            'sale_id': completed_sale['id'],
            'invoice_number': completed_sale['invoice_number'],
            'shop_id': completed_sale['shop_id'],
            'tenant_id': completed_sale['tenant_id'],
            'subtotal': completed_sale['subtotal'],
            'tax_total': completed_sale['tax_total'],
            'grand_total': completed_sale['grand_total'],
            'payment_method': completed_sale['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = completed_sale['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(sale_completed_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Complete a sale in the sales service
        mock_complete_sale(
            sale_id=completed_sale['id'],
            payment_method=completed_sale['payment_method'],
            amount_paid=completed_sale['amount_paid'],
            change_amount=completed_sale['change_amount']
        )
        
        # Step 2: Publish sale completed event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['SALE_COMPLETED'],
            'sale_id': completed_sale['id'],
            'invoice_number': completed_sale['invoice_number'],
            'shop_id': completed_sale['shop_id'],
            'tenant_id': completed_sale['tenant_id'],
            'subtotal': completed_sale['subtotal'],
            'tax_total': completed_sale['tax_total'],
            'grand_total': completed_sale['grand_total'],
            'payment_method': completed_sale['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['SALES_EVENTS'],
            key=completed_sale['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['SALES_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == completed_sale['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['SALE_COMPLETED']
        assert published_event['sale_id'] == completed_sale['id']
        assert published_event['invoice_number'] == completed_sale['invoice_number']
        assert published_event['grand_total'] == completed_sale['grand_total']
        
        # Step 3: Consume the event in the accounting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            topics=[TOPICS['SALES_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == completed_sale['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['SALE_COMPLETED']
        assert event_data['sale_id'] == completed_sale['id']
        assert event_data['invoice_number'] == completed_sale['invoice_number']
        assert event_data['grand_total'] == completed_sale['grand_total']
        
        # Step 4: Create a journal entry in the accounting service
        journal_entry = mock_create_journal_entry(event_data)
        
        # Verify that the journal entry was created correctly
        assert journal_entry['reference_id'] == completed_sale['id']
        assert journal_entry['reference_type'] == 'sale'
        assert journal_entry['amount'] == completed_sale['grand_total']
        assert journal_entry['tenant_id'] == completed_sale['tenant_id']
        assert journal_entry['shop_id'] == completed_sale['shop_id']
        assert journal_entry['status'] == 'posted'
        
        # Verify that the journal entries balance (debits = credits)
        total_debits = sum(entry['debit'] for entry in journal_entry['entries'])
        total_credits = sum(entry['credit'] for entry in journal_entry['entries'])
        assert total_debits == total_credits
        
        # Step 5: Publish journal created event to Kafka
        journal_created_event = {
            'event_type': EVENT_TYPES['JOURNAL_CREATED'],
            'journal_id': journal_entry['id'],
            'reference_id': journal_entry['reference_id'],
            'reference_type': journal_entry['reference_type'],
            'amount': journal_entry['amount'],
            'tenant_id': journal_entry['tenant_id'],
            'shop_id': journal_entry['shop_id'],
            'status': journal_entry['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['JOURNAL_EVENTS'],
            key=journal_entry['id'],
            event_data=journal_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 2
        
        published_message = mock_kafka_producer.messages[1]
        assert published_message['topic'] == TOPICS['JOURNAL_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['JOURNAL_CREATED']
        assert published_event['journal_id'] == journal_entry['id']
        assert published_event['reference_id'] == journal_entry['reference_id']
        assert published_event['amount'] == journal_entry['amount']

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_sale_refund_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, sale_data, tenant_data, shop_data):
        """
        Test that when a sale is refunded in the sales service, the appropriate events
        are published to Kafka and can be consumed by the accounting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a refund for the sale
        refund_data = {
            'id': str(uuid.uuid4()),
            'sale_id': sale_data['id'],
            'invoice_number': sale_data['invoice_number'],
            'shop_id': sale_data['shop_id'],
            'tenant_id': sale_data['tenant_id'],
            'items': sale_data['items'],
            'subtotal': sale_data['subtotal'],
            'tax_total': sale_data['tax_total'],
            'grand_total': sale_data['grand_total'],
            'refund_reason': 'Customer returned items',
            'status': 'completed',
            'created_by': str(uuid.uuid4()),
            'created_at': timezone.now().isoformat()
        }
        
        # Set up mock consumer with a message that will be returned when polling
        return_completed_event = {
            'event_type': EVENT_TYPES['RETURN_COMPLETED'],
            'return_id': refund_data['id'],
            'sale_id': refund_data['sale_id'],
            'invoice_number': refund_data['invoice_number'],
            'shop_id': refund_data['shop_id'],
            'tenant_id': refund_data['tenant_id'],
            'subtotal': refund_data['subtotal'],
            'tax_total': refund_data['tax_total'],
            'grand_total': refund_data['grand_total'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = refund_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(return_completed_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish return completed event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['RETURN_COMPLETED'],
            'return_id': refund_data['id'],
            'sale_id': refund_data['sale_id'],
            'invoice_number': refund_data['invoice_number'],
            'shop_id': refund_data['shop_id'],
            'tenant_id': refund_data['tenant_id'],
            'subtotal': refund_data['subtotal'],
            'tax_total': refund_data['tax_total'],
            'grand_total': refund_data['grand_total'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['RETURN_EVENTS'],
            key=refund_data['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['RETURN_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == refund_data['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['RETURN_COMPLETED']
        assert published_event['return_id'] == refund_data['id']
        assert published_event['sale_id'] == refund_data['sale_id']
        assert published_event['grand_total'] == refund_data['grand_total']
        
        # Step 2: Consume the event in the accounting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            topics=[TOPICS['RETURN_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == refund_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['RETURN_COMPLETED']
        assert event_data['return_id'] == refund_data['id']
        assert event_data['sale_id'] == refund_data['sale_id']
        assert event_data['grand_total'] == refund_data['grand_total']
        
        # Step 3: Create a journal entry in the accounting service for the refund
        journal_id = str(uuid.uuid4())
        journal_entry = {
            'id': journal_id,
            'reference_id': refund_data['id'],
            'reference_type': 'return',
            'description': f"Refund for Sale {refund_data['invoice_number']}",
            'amount': refund_data['grand_total'],
            'tenant_id': refund_data['tenant_id'],
            'shop_id': refund_data['shop_id'],
            'entries': [
                {
                    'account_id': 'cash',
                    'debit': 0,
                    'credit': refund_data['grand_total']
                },
                {
                    'account_id': 'sales_revenue',
                    'debit': refund_data['subtotal'],
                    'credit': 0
                },
                {
                    'account_id': 'sales_tax',
                    'debit': refund_data['tax_total'],
                    'credit': 0
                }
            ],
            'status': 'posted',
            'created_at': timezone.now().isoformat()
        }
        
        # Verify that the journal entries balance (debits = credits)
        total_debits = sum(entry['debit'] for entry in journal_entry['entries'])
        total_credits = sum(entry['credit'] for entry in journal_entry['entries'])
        assert total_debits == total_credits
        
        # Step 4: Publish journal created event to Kafka
        journal_created_event = {
            'event_type': EVENT_TYPES['JOURNAL_CREATED'],
            'journal_id': journal_entry['id'],
            'reference_id': journal_entry['reference_id'],
            'reference_type': journal_entry['reference_type'],
            'amount': journal_entry['amount'],
            'tenant_id': journal_entry['tenant_id'],
            'shop_id': journal_entry['shop_id'],
            'status': journal_entry['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['JOURNAL_EVENTS'],
            key=journal_entry['id'],
            event_data=journal_created_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 2
        
        published_message = mock_kafka_producer.messages[1]
        assert published_message['topic'] == TOPICS['JOURNAL_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['JOURNAL_CREATED']
        assert published_event['journal_id'] == journal_entry['id']
        assert published_event['reference_id'] == journal_entry['reference_id']
        assert published_event['reference_type'] == 'return'
        assert published_event['amount'] == journal_entry['amount']
