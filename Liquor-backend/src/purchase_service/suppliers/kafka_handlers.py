import logging
import json
from django.conf import settings
from django.utils import timezone
from common.utils.kafka_utils import consume_events, publish_event
from common.kafka_config import TOPICS, EVENT_TYPES, CONSUMER_GROUPS

logger = logging.getLogger(__name__)

def start_kafka_consumers():
    """
    Start Kafka consumers for the suppliers module.
    """
    logger.info("Starting Kafka consumers for suppliers module")
    
    # Start consumer for supplier events
    try:
        consume_events(
            CONSUMER_GROUPS['PURCHASE_SERVICE'],
            [TOPICS['SUPPLIER_EVENTS']],
            process_supplier_event
        )
    except Exception as e:
        logger.error(f"Error starting Kafka consumer for supplier events: {str(e)}")

def process_supplier_event(key, event_data):
    """
    Process supplier events from Kafka.
    
    Args:
        key (str): Event key.
        event_data (dict): Event data.
    """
    try:
        event_type = event_data.get('event_type')
        
        if event_type == EVENT_TYPES['SUPPLIER_CREATED']:
            logger.info(f"Processing supplier created event: {key}")
            # This is handled by the suppliers module directly
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_UPDATED']:
            logger.info(f"Processing supplier updated event: {key}")
            # This is handled by the suppliers module directly
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_PAYMENT_CREATED']:
            logger.info(f"Processing supplier payment created event: {key}")
            # This is handled by the suppliers module directly
            pass
        
        elif event_type == EVENT_TYPES['SUPPLIER_INVOICE_CREATED']:
            logger.info(f"Processing supplier invoice created event: {key}")
            # This is handled by the suppliers module directly
            pass
        
        else:
            logger.warning(f"Unknown supplier event type: {event_type}")
    
    except Exception as e:
        logger.error(f"Error processing supplier event: {str(e)}")

def publish_supplier_created_event(supplier):
    """
    Publish a supplier created event to Kafka.
    
    Args:
        supplier: Supplier object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SUPPLIER_CREATED'],
            'supplier_id': str(supplier.id),
            'code': supplier.code,
            'name': supplier.name,
            'tenant_id': str(supplier.tenant_id),
            'user_id': str(supplier.created_by),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SUPPLIER_EVENTS'], f'supplier:{supplier.id}', event_data)
        logger.info(f"Published supplier created event for supplier {supplier.id}")
    
    except Exception as e:
        logger.error(f"Error publishing supplier created event: {str(e)}")

def publish_supplier_updated_event(supplier, updated_fields):
    """
    Publish a supplier updated event to Kafka.
    
    Args:
        supplier: Supplier object.
        updated_fields: List of updated fields.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SUPPLIER_UPDATED'],
            'supplier_id': str(supplier.id),
            'code': supplier.code,
            'name': supplier.name,
            'tenant_id': str(supplier.tenant_id),
            'updated_fields': updated_fields,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SUPPLIER_EVENTS'], f'supplier:{supplier.id}', event_data)
        logger.info(f"Published supplier updated event for supplier {supplier.id}")
    
    except Exception as e:
        logger.error(f"Error publishing supplier updated event: {str(e)}")

def publish_supplier_payment_event(payment):
    """
    Publish a supplier payment event to Kafka.
    
    Args:
        payment: Supplier payment object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SUPPLIER_PAYMENT_CREATED'],
            'payment_id': str(payment.id),
            'payment_number': payment.payment_number,
            'supplier_id': str(payment.supplier.id),
            'shop_id': str(payment.shop_id),
            'tenant_id': str(payment.tenant_id),
            'user_id': str(payment.created_by),
            'amount': float(payment.amount),
            'payment_method': payment.payment_method,
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SUPPLIER_EVENTS'], f'payment:{payment.id}', event_data)
        logger.info(f"Published supplier payment event for payment {payment.id}")
    
    except Exception as e:
        logger.error(f"Error publishing supplier payment event: {str(e)}")

def publish_supplier_invoice_event(invoice):
    """
    Publish a supplier invoice event to Kafka.
    
    Args:
        invoice: Supplier invoice object.
    """
    try:
        event_data = {
            'event_type': EVENT_TYPES['SUPPLIER_INVOICE_CREATED'],
            'invoice_id': str(invoice.id),
            'invoice_number': invoice.invoice_number,
            'supplier_id': str(invoice.supplier.id),
            'shop_id': str(invoice.shop_id),
            'tenant_id': str(invoice.tenant_id),
            'user_id': str(invoice.created_by),
            'total_amount': float(invoice.total_amount),
            'due_date': invoice.due_date.isoformat(),
            'timestamp': timezone.now().isoformat()
        }
        
        publish_event(TOPICS['SUPPLIER_EVENTS'], f'invoice:{invoice.id}', event_data)
        logger.info(f"Published supplier invoice event for invoice {invoice.id}")
    
    except Exception as e:
        logger.error(f"Error publishing supplier invoice event: {str(e)}")