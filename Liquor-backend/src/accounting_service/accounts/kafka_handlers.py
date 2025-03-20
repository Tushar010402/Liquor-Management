import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the accounts module.
    """
    logger.info("Starting Kafka consumers for accounts module")
    
    # Start consumer for accounting events
    try:
        consume_events(
            CONSUMER_GROUPS['ACCOUNTING_SERVICE'],
            [TOPICS['ACCOUNTING_EVENTS']],
            process_accounting_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for accounting events: {str(e)}")

def process_accounting_event(key, event_data):
    """
    Process accounting events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['FISCAL_YEAR_CREATED']:
            logger.info(f"Processing fiscal year created event: {key}")
            # This is handled by the accounts module directly
            pass
        
        elif event_type == EVENT_TYPES['FISCAL_YEAR_CLOSED']:
            logger.info(f"Processing fiscal year closed event: {key}")
            # This is handled by the accounts module directly
            pass
        
        elif event_type == EVENT_TYPES['ACCOUNTING_PERIOD_CREATED']:
            logger.info(f"Processing accounting period created event: {key}")
            # This is handled by the accounts module directly
            pass
        
        elif event_type == EVENT_TYPES['ACCOUNTING_PERIOD_CLOSED']:
            logger.info(f"Processing accounting period closed event: {key}")
            # This is handled by the accounts module directly
            pass
        
        else:
            logger.warning(f"Unknown accounting event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing accounting event: {str(e)}")

def publish_fiscal_year_created_event(fiscal_year):
    """
    Publish a fiscal year created event to Kafka.
    
    Args:
        fiscal_year: Fiscal year object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['FISCAL_YEAR_CREATED'],
            'fiscal_year_id': str(fiscal_year.id),
            'name': fiscal_year.name,
            'start_date': fiscal_year.start_date.isoformat(),
            'end_date': fiscal_year.end_date.isoformat(),
            'tenant_id': str(fiscal_year.tenant_id),
            'user_id': str(fiscal_year.created_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['ACCOUNTING_EVENTS'], f'fiscal_year:{fiscal_year.id}', event_data)
        logger.info(f"Published fiscal year created event for fiscal year {fiscal_year.id}")
    
    except Exception as e:
        logger.error(f"Error publishing fiscal year created event: {str(e)}")

def publish_fiscal_year_closed_event(fiscal_year):
    """
    Publish a fiscal year closed event to Kafka.
    
    Args:
        fiscal_year: Fiscal year object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['FISCAL_YEAR_CLOSED'],
            'fiscal_year_id': str(fiscal_year.id),
            'name': fiscal_year.name,
            'start_date': fiscal_year.start_date.isoformat(),
            'end_date': fiscal_year.end_date.isoformat(),
            'tenant_id': str(fiscal_year.tenant_id),
            'user_id': str(fiscal_year.closed_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['ACCOUNTING_EVENTS'], f'fiscal_year:{fiscal_year.id}', event_data)
        logger.info(f"Published fiscal year closed event for fiscal year {fiscal_year.id}")
    
    except Exception as e:
        logger.error(f"Error publishing fiscal year closed event: {str(e)}")

def publish_accounting_period_created_event(period):
    """
    Publish an accounting period created event to Kafka.
    
    Args:
        period: Accounting period object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['ACCOUNTING_PERIOD_CREATED'],
            'period_id': str(period.id),
            'name': period.name,
            'start_date': period.start_date.isoformat(),
            'end_date': period.end_date.isoformat(),
            'fiscal_year_id': str(period.fiscal_year.id),
            'tenant_id': str(period.tenant_id),
            'user_id': str(period.created_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['ACCOUNTING_EVENTS'], f'period:{period.id}', event_data)
        logger.info(f"Published accounting period created event for period {period.id}")
    
    except Exception as e:
        logger.error(f"Error publishing accounting period created event: {str(e)}")

def publish_accounting_period_closed_event(period):
    """
    Publish an accounting period closed event to Kafka.
    
    Args:
        period: Accounting period object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['ACCOUNTING_PERIOD_CLOSED'],
            'period_id': str(period.id),
            'name': period.name,
            'start_date': period.start_date.isoformat(),
            'end_date': period.end_date.isoformat(),
            'fiscal_year_id': str(period.fiscal_year.id),
            'tenant_id': str(period.tenant_id),
            'user_id': str(period.closed_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['ACCOUNTING_EVENTS'], f'period:{period.id}', event_data)
        logger.info(f"Published accounting period closed event for period {period.id}")
    
    except Exception as e:
        logger.error(f"Error publishing accounting period closed event: {str(e)}")