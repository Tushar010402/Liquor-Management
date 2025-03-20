import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the sales service.
    """
    logger.info("Starting Kafka consumers for sales service")
    
    # Start consumer for inventory events
    try:
        consume_events(
            CONSUMER_GROUPS['SALES_SERVICE'],
            [TOPICS['INVENTORY_EVENTS']],
            process_inventory_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for inventory events: {str(e)}")
    
    # Start consumer for sales events
    try:
        consume_events(
            CONSUMER_GROUPS['SALES_SERVICE'],
            [TOPICS['SALES_EVENTS'], TOPICS['RETURN_EVENTS']],
            process_sales_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for sales events: {str(e)}")

def process_inventory_event(key, event_data):
    """
    Process inventory events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['LOW_STOCK_ALERT']:
            logger.info(f"Processing low stock alert event: {key}")
            # Handle low stock alert in sales service
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['EXPIRY_ALERT']:
            logger.info(f"Processing expiry alert event: {key}")
            # Handle expiry alert in sales service
            # This would be implemented in a real application
            pass
        
        else:
            logger.debug(f"Ignoring inventory event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing inventory event: {str(e)}")

def process_sales_event(key, event_data):
    """
    Process sales events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['SALE_CREATED']:
            logger.info(f"Processing sale created event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['SALE_APPROVED']:
            logger.info(f"Processing sale approved event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['SALE_REJECTED']:
            logger.info(f"Processing sale rejected event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['SALE_COMPLETED']:
            logger.info(f"Processing sale completed event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['RETURN_CREATED']:
            logger.info(f"Processing return created event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['RETURN_APPROVED']:
            logger.info(f"Processing return approved event: {key}")
            # This is handled by the sales service directly
            pass
        
        elif event_type == EVENT_TYPES['RETURN_COMPLETED']:
            logger.info(f"Processing return completed event: {key}")
            # This is handled by the sales service directly
            pass
        
        else:
            logger.warning(f"Unknown sales event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing sales event: {str(e)}")

def publish_sale_created_event(sale):
    """
    Publish a sale created event to Kafka.
    
    Args:
        sale: Sale object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SALE_CREATED'],
            'sale_id': str(sale.id),
            'invoice_number': sale.invoice_number,
            'shop_id': str(sale.shop_id),
            'tenant_id': str(sale.tenant_id),
            'user_id': str(sale.created_by),
            'total_amount': float(sale.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SALES_EVENTS'], f'sale:{sale.id}', event_data)
        logger.info(f"Published sale created event for sale {sale.id}")
    
    except Exception as e:
        logger.error(f"Error publishing sale created event: {str(e)}")

def publish_sale_approved_event(sale):
    """
    Publish a sale approved event to Kafka.
    
    Args:
        sale: Sale object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SALE_APPROVED'],
            'sale_id': str(sale.id),
            'invoice_number': sale.invoice_number,
            'shop_id': str(sale.shop_id),
            'tenant_id': str(sale.tenant_id),
            'user_id': str(sale.approved_by),
            'total_amount': float(sale.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SALES_EVENTS'], f'sale:{sale.id}', event_data)
        logger.info(f"Published sale approved event for sale {sale.id}")
    
    except Exception as e:
        logger.error(f"Error publishing sale approved event: {str(e)}")

def publish_sale_completed_event(sale, items):
    """
    Publish a sale completed event to Kafka.
    
    Args:
        sale: Sale object.
        items: List of sale items.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SALE_COMPLETED'],
            'sale_id': str(sale.id),
            'invoice_number': sale.invoice_number,
            'shop_id': str(sale.shop_id),
            'tenant_id': str(sale.tenant_id),
            'user_id': str(sale.created_by),
            'total_amount': float(sale.total_amount),
            'items': items,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SALES_EVENTS'], f'sale:{sale.id}', event_data)
        logger.info(f"Published sale completed event for sale {sale.id}")
    
    except Exception as e:
        logger.error(f"Error publishing sale completed event: {str(e)}")

def publish_return_created_event(return_obj):
    """
    Publish a return created event to Kafka.
    
    Args:
        return_obj: Return object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['RETURN_CREATED'],
            'return_id': str(return_obj.id),
            'return_number': return_obj.return_number,
            'shop_id': str(return_obj.shop_id),
            'tenant_id': str(return_obj.tenant_id),
            'user_id': str(return_obj.created_by),
            'total_amount': float(return_obj.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['RETURN_EVENTS'], f'return:{return_obj.id}', event_data)
        logger.info(f"Published return created event for return {return_obj.id}")
    
    except Exception as e:
        logger.error(f"Error publishing return created event: {str(e)}")

def publish_return_completed_event(return_obj, items):
    """
    Publish a return completed event to Kafka.
    
    Args:
        return_obj: Return object.
        items: List of return items.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['RETURN_COMPLETED'],
            'return_id': str(return_obj.id),
            'return_number': return_obj.return_number,
            'shop_id': str(return_obj.shop_id),
            'tenant_id': str(return_obj.tenant_id),
            'user_id': str(return_obj.created_by),
            'total_amount': float(return_obj.total_amount),
            'items': items,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['RETURN_EVENTS'], f'return:{return_obj.id}', event_data)
        logger.info(f"Published return completed event for return {return_obj.id}")
    
    except Exception as e:
        logger.error(f"Error publishing return completed event: {str(e)}")