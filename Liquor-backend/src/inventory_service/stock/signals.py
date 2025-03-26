from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import (
    StockLevel, StockTransaction, StockTransfer, StockTransferItem,
    StockAdjustment, StockAdjustmentItem
)

@receiver(post_save, sender=StockLevel)
def stock_level_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockLevel post_save event.
    Publishes stock level events to Kafka.
    """
    if created:
        # Stock level created event
        event_data = {
            'event_type': 'stock_level_created',
            'stock_level_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'current_stock': instance.current_stock,
            'minimum_stock': instance.minimum_stock,
            'maximum_stock': instance.maximum_stock,
            'is_low_stock': instance.is_low_stock,
            'is_out_of_stock': instance.is_out_of_stock
        }
    else:
        # Stock level updated event
        event_data = {
            'event_type': 'stock_level_updated',
            'stock_level_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'current_stock': instance.current_stock,
            'minimum_stock': instance.minimum_stock,
            'maximum_stock': instance.maximum_stock,
            'is_low_stock': instance.is_low_stock,
            'is_out_of_stock': instance.is_out_of_stock
        }
    
    publish_event('inventory-events', f'stock-level:{instance.id}', event_data)

@receiver(post_save, sender=StockTransaction)
def stock_transaction_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockTransaction post_save event.
    Publishes stock transaction events to Kafka.
    """
    if created:
        # Stock transaction created event
        event_data = {
            'event_type': 'stock_transaction_created',
            'transaction_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'transaction_type': instance.transaction_type,
            'quantity': instance.quantity,
            'reference_id': str(instance.reference_id) if instance.reference_id else None,
            'reference_type': instance.reference_type
        }
        
        publish_event('inventory-events', f'stock-transaction:{instance.id}', event_data)

@receiver(post_save, sender=StockTransfer)
def stock_transfer_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockTransfer post_save event.
    Publishes stock transfer events to Kafka.
    """
    if created:
        # Stock transfer created event
        event_data = {
            'event_type': 'stock_transfer_created',
            'transfer_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'source_shop_id': str(instance.source_shop_id),
            'destination_shop_id': str(instance.destination_shop_id),
            'transfer_date': instance.transfer_date.isoformat(),
            'status': instance.status,
            'reference_number': instance.reference_number
        }
    else:
        # Stock transfer updated event
        event_data = {
            'event_type': 'stock_transfer_updated',
            'transfer_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'source_shop_id': str(instance.source_shop_id),
            'destination_shop_id': str(instance.destination_shop_id),
            'transfer_date': instance.transfer_date.isoformat(),
            'status': instance.status,
            'reference_number': instance.reference_number
        }
    
    publish_event('inventory-events', f'stock-transfer:{instance.id}', event_data)

@receiver(post_save, sender=StockTransferItem)
def stock_transfer_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockTransferItem post_save event.
    Publishes stock transfer item events to Kafka.
    """
    if created:
        # Stock transfer item created event
        event_data = {
            'event_type': 'stock_transfer_item_created',
            'transfer_id': str(instance.transfer.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'quantity': instance.quantity
        }
    else:
        # Stock transfer item updated event
        event_data = {
            'event_type': 'stock_transfer_item_updated',
            'transfer_id': str(instance.transfer.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'quantity': instance.quantity,
            'received_quantity': instance.received_quantity,
            'is_received': instance.is_received
        }
    
    publish_event('inventory-events', f'stock-transfer-item:{instance.id}', event_data)

@receiver(post_save, sender=StockAdjustment)
def stock_adjustment_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockAdjustment post_save event.
    Publishes stock adjustment events to Kafka.
    """
    if created:
        # Stock adjustment created event
        event_data = {
            'event_type': 'stock_adjustment_created',
            'adjustment_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'adjustment_date': instance.adjustment_date.isoformat(),
            'adjustment_type': instance.adjustment_type,
            'reference_number': instance.reference_number
        }
        
        publish_event('inventory-events', f'stock-adjustment:{instance.id}', event_data)

@receiver(post_save, sender=StockAdjustmentItem)
def stock_adjustment_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StockAdjustmentItem post_save event.
    Publishes stock adjustment item events to Kafka.
    """
    if created:
        # Stock adjustment item created event
        event_data = {
            'event_type': 'stock_adjustment_item_created',
            'adjustment_id': str(instance.adjustment.id),
            'tenant_id': str(instance.tenant_id),
            'shop_id': str(instance.shop_id),
            'product_id': str(instance.product.id),
            'variant_id': str(instance.variant.id) if instance.variant else None,
            'previous_quantity': instance.previous_quantity,
            'new_quantity': instance.new_quantity,
            'difference': instance.difference
        }
        
        publish_event('inventory-events', f'stock-adjustment-item:{instance.id}', event_data)