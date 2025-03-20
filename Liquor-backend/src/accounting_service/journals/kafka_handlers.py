import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the journals module.
    """
    logger.info("Starting Kafka consumers for journals module")
    
    # Start consumer for journal events
    try:
        consume_events(
            CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            [TOPICS['JOURNAL_EVENTS']],
            process_journal_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for journal events: {str(e)}")
    
    # Start consumer for sales events
    try:
        consume_events(
            CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            [TOPICS['SALES_EVENTS'], TOPICS['RETURN_EVENTS'], TOPICS['CASH_EVENTS']],
            process_sales_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for sales events: {str(e)}")
    
    # Start consumer for purchase events
    try:
        consume_events(
            CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            [TOPICS['PURCHASE_EVENTS'], TOPICS['GOODS_RECEIPT_EVENTS'], TOPICS['SUPPLIER_EVENTS']],
            process_purchase_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for purchase events: {str(e)}")

def process_journal_event(key, event_data):
    """
    Process journal events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['JOURNAL_CREATED']:
            logger.info(f"Processing journal created event: {key}")
            # This is handled by the journals module directly
            pass
        
        elif event_type == EVENT_TYPES['JOURNAL_POSTED']:
            logger.info(f"Processing journal posted event: {key}")
            # This is handled by the journals module directly
            pass
        
        elif event_type == EVENT_TYPES['JOURNAL_REVERSED']:
            logger.info(f"Processing journal reversed event: {key}")
            # This is handled by the journals module directly
            pass
        
        else:
            logger.warning(f"Unknown journal event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing journal event: {str(e)}")

def process_sales_event(key, event_data):
    """
    Process sales events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['SALE_COMPLETED']:
            logger.info(f"Processing sale completed event: {key}")
            # Create journal entry for sale
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['RETURN_COMPLETED']:
            logger.info(f"Processing return completed event: {key}")
            # Create journal entry for return
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['CASH_TRANSACTION_CREATED']:
            logger.info(f"Processing cash transaction created event: {key}")
            # Create journal entry for cash transaction
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['DEPOSIT_VERIFIED']:
            logger.info(f"Processing deposit verified event: {key}")
            # Create journal entry for deposit
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['EXPENSE_APPROVED']:
            logger.info(f"Processing expense approved event: {key}")
            # Create journal entry for expense
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring sales event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing sales event: {str(e)}")

def process_purchase_event(key, event_data):
    """
    Process purchase events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']:
            logger.info(f"Processing goods receipt completed event: {key}")
            # Create journal entry for goods receipt
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_PAYMENT_CREATED']:
            logger.info(f"Processing supplier payment created event: {key}")
            # Create journal entry for supplier payment
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_INVOICE_CREATED']:
            logger.info(f"Processing supplier invoice created event: {key}")
            # Create journal entry for supplier invoice
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring purchase event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing purchase event: {str(e)}")

def publish_journal_created_event(journal):
    """
    Publish a journal created event to Kafka.
    
    Args:
        journal: Journal object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['JOURNAL_CREATED'],
            'journal_id': str(journal.id),
            'journal_number': journal.journal_number,
            'journal_type': journal.journal_type,
            'tenant_id': str(journal.tenant_id),
            'user_id': str(journal.created_by),
            'total_amount': float(journal.total_debit),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['JOURNAL_EVENTS'], f'journal:{journal.id}', event_data)
        logger.info(f"Published journal created event for journal {journal.id}")
    
    except Exception as e:
        logger.error(f"Error publishing journal created event: {str(e)}")

def publish_journal_posted_event(journal):
    """
    Publish a journal posted event to Kafka.
    
    Args:
        journal: Journal object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['JOURNAL_POSTED'],
            'journal_id': str(journal.id),
            'journal_number': journal.journal_number,
            'journal_type': journal.journal_type,
            'tenant_id': str(journal.tenant_id),
            'user_id': str(journal.posted_by),
            'total_amount': float(journal.total_debit),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['JOURNAL_EVENTS'], f'journal:{journal.id}', event_data)
        logger.info(f"Published journal posted event for journal {journal.id}")
    
    except Exception as e:
        logger.error(f"Error publishing journal posted event: {str(e)}")

def publish_journal_reversed_event(journal):
    """
    Publish a journal reversed event to Kafka.
    
    Args:
        journal: Journal object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['JOURNAL_REVERSED'],
            'journal_id': str(journal.id),
            'journal_number': journal.journal_number,
            'journal_type': journal.journal_type,
            'tenant_id': str(journal.tenant_id),
            'user_id': str(journal.reversed_by),
            'total_amount': float(journal.total_debit),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['JOURNAL_EVENTS'], f'journal:{journal.id}', event_data)
        logger.info(f"Published journal reversed event for journal {journal.id}")
    
    except Exception as e:
        logger.error(f"Error publishing journal reversed event: {str(e)}")