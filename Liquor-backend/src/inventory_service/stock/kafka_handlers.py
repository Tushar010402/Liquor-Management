import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the inventory service.
    """
    logger.info("Starting Kafka consumers for inventory service")
    
    # Start consumer for inventory events
    try:
        consume_events(
            CONSUMER_GROUPS['INVENTORY_SERVICE'],
            [TOPICS['INVENTORY_EVENTS'], TOPICS['STOCK_ADJUSTMENT_EVENTS'], TOPICS['STOCK_TRANSFER_EVENTS']],
            process_inventory_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for inventory events: {str(e)}")
    
    # Start consumer for sales events
    try:
        consume_events(
            CONSUMER_GROUPS['INVENTORY_SERVICE'],
            [TOPICS['SALES_EVENTS'], TOPICS['RETURN_EVENTS']],
            process_sales_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for sales events: {str(e)}")
    
    # Start consumer for purchase events
    try:
        consume_events(
            CONSUMER_GROUPS['INVENTORY_SERVICE'],
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
        
        if event_type == EVENT_TYPES['STOCK_ADJUSTED']:
            logger.info(f"Processing stock adjusted event: {key}")
            # Update inventory levels based on stock adjustment
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['STOCK_TRANSFERRED']:
            logger.info(f"Processing stock transferred event: {key}")
            # Update inventory levels based on stock transfer
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['LOW_STOCK_ALERT']:
            logger.info(f"Processing low stock alert event: {key}")
            # Handle low stock alert
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['EXPIRY_ALERT']:
            logger.info(f"Processing expiry alert event: {key}")
            # Handle expiry alert
            # This would be implemented in a real application
            pass
        
        else:
            logger.warning(f"Unknown inventory event type: {event_type}")
    
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
        
        if event_type == EVENT_TYPES['SALE_COMPLETED']:
            logger.info(f"Processing sale completed event: {key}")
            # Update inventory levels based on sale
            # This would be implemented in a real application
            pass
        
        elif event_type == EVENT_TYPES['RETURN_COMPLETED']:
            logger.info(f"Processing return completed event: {key}")
            # Update inventory levels based on return
            # This would be implemented in a real application
            pass
        
        else:
            logger.warning(f"Unknown sales event type: {event_type}")
    
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
            # Update inventory levels based on goods receipt
            # This would be implemented in a real application
            pass
        
        else:
            logger.warning(f"Unknown purchase event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing purchase event: {str(e)}")

def publish_stock_adjusted_event(adjustment, products):
    """
    Publish a stock adjusted event to Kafka.
    
    Args:
        adjustment: Stock adjustment object.
        products: List of adjusted products.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['STOCK_ADJUSTED'],
            'adjustment_id': str(adjustment.id),
            'shop_id': str(adjustment.shop_id),
            'tenant_id': str(adjustment.tenant_id),
            'user_id': str(adjustment.created_by),
            'products': products,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['STOCK_ADJUSTMENT_EVENTS'], f'adjustment:{adjustment.id}', event_data)
        logger.info(f"Published stock adjusted event for adjustment {adjustment.id}")
    
    except Exception as e:
        logger.error(f"Error publishing stock adjusted event: {str(e)}")

def publish_stock_transferred_event(transfer, products):
    """
    Publish a stock transferred event to Kafka.
    
    Args:
        transfer: Stock transfer object.
        products: List of transferred products.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['STOCK_TRANSFERRED'],
            'transfer_id': str(transfer.id),
            'from_shop_id': str(transfer.from_shop_id),
            'to_shop_id': str(transfer.to_shop_id),
            'tenant_id': str(transfer.tenant_id),
            'user_id': str(transfer.created_by),
            'products': products,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['STOCK_TRANSFER_EVENTS'], f'transfer:{transfer.id}', event_data)
        logger.info(f"Published stock transferred event for transfer {transfer.id}")
    
    except Exception as e:
        logger.error(f"Error publishing stock transferred event: {str(e)}")

def publish_low_stock_alert_event(product, shop_id, tenant_id):
    """
    Publish a low stock alert event to Kafka.
    
    Args:
        product: Product object.
        shop_id: Shop ID.
        tenant_id: Tenant ID.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['LOW_STOCK_ALERT'],
            'product_id': str(product.id),
            'product_name': product.name,
            'product_code': product.code,
            'current_stock': float(product.current_stock),
            'min_stock': float(product.min_stock),
            'shop_id': str(shop_id),
            'tenant_id': str(tenant_id),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['INVENTORY_EVENTS'], f'product:{product.id}', event_data)
        logger.info(f"Published low stock alert event for product {product.id}")
    
    except Exception as e:
        logger.error(f"Error publishing low stock alert event: {str(e)}")

def publish_expiry_alert_event(product, batch, shop_id, tenant_id):
    """
    Publish an expiry alert event to Kafka.
    
    Args:
        product: Product object.
        batch: Batch object.
        shop_id: Shop ID.
        tenant_id: Tenant ID.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['EXPIRY_ALERT'],
            'product_id': str(product.id),
            'product_name': product.name,
            'product_code': product.code,
            'batch_number': batch.batch_number,
            'expiry_date': batch.expiry_date.isoformat(),
            'quantity': float(batch.quantity),
            'shop_id': str(shop_id),
            'tenant_id': str(tenant_id),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['INVENTORY_EVENTS'], f'batch:{batch.id}', event_data)
        logger.info(f"Published expiry alert event for batch {batch.id}")
    
    except Exception as e:
        logger.error(f"Error publishing expiry alert event: {str(e)}")