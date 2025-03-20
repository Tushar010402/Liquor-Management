import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the reporting service.
    """
    logger.info("Starting Kafka consumers for reporting service")
    
    # Start consumer for reporting events
    try:
        consume_events(
            CONSUMER_GROUPS['REPORTING_SERVICE'],
            [TOPICS['REPORTING_EVENTS']],
            process_reporting_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for reporting events: {str(e)}")
    
    # Start consumer for sales events
    try:
        consume_events(
            CONSUMER_GROUPS['REPORTING_SERVICE'],
            [TOPICS['SALES_EVENTS'], TOPICS['RETURN_EVENTS'], TOPICS['CASH_EVENTS']],
            process_sales_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for sales events: {str(e)}")
    
    # Start consumer for inventory events
    try:
        consume_events(
            CONSUMER_GROUPS['REPORTING_SERVICE'],
            [TOPICS['INVENTORY_EVENTS'], TOPICS['STOCK_ADJUSTMENT_EVENTS'], TOPICS['STOCK_TRANSFER_EVENTS']],
            process_inventory_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for inventory events: {str(e)}")
    
    # Start consumer for purchase events
    try:
        consume_events(
            CONSUMER_GROUPS['REPORTING_SERVICE'],
            [TOPICS['PURCHASE_EVENTS'], TOPICS['GOODS_RECEIPT_EVENTS'], TOPICS['SUPPLIER_EVENTS']],
            process_purchase_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for purchase events: {str(e)}")
    
    # Start consumer for accounting events
    try:
        consume_events(
            CONSUMER_GROUPS['REPORTING_SERVICE'],
            [TOPICS['ACCOUNTING_EVENTS'], TOPICS['JOURNAL_EVENTS']],
            process_accounting_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for accounting events: {str(e)}")

def process_reporting_event(key, event_data):
    """
    Process reporting events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['REPORT_GENERATED']:
            logger.info(f"Processing report generated event: {key}")
            # This is handled by the reporting service directly
            pass
        
        elif event_type == EVENT_TYPES['REPORT_SCHEDULED']:
            logger.info(f"Processing report scheduled event: {key}")
            # This is handled by the reporting service directly
            pass
        
        else:
            logger.warning(f"Unknown reporting event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing reporting event: {str(e)}")

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
            # Update sales reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['RETURN_COMPLETED']:
            logger.info(f"Processing return completed event: {key}")
            # Update sales reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['DAILY_SUMMARY_CREATED']:
            logger.info(f"Processing daily summary created event: {key}")
            # Update sales reports
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring sales event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing sales event: {str(e)}")

def process_inventory_event(key, event_data):
    """
    Process inventory events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['STOCK_ADJUSTED']:
            logger.info(f"Processing stock adjusted event: {key}")
            # Update inventory reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['STOCK_TRANSFERRED']:
            logger.info(f"Processing stock transferred event: {key}")
            # Update inventory reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['LOW_STOCK_ALERT']:
            logger.info(f"Processing low stock alert event: {key}")
            # Update inventory reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['EXPIRY_ALERT']:
            logger.info(f"Processing expiry alert event: {key}")
            # Update inventory reports
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring inventory event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing inventory event: {str(e)}")

def process_purchase_event(key, event_data):
    """
    Process purchase events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['PURCHASE_ORDER_CREATED']:
            logger.info(f"Processing purchase order created event: {key}")
            # Update purchase reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']:
            logger.info(f"Processing goods receipt completed event: {key}")
            # Update purchase reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_PAYMENT_CREATED']:
            logger.info(f"Processing supplier payment created event: {key}")
            # Update purchase reports
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring purchase event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing purchase event: {str(e)}")

def process_accounting_event(key, event_data):
    """
    Process accounting events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['JOURNAL_POSTED']:
            logger.info(f"Processing journal posted event: {key}")
            # Update financial reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['FISCAL_YEAR_CLOSED']:
            logger.info(f"Processing fiscal year closed event: {key}")
            # Update financial reports
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['ACCOUNTING_PERIOD_CLOSED']:
            logger.info(f"Processing accounting period closed event: {key}")
            # Update financial reports
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring accounting event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing accounting event: {str(e)}")

def publish_report_generated_event(report):
    """
    Publish a report generated event to Kafka.
    
    Args:
        report: Report object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['REPORT_GENERATED'],
            'report_id': str(report.id),
            'report_name': report.report_name,
            'report_type': report.report_type,
            'tenant_id': str(report.tenant_id),
            'user_id': str(report.generated_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['REPORTING_EVENTS'], f'report:{report.id}', event_data)
        logger.info(f"Published report generated event for report {report.id}")
    
    except Exception as e:
        logger.error(f"Error publishing report generated event: {str(e)}")

def publish_report_scheduled_event(schedule):
    """
    Publish a report scheduled event to Kafka.
    
    Args:
        schedule: Report schedule object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['REPORT_SCHEDULED'],
            'schedule_id': str(schedule.id),
            'name': schedule.name,
            'report_type': schedule.report_type,
            'frequency': schedule.frequency,
            'next_run_date': schedule.next_run_date.isoformat(),
            'tenant_id': str(schedule.tenant_id),
            'user_id': str(schedule.created_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['REPORTING_EVENTS'], f'schedule:{schedule.id}', event_data)
        logger.info(f"Published report scheduled event for schedule {schedule.id}")
    
    except Exception as e:
        logger.error(f"Error publishing report scheduled event: {str(e)}")