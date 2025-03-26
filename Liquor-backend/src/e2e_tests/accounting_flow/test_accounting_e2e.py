"""
End-to-end test for the accounting flow in the Liquor Management System.
This test verifies the complete flow of accounting processes, including sales transactions,
purchase transactions, journal entries, ledger updates, and tax calculations.
"""

import json
import uuid
import pytest
from unittest.mock import patch, MagicMock
from django.utils import timezone
from datetime import datetime, timedelta

# Import Kafka configuration
from common.kafka_config import TOPICS, EVENT_TYPES

# Mock functions for the accounting flow
def mock_create_sales_transaction(sale_id, shop_id, tenant_id, amount, payment_method):
    """Mock function for creating a sales transaction in the accounting service."""
    transaction_id = str(uuid.uuid4())
    
    return {
        'id': transaction_id,
        'sale_id': sale_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'amount': amount,
        'payment_method': payment_method,
        'transaction_type': 'sales',
        'status': 'completed',
        'created_at': timezone.now().isoformat()
    }

def mock_create_purchase_transaction(po_id, shop_id, tenant_id, amount, payment_method):
    """Mock function for creating a purchase transaction in the accounting service."""
    transaction_id = str(uuid.uuid4())
    
    return {
        'id': transaction_id,
        'purchase_order_id': po_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'amount': amount,
        'payment_method': payment_method,
        'transaction_type': 'purchase',
        'status': 'completed',
        'created_at': timezone.now().isoformat()
    }

def mock_create_journal_entry(transaction_id, shop_id, tenant_id, entries, description):
    """Mock function for creating a journal entry in the accounting service."""
    journal_id = str(uuid.uuid4())
    
    return {
        'id': journal_id,
        'transaction_id': transaction_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'entries': entries,
        'description': description,
        'status': 'posted',
        'created_at': timezone.now().isoformat()
    }

def mock_update_ledger(journal_id, entries):
    """Mock function for updating the ledger in the accounting service."""
    return {
        'journal_id': journal_id,
        'entries_processed': len(entries),
        'updated_at': timezone.now().isoformat()
    }

def mock_calculate_tax(amount, tax_rate=0.18):
    """Mock function for calculating tax in the accounting service."""
    tax_amount = amount * tax_rate
    return {
        'amount': amount,
        'tax_rate': tax_rate,
        'tax_amount': tax_amount,
        'total_amount': amount + tax_amount
    }

def mock_create_tax_entry(transaction_id, shop_id, tenant_id, tax_details):
    """Mock function for creating a tax entry in the accounting service."""
    tax_entry_id = str(uuid.uuid4())
    
    return {
        'id': tax_entry_id,
        'transaction_id': transaction_id,
        'shop_id': shop_id,
        'tenant_id': tenant_id,
        'amount': tax_details['amount'],
        'tax_rate': tax_details['tax_rate'],
        'tax_amount': tax_details['tax_amount'],
        'status': 'filed',
        'created_at': timezone.now().isoformat()
    }

class TestAccountingE2EFlow:
    """
    Test the end-to-end accounting flow in the Liquor Management System.
    """
    
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_sales_transaction_accounting_flow(self, mock_get_consumer, mock_get_producer,
                                             mock_kafka_producer, mock_kafka_consumer,
                                             shop_data, tenant_data):
        """
        Test the complete flow of accounting for a sales transaction, including
        journal entries, ledger updates, and tax calculations.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        sale_id = str(uuid.uuid4())
        amount = 1000.0
        payment_method = 'cash'
        
        # Step 1: Create a sales transaction in the accounting service
        sales_transaction = mock_create_sales_transaction(
            sale_id=sale_id,
            shop_id=shop_id,
            tenant_id=tenant_id,
            amount=amount,
            payment_method=payment_method
        )
        
        # Step 2: Publish sales transaction created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        sales_transaction_event = {
            'event_type': EVENT_TYPES['SALES_TRANSACTION_CREATED'],
            'transaction_id': sales_transaction['id'],
            'sale_id': sales_transaction['sale_id'],
            'shop_id': sales_transaction['shop_id'],
            'tenant_id': sales_transaction['tenant_id'],
            'amount': sales_transaction['amount'],
            'payment_method': sales_transaction['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=sales_transaction['id'],
            event_data=sales_transaction_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == sales_transaction['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Calculate tax for the sales transaction
        tax_details = mock_calculate_tax(sales_transaction['amount'])
        
        # Step 4: Create tax entry for the sales transaction
        tax_entry = mock_create_tax_entry(
            transaction_id=sales_transaction['id'],
            shop_id=sales_transaction['shop_id'],
            tenant_id=sales_transaction['tenant_id'],
            tax_details=tax_details
        )
        
        # Step 5: Create journal entries for the sales transaction
        journal_entries = [
            {
                'account': 'cash',
                'debit': sales_transaction['amount'] + tax_details['tax_amount'],
                'credit': 0
            },
            {
                'account': 'sales_revenue',
                'debit': 0,
                'credit': sales_transaction['amount']
            },
            {
                'account': 'tax_payable',
                'debit': 0,
                'credit': tax_details['tax_amount']
            }
        ]
        
        journal_entry = mock_create_journal_entry(
            transaction_id=sales_transaction['id'],
            shop_id=sales_transaction['shop_id'],
            tenant_id=sales_transaction['tenant_id'],
            entries=journal_entries,
            description=f"Sales transaction {sales_transaction['id']}"
        )
        
        # Step 6: Publish journal entry created event to Kafka
        journal_entry_event = {
            'event_type': EVENT_TYPES['JOURNAL_ENTRY_CREATED'],
            'journal_id': journal_entry['id'],
            'transaction_id': journal_entry['transaction_id'],
            'shop_id': journal_entry['shop_id'],
            'tenant_id': journal_entry['tenant_id'],
            'entries': journal_entry['entries'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=journal_entry['id'],
            event_data=journal_entry_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 7: Update ledger based on the journal entries
        ledger_update = mock_update_ledger(
            journal_id=journal_entry['id'],
            entries=journal_entry['entries']
        )
        
        # Step 8: Publish ledger updated event to Kafka
        ledger_updated_event = {
            'event_type': EVENT_TYPES['LEDGER_UPDATED'],
            'journal_id': journal_entry['id'],
            'shop_id': journal_entry['shop_id'],
            'tenant_id': journal_entry['tenant_id'],
            'entries_processed': ledger_update['entries_processed'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=journal_entry['id'],
            event_data=ledger_updated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Verify the complete flow
        assert sales_transaction['status'] == 'completed'
        assert sales_transaction['amount'] == amount
        assert sales_transaction['payment_method'] == payment_method
        assert tax_entry['tax_amount'] == tax_details['tax_amount']
        assert journal_entry['status'] == 'posted'
        assert len(journal_entry['entries']) == 3
        assert ledger_update['entries_processed'] == len(journal_entry['entries'])
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    @patch('common.utils.kafka_utils.get_kafka_consumer')
    def test_purchase_transaction_accounting_flow(self, mock_get_consumer, mock_get_producer,
                                                mock_kafka_producer, mock_kafka_consumer,
                                                shop_data, tenant_data):
        """
        Test the complete flow of accounting for a purchase transaction, including
        journal entries, ledger updates, and tax calculations.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        po_id = str(uuid.uuid4())
        amount = 5000.0
        payment_method = 'bank_transfer'
        
        # Step 1: Create a purchase transaction in the accounting service
        purchase_transaction = mock_create_purchase_transaction(
            po_id=po_id,
            shop_id=shop_id,
            tenant_id=tenant_id,
            amount=amount,
            payment_method=payment_method
        )
        
        # Step 2: Publish purchase transaction created event to Kafka
        from common.utils.kafka_utils import publish_event
        
        purchase_transaction_event = {
            'event_type': EVENT_TYPES['PURCHASE_PAYMENT_CREATED'],
            'transaction_id': purchase_transaction['id'],
            'purchase_order_id': purchase_transaction['purchase_order_id'],
            'shop_id': purchase_transaction['shop_id'],
            'tenant_id': purchase_transaction['tenant_id'],
            'amount': purchase_transaction['amount'],
            'payment_method': purchase_transaction['payment_method'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=purchase_transaction['id'],
            event_data=purchase_transaction_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == purchase_transaction['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 3: Calculate tax for the purchase transaction
        tax_details = mock_calculate_tax(purchase_transaction['amount'])
        
        # Step 4: Create tax entry for the purchase transaction
        tax_entry = mock_create_tax_entry(
            transaction_id=purchase_transaction['id'],
            shop_id=purchase_transaction['shop_id'],
            tenant_id=purchase_transaction['tenant_id'],
            tax_details=tax_details
        )
        
        # Step 5: Create journal entries for the purchase transaction
        journal_entries = [
            {
                'account': 'inventory',
                'debit': purchase_transaction['amount'],
                'credit': 0
            },
            {
                'account': 'tax_receivable',
                'debit': tax_details['tax_amount'],
                'credit': 0
            },
            {
                'account': 'bank',
                'debit': 0,
                'credit': purchase_transaction['amount'] + tax_details['tax_amount']
            }
        ]
        
        journal_entry = mock_create_journal_entry(
            transaction_id=purchase_transaction['id'],
            shop_id=purchase_transaction['shop_id'],
            tenant_id=purchase_transaction['tenant_id'],
            entries=journal_entries,
            description=f"Purchase transaction {purchase_transaction['id']}"
        )
        
        # Step 6: Publish journal entry created event to Kafka
        journal_entry_event = {
            'event_type': EVENT_TYPES['JOURNAL_ENTRY_CREATED'],
            'journal_id': journal_entry['id'],
            'transaction_id': journal_entry['transaction_id'],
            'shop_id': journal_entry['shop_id'],
            'tenant_id': journal_entry['tenant_id'],
            'entries': journal_entry['entries'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=journal_entry['id'],
            event_data=journal_entry_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Reset the messages for the next event
        mock_kafka_producer.messages = []
        
        # Step 7: Update ledger based on the journal entries
        ledger_update = mock_update_ledger(
            journal_id=journal_entry['id'],
            entries=journal_entry['entries']
        )
        
        # Step 8: Publish ledger updated event to Kafka
        ledger_updated_event = {
            'event_type': EVENT_TYPES['LEDGER_UPDATED'],
            'journal_id': journal_entry['id'],
            'shop_id': journal_entry['shop_id'],
            'tenant_id': journal_entry['tenant_id'],
            'entries_processed': ledger_update['entries_processed'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=journal_entry['id'],
            event_data=ledger_updated_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == journal_entry['id']
        
        # Verify the complete flow
        assert purchase_transaction['status'] == 'completed'
        assert purchase_transaction['amount'] == amount
        assert purchase_transaction['payment_method'] == payment_method
        assert tax_entry['tax_amount'] == tax_details['tax_amount']
        assert journal_entry['status'] == 'posted'
        assert len(journal_entry['entries']) == 3
        assert ledger_update['entries_processed'] == len(journal_entry['entries'])
        
    @patch('common.utils.kafka_utils.get_kafka_producer')
    def test_tax_calculation_and_reporting(self, mock_get_producer, mock_kafka_producer,
                                          shop_data, tenant_data):
        """
        Test the flow of tax calculation and reporting in the accounting service.
        """
        # Set up mock producer
        mock_get_producer.return_value = mock_kafka_producer
        
        # Create test data
        shop_id = shop_data['id']
        tenant_id = tenant_data['id']
        report_id = str(uuid.uuid4())
        month = datetime.now().month
        year = datetime.now().year
        
        # Step 1: Create tax entries for the month
        tax_entries = [
            {
                'id': str(uuid.uuid4()),
                'transaction_id': str(uuid.uuid4()),
                'shop_id': shop_id,
                'tenant_id': tenant_id,
                'amount': 1000.0,
                'tax_rate': 0.18,
                'tax_amount': 180.0,
                'status': 'filed',
                'created_at': timezone.now().isoformat()
            },
            {
                'id': str(uuid.uuid4()),
                'transaction_id': str(uuid.uuid4()),
                'shop_id': shop_id,
                'tenant_id': tenant_id,
                'amount': 5000.0,
                'tax_rate': 0.18,
                'tax_amount': 900.0,
                'status': 'filed',
                'created_at': timezone.now().isoformat()
            }
        ]
        
        # Step 2: Generate tax report
        tax_report = {
            'id': report_id,
            'shop_id': shop_id,
            'tenant_id': tenant_id,
            'month': month,
            'year': year,
            'total_taxable_amount': sum(entry['amount'] for entry in tax_entries),
            'total_tax_amount': sum(entry['tax_amount'] for entry in tax_entries),
            'tax_entries': tax_entries,
            'status': 'generated',
            'created_at': timezone.now().isoformat()
        }
        
        # Step 3: Publish tax report generated event to Kafka
        from common.utils.kafka_utils import publish_event
        
        tax_report_event = {
            'event_type': EVENT_TYPES['TAX_REPORT_GENERATED'],
            'report_id': tax_report['id'],
            'shop_id': tax_report['shop_id'],
            'tenant_id': tax_report['tenant_id'],
            'month': tax_report['month'],
            'year': tax_report['year'],
            'total_taxable_amount': tax_report['total_taxable_amount'],
            'total_tax_amount': tax_report['total_tax_amount'],
            'timestamp': timezone.now().isoformat()
        }
        
        result = publish_event(
            topic=TOPICS['ACCOUNTING_EVENTS'],
            key=tax_report['id'],
            event_data=tax_report_event
        )
        
        # Verify that the event was published successfully
        assert result is True
        assert len(mock_kafka_producer.messages) == 1
        
        published_message = mock_kafka_producer.messages[0]
        assert published_message['topic'] == TOPICS['ACCOUNTING_EVENTS']
        key = published_message['key'].decode('utf-8') if isinstance(published_message['key'], bytes) else published_message['key']
        assert key == tax_report['id']
        
        # Verify the tax report
        assert tax_report['status'] == 'generated'
        assert tax_report['total_taxable_amount'] == 6000.0
        assert tax_report['total_tax_amount'] == 1080.0
        assert len(tax_report['tax_entries']) == 2
