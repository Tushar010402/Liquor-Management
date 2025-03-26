"""
Integration test for cash transaction events between sales service and accounting service.
This test verifies that when a cash transaction is created in the sales service, the appropriate events
are published to Kafka and can be consumed by the accounting service to create journal entries.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

# Import the sales service cash transaction creation function (mock for testing)
def mock_create_cash_transaction(shop_id, tenant_id, transaction_type, amount, description, user_id):
    """Mock function for creating a cash transaction in the sales service."""
    transaction_id = str(uuid.uuid4())
    return {
        'id': transaction_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'transaction_type': transaction_type,
        'amount': amount,
        'description': description,
        'created_by': user_id,
        'status': 'completed',
        'created_at': timezone.now().isoformat()
    }

# Import the accounting service journal entry creation function (mock for testing)
def mock_create_journal_entry(transaction_data):
    """Mock function for creating a journal entry in the accounting service."""
    journal_id = str(uuid.uuid4())
    
    # Determine debit and credit accounts based on transaction type
    if transaction_data['transaction_type'] == 'deposit':
        debit_account = 'cash'
        credit_account = 'cash_deposits'
    elif transaction_data['transaction_type'] == 'withdrawal':
        debit_account = 'cash_withdrawals'
        credit_account = 'cash'
    elif transaction_data['transaction_type'] == 'expense':
        debit_account = 'expenses'
        credit_account = 'cash'
    else:
        debit_account = 'cash'
        credit_account = 'other_income'
    
    return {
        'id': journal_id,
        'reference_id': transaction_data['transaction_id'],
        'reference_type': 'cash_transaction',
        'description': transaction_data['description'],
        'amount': transaction_data['amount'],
        'tenant_id': transaction_data['tenant_id'],
        'shop_id': transaction_data['shop_id'],
        'entries': [
            {
                'account_id': debit_account,
                'debit': transaction_data['amount'],
                'credit': 0
            },
            {
                'account_id': credit_account,
                'debit': 0,
                'credit': transaction_data['amount']
            }
        ],
        'status': 'posted',
        'created_at': timezone.now().isoformat()
    }

class TestCashTransactionEventFlow:
    """
    Test the cash transaction event flow between sales service and accounting service.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_cash_deposit_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data, shop_data, user_data):
        """
        Test that when a cash deposit is created in the sales service, the appropriate events
        are published to Kafka and can be consumed by the accounting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a cash deposit transaction
        deposit_data = mock_create_cash_transaction(
            shop_id=shop_data['id'],
            tenant_id=tenant_data['id'],
            transaction_type='deposit',
            amount=5000.0,
            description='Daily deposit to bank',
            user_id=user_data['id']
        )
        
        # Set up mock consumer with a message that will be returned when polling
        cash_transaction_event = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': deposit_data['id'],
            'shop_id': deposit_data['shop_id'],
            'tenant_id': deposit_data['tenant_id'],
            'transaction_type': deposit_data['transaction_type'],
            'amount': deposit_data['amount'],
            'description': deposit_data['description'],
            'status': deposit_data['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = deposit_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(cash_transaction_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish cash transaction created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': deposit_data['id'],
            'shop_id': deposit_data['shop_id'],
            'tenant_id': deposit_data['tenant_id'],
            'transaction_type': deposit_data['transaction_type'],
            'amount': deposit_data['amount'],
            'description': deposit_data['description'],
            'status': deposit_data['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['CASH_EVENTS'],
            key=deposit_data['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['CASH_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == deposit_data['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['CASH_TRANSACTION_CREATED']
        assert published_event['transaction_id'] == deposit_data['id']
        assert published_event['transaction_type'] == 'deposit'
        assert published_event['amount'] == deposit_data['amount']
        
        # Step 2: Consume the event in the accounting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            topics=[TOPICS['CASH_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == deposit_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['CASH_TRANSACTION_CREATED']
        assert event_data['transaction_id'] == deposit_data['id']
        assert event_data['transaction_type'] == 'deposit'
        assert event_data['amount'] == deposit_data['amount']
        
        # Step 3: Create a journal entry in the accounting service
        journal_entry = mock_create_journal_entry(event_data)
        
        # Verify that the journal entry was created correctly
        assert journal_entry['reference_id'] == deposit_data['id']
        assert journal_entry['reference_type'] == 'cash_transaction'
        assert journal_entry['amount'] == deposit_data['amount']
        assert journal_entry['tenant_id'] == deposit_data['tenant_id']
        assert journal_entry['shop_id'] == deposit_data['shop_id']
        assert journal_entry['status'] == 'posted'
        
        # Verify that the journal entries balance (debits = credits)
        total_debits = sum(entry['debit'] for entry in journal_entry['entries'])
        total_credits = sum(entry['credit'] for entry in journal_entry['entries'])
        assert total_debits == total_credits
        
        # For a deposit, cash account should be debited
        assert journal_entry['entries'][0]['account_id'] == 'cash'
        assert journal_entry['entries'][0]['debit'] == deposit_data['amount']
        assert journal_entry['entries'][0]['credit'] == 0
        
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
        assert published_event['reference_type'] == 'cash_transaction'
        assert published_event['amount'] == journal_entry['amount']

    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_cash_expense_event_flow(self, mock_get_consumer, mock_get_producer, mock_kafka_producer, mock_kafka_consumer, tenant_data, shop_data, user_data):
        """
        Test that when a cash expense is created in the sales service, the appropriate events
        are published to Kafka and can be consumed by the accounting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create a cash expense transaction
        expense_data = mock_create_cash_transaction(
            shop_id=shop_data['id'],
            tenant_id=tenant_data['id'],
            transaction_type='expense',
            amount=500.0,
            description='Office supplies',
            user_id=user_data['id']
        )
        
        # Set up mock consumer with a message that will be returned when polling
        cash_transaction_event = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': expense_data['id'],
            'shop_id': expense_data['shop_id'],
            'tenant_id': expense_data['tenant_id'],
            'transaction_type': expense_data['transaction_type'],
            'amount': expense_data['amount'],
            'description': expense_data['description'],
            'status': expense_data['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        # Create a mock message that the consumer will return
        mock_message = MagicMock()
        mock_message.error.return_value = None
        mock_message.key.return_value = expense_data['id'].encode('utf-8')
        mock_message.value.return_value = json.dumps(cash_transaction_event).encode('utf-8')
        
        # Set up the consumer to return our mock message
        mock_kafka_consumer.messages = [mock_message]
        mock_get_consumer.return_value = mock_kafka_consumer
        
        # Step 1: Publish cash transaction created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        event_data = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': expense_data['id'],
            'shop_id': expense_data['shop_id'],
            'tenant_id': expense_data['tenant_id'],
            'transaction_type': expense_data['transaction_type'],
            'amount': expense_data['amount'],
            'description': expense_data['description'],
            'status': expense_data['status'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['CASH_EVENTS'],
            key=expense_data['id'],
            event_data=event_data
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['CASH_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == expense_data['id']
        
        # Decode the published message value
        published_event = json.loads(published_message['value'].decode('utf-8'))
        assert published_event['event_type'] == EVENT_TYPES['CASH_TRANSACTION_CREATED']
        assert published_event['transaction_id'] == expense_data['id']
        assert published_event['transaction_type'] == 'expense'
        assert published_event['amount'] == expense_data['amount']
        
        # Step 2: Consume the event in the accounting service
        from common.utils.kafka_utils import consume_events
        
        # Mock the process_message function
        process_message = MagicMock()
        
        # Call consume_events with our mock process_message function
        consume_events(
            consumer_group=CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            topics=[TOPICS['CASH_EVENTS']],
            process_message=process_message
        )
        
        # Verify that the process_message function was called with the correct arguments
        process_message.assert_called_once()
        args = process_message.call_args[0]
        
        # The first argument should be the message key
        assert args[0] == expense_data['id']
        
        # The second argument should be the event data
        event_data = args[1]
        assert event_data['event_type'] == EVENT_TYPES['CASH_TRANSACTION_CREATED']
        assert event_data['transaction_id'] == expense_data['id']
        assert event_data['transaction_type'] == 'expense'
        assert event_data['amount'] == expense_data['amount']
        
        # Step 3: Create a journal entry in the accounting service
        journal_entry = mock_create_journal_entry(event_data)
        
        # Verify that the journal entry was created correctly
        assert journal_entry['reference_id'] == expense_data['id']
        assert journal_entry['reference_type'] == 'cash_transaction'
        assert journal_entry['amount'] == expense_data['amount']
        assert journal_entry['tenant_id'] == expense_data['tenant_id']
        assert journal_entry['shop_id'] == expense_data['shop_id']
        assert journal_entry['status'] == 'posted'
        
        # Verify that the journal entries balance (debits = credits)
        total_debits = sum(entry['debit'] for entry in journal_entry['entries'])
        total_credits = sum(entry['credit'] for entry in journal_entry['entries'])
        assert total_debits == total_credits
        
        # For an expense, expenses account should be debited and cash credited
        assert journal_entry['entries'][0]['account_id'] == 'expenses'
        assert journal_entry['entries'][0]['debit'] == expense_data['amount']
        assert journal_entry['entries'][1]['account_id'] == 'cash'
        assert journal_entry['entries'][1]['credit'] == expense_data['amount']
        
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
        assert published_event['reference_type'] == 'cash_transaction'
        assert published_event['amount'] == journal_entry['amount']
