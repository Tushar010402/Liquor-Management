import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the goods receipt module.
    """
    logger.info("Starting Kafka consumers for goods receipt module")
    
    # Start consumer for goods receipt events
    try:
        consume_events(
            CONSUMER_GROUPS['PURCHASE_SERVICE'],
            [TOPICS['GOODS_RECEIPT_EVENTS']],
            process_goods_receipt_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for goods receipt events: {str(e)}")

def process_goods_receipt_event(key, event_data):
    """
    Process goods receipt events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['GOODS_RECEIPT_CREATED']:
            logger.info(f"Processing goods receipt created event: {key}")
            # This is handled by the goods receipt module directly
            pass
        
        elif event_type == EVENT_TYPES['GOODS_RECEIPT_APPROVED']:
            logger.info(f"Processing goods receipt approved event: {key}")
            # This is handled by the goods receipt module directly
            pass
        
        elif event_type == EVENT_TYPES['GOODS_RECEIPT_COMPLETED']:
            logger.info(f"Processing goods receipt completed event: {key}")
            # This is handled by the goods receipt module directly
            pass
        
        else:
            logger.warning(f"Unknown goods receipt event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing goods receipt event: {str(e)}")

def publish_goods_receipt_created_event(goods_receipt):
    """
    Publish a goods receipt created event to Kafka.
    
    Args:
        goods_receipt: Goods receipt object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_CREATED'],
            'goods_receipt_id': str(goods_receipt.id),
            'gr_number': goods_receipt.gr_number,
            'shop_id': str(goods_receipt.shop_id),
            'tenant_id': str(goods_receipt.tenant_id),
            'user_id': str(goods_receipt.created_by),
            'supplier_id': str(goods_receipt.supplier_id),
            'purchase_order_id': str(goods_receipt.purchase_order.id) if goods_receipt.purchase_order else None,
            'total_amount': float(goods_receipt.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['GOODS_RECEIPT_EVENTS'], f'goods_receipt:{goods_receipt.id}', event_data)
        logger.info(f"Published goods receipt created event for goods receipt {goods_receipt.id}")
    
    except Exception as e:
        logger.error(f"Error publishing goods receipt created event: {str(e)}")

def publish_goods_receipt_approved_event(goods_receipt):
    """
    Publish a goods receipt approved event to Kafka.
    
    Args:
        goods_receipt: Goods receipt object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_APPROVED'],
            'goods_receipt_id': str(goods_receipt.id),
            'gr_number': goods_receipt.gr_number,
            'shop_id': str(goods_receipt.shop_id),
            'tenant_id': str(goods_receipt.tenant_id),
            'user_id': str(goods_receipt.approved_by),
            'supplier_id': str(goods_receipt.supplier_id),
            'purchase_order_id': str(goods_receipt.purchase_order.id) if goods_receipt.purchase_order else None,
            'total_amount': float(goods_receipt.total_amount),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['GOODS_RECEIPT_EVENTS'], f'goods_receipt:{goods_receipt.id}', event_data)
        logger.info(f"Published goods receipt approved event for goods receipt {goods_receipt.id}")
    
    except Exception as e:
        logger.error(f"Error publishing goods receipt approved event: {str(e)}")

def publish_goods_receipt_completed_event(goods_receipt, items):
    """
    Publish a goods receipt completed event to Kafka.
    
    Args:
        goods_receipt: Goods receipt object.
        items: List of goods receipt items.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['GOODS_RECEIPT_COMPLETED'],
            'goods_receipt_id': str(goods_receipt.id),
            'gr_number': goods_receipt.gr_number,
            'shop_id': str(goods_receipt.shop_id),
            'tenant_id': str(goods_receipt.tenant_id),
            'user_id': str(goods_receipt.created_by),
            'supplier_id': str(goods_receipt.supplier_id),
            'purchase_order_id': str(goods_receipt.purchase_order.id) if goods_receipt.purchase_order else None,
            'total_amount': float(goods_receipt.total_amount),
            'items': items,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['GOODS_RECEIPT_EVENTS'], f'goods_receipt:{goods_receipt.id}', event_data)
        logger.info(f"Published goods receipt completed event for goods receipt {goods_receipt.id}")
    
    except Exception as e:
        logger.error(f"Error publishing goods receipt completed event: {str(e)}")

def publish_quality_check_event(quality_check):
    """
    Publish a quality check event to Kafka.
    
    Args:
        quality_check: Quality check object.
    """
    try:
        event_data = {
            'event_type': 'quality_check_completed',  # Not in EVENT_TYPES yet
            'quality_check_id': str(quality_check.id),
            'check_number': quality_check.check_number,
            'shop_id': str(quality_check.shop_id),
            'tenant_id': str(quality_check.tenant_id),
            'user_id': str(quality_check.checked_by),
            'goods_receipt_id': str(quality_check.goods_receipt.id),
            'status': quality_check.status,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['GOODS_RECEIPT_EVENTS'], f'quality_check:{quality_check.id}', event_data)
        logger.info(f"Published quality check event for quality check {quality_check.id}")
    
    except Exception as e:
        logger.error(f"Error publishing quality check event: {str(e)}")