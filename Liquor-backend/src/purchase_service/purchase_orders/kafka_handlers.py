import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the purchase service.
    """
    logger.info("Starting Kafka consumers for purchase service")
    
    # Start consumer for inventory events
    try:
        consume_events(
            CONSUMER_GROUPS['PURCHASE_SERVICE'],
            [TOPICS['INVENTORY_EVENTS']],
            process_inventory_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for inventory events: {str(e)}")
    
    # Start consumer for purchase events
    try:
        consume_events(
            CONSUMER_GROUPS['PURCHASE_SERVICE'],
            [TOPICS['PURCHASE_EVENTS'], TOPICS['GOODS_RECEIPT_EVENTS']],
            process_purchase_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for purchase events: {str(e)}")

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
            # Handle low stock alert in purchase service
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
            # This is handled by the purchase service directly
            pass
        
        elif event_type == EVENT_TYPES['PURCHASE_ORDER_APPROVED']:
            logger.info(f"Processing purchase order approved event: {key}")
            # This is handled by the purchase service directly
            pass
        
        elif event_type == EVENT_TYPES['PURCHASE_ORDER_SENT']:
            logger.info(f"Processing purchase order sent event: {key}")
            # This is handled by the purchase service directly
            pass
        
        elif event_type == EVENT_TYPES['GOODS_RECEIPT_CREATED']:
            logger.info(f"Processing goods receipt created event: {key}")
            # This is handled by the purchase service directly
            pass
        
        elif event_type == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']:
            logger.info(f"Processing goods receipt completed event: {key}")
            # This is handled by the purchase service directly
            pass
        
        else:
            logger.warning(f"Unknown purchase event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing purchase event: {str(e)}")

def publish_purchase_order_created_event(purchase_order):
    """
    Publish a purchase order created event to Kafka.
    
    Args:
        purchase_order: Purchase order object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_CREATED'],
            'purchase_order_id': str(purchase_order.id),
            'po_number': purchase_order.po_number,
            'shop_id': str(purchase_order.shop_id),
            'tenant_id': str(purchase_order.tenant_id),
            'user_id': str(purchase_order.created_by),
            'supplier_id': str(purchase_order.supplier_id),
            'total_amount': float(purchase_order.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['PURCHASE_EVENTS'], f'purchase_order:{purchase_order.id}', event_data)
        logger.info(f"Published purchase order created event for purchase order {purchase_order.id}")
    
    except Exception as e:
        logger.error(f"Error publishing purchase order created event: {str(e)}")

def publish_purchase_order_approved_event(purchase_order):
    """
    Publish a purchase order approved event to Kafka.
    
    Args:
        purchase_order: Purchase order object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_APPROVED'],
            'purchase_order_id': str(purchase_order.id),
            'po_number': purchase_order.po_number,
            'shop_id': str(purchase_order.shop_id),
            'tenant_id': str(purchase_order.tenant_id),
            'user_id': str(purchase_order.approved_by),
            'supplier_id': str(purchase_order.supplier_id),
            'total_amount': float(purchase_order.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['PURCHASE_EVENTS'], f'purchase_order:{purchase_order.id}', event_data)
        logger.info(f"Published purchase order approved event for purchase order {purchase_order.id}")
    
    except Exception as e:
        logger.error(f"Error publishing purchase order approved event: {str(e)}")

def publish_purchase_order_sent_event(purchase_order):
    """
    Publish a purchase order sent event to Kafka.
    
    Args:
        purchase_order: Purchase order object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['PURCHASE_ORDER_SENT'],
            'purchase_order_id': str(purchase_order.id),
            'po_number': purchase_order.po_number,
            'shop_id': str(purchase_order.shop_id),
            'tenant_id': str(purchase_order.tenant_id),
            'user_id': str(purchase_order.created_by),
            'supplier_id': str(purchase_order.supplier_id),
            'total_amount': float(purchase_order.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['PURCHASE_EVENTS'], f'purchase_order:{purchase_order.id}', event_data)
        logger.info(f"Published purchase order sent event for purchase order {purchase_order.id}")
    
    except Exception as e:
        logger.error(f"Error publishing purchase order sent event: {str(e)}")