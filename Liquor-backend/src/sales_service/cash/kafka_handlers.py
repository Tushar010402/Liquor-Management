import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the cash module.
    """
    logger.info("Starting Kafka consumers for cash module")
    
    # Start consumer for cash events
    try:
        consume_events(
            CONSUMER_GROUPS['SALES_SERVICE'],
            [TOPICS['CASH_EVENTS']],
            process_cash_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for cash events: {str(e)}")

def process_cash_event(key, event_data):
    """
    Process cash events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['CASH_TRANSACTION_CREATED']:
            logger.info(f"Processing cash transaction created event: {key}")
            # This is handled by the cash module directly
            pass
        
        elif event_type == EVENT_TYPES['DEPOSIT_CREATED']:
            logger.info(f"Processing deposit created event: {key}")
            # This is handled by the cash module directly
            pass
        
        elif event_type == EVENT_TYPES['DEPOSIT_VERIFIED']:
            logger.info(f"Processing deposit verified event: {key}")
            # This is handled by the cash module directly
            pass
        
        elif event_type == EVENT_TYPES['EXPENSE_CREATED']:
            logger.info(f"Processing expense created event: {key}")
            # This is handled by the cash module directly
            pass
        
        elif event_type == EVENT_TYPES['EXPENSE_APPROVED']:
            logger.info(f"Processing expense approved event: {key}")
            # This is handled by the cash module directly
            pass
        
        elif event_type == EVENT_TYPES['DAILY_SUMMARY_CREATED']:
            logger.info(f"Processing daily summary created event: {key}")
            # This is handled by the cash module directly
            pass
        
        else:
            logger.warning(f"Unknown cash event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing cash event: {str(e)}")

def publish_cash_transaction_event(transaction):
    """
    Publish a cash transaction event to Kafka.
    
    Args:
        transaction: Cash transaction object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['CASH_TRANSACTION_CREATED'],
            'transaction_id': str(transaction.id),
            'transaction_number': transaction.transaction_number,
            'transaction_type': transaction.transaction_type,
            'shop_id': str(transaction.shop_id),
            'tenant_id': str(transaction.tenant_id),
            'user_id': str(transaction.created_by),
            'amount': float(transaction.amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['CASH_EVENTS'], f'transaction:{transaction.id}', event_data)
        logger.info(f"Published cash transaction event for transaction {transaction.id}")
    
    except Exception as e:
        logger.error(f"Error publishing cash transaction event: {str(e)}")

def publish_deposit_created_event(deposit):
    """
    Publish a deposit created event to Kafka.
    
    Args:
        deposit: Bank deposit object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['DEPOSIT_CREATED'],
            'deposit_id': str(deposit.id),
            'deposit_number': deposit.deposit_number,
            'shop_id': str(deposit.shop_id),
            'tenant_id': str(deposit.tenant_id),
            'user_id': str(deposit.created_by),
            'amount': float(deposit.amount),
            'bank_name': deposit.bank_name,
            'account_number': deposit.account_number,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['CASH_EVENTS'], f'deposit:{deposit.id}', event_data)
        logger.info(f"Published deposit created event for deposit {deposit.id}")
    
    except Exception as e:
        logger.error(f"Error publishing deposit created event: {str(e)}")

def publish_deposit_verified_event(deposit):
    """
    Publish a deposit verified event to Kafka.
    
    Args:
        deposit: Bank deposit object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['DEPOSIT_VERIFIED'],
            'deposit_id': str(deposit.id),
            'deposit_number': deposit.deposit_number,
            'shop_id': str(deposit.shop_id),
            'tenant_id': str(deposit.tenant_id),
            'user_id': str(deposit.verified_by),
            'amount': float(deposit.amount),
            'bank_name': deposit.bank_name,
            'account_number': deposit.account_number,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['CASH_EVENTS'], f'deposit:{deposit.id}', event_data)
        logger.info(f"Published deposit verified event for deposit {deposit.id}")
    
    except Exception as e:
        logger.error(f"Error publishing deposit verified event: {str(e)}")

def publish_expense_created_event(expense):
    """
    Publish an expense created event to Kafka.
    
    Args:
        expense: Expense object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['EXPENSE_CREATED'],
            'expense_id': str(expense.id),
            'expense_number': expense.expense_number,
            'shop_id': str(expense.shop_id),
            'tenant_id': str(expense.tenant_id),
            'user_id': str(expense.created_by),
            'amount': float(expense.amount),
            'category': expense.category,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['CASH_EVENTS'], f'expense:{expense.id}', event_data)
        logger.info(f"Published expense created event for expense {expense.id}")
    
    except Exception as e:
        logger.error(f"Error publishing expense created event: {str(e)}")

def publish_daily_summary_event(summary):
    """
    Publish a daily summary event to Kafka.
    
    Args:
        summary: Daily summary object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['DAILY_SUMMARY_CREATED'],
            'summary_id': str(summary.id),
            'shop_id': str(summary.shop_id),
            'tenant_id': str(summary.tenant_id),
            'user_id': str(summary.created_by),
            'summary_date': summary.summary_date.isoformat(),
            'opening_balance': float(summary.opening_balance),
            'closing_balance': float(summary.closing_balance),
            'total_sales': float(summary.total_sales),
            'total_returns': float(summary.total_returns),
            'total_expenses': float(summary.total_expenses),
            'total_deposits': float(summary.total_deposits),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['CASH_EVENTS'], f'summary:{summary.id}', event_data)
        logger.info(f"Published daily summary event for summary {summary.id}")
    
    except Exception as e:
        logger.error(f"Error publishing daily summary event: {str(e)}")