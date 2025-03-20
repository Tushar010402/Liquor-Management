from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import BrandCategory, Brand, BrandSupplier

@receiver(post_save, sender=BrandCategory)
def brand_category_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for BrandCategory post_save event.
    Publishes brand category events to Kafka.
    """
    if created:
        # Brand category created event
        event_data = {
            'event_type': 'brand_category_created',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Brand category updated event
        event_data = {
            'event_type': 'brand_category_updated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'brand-category:{instance.id}', event_data)

@receiver(post_save, sender=Brand)
def brand_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Brand post_save event.
    Publishes brand events to Kafka.
    """
    if created:
        # Brand created event
        event_data = {
            'event_type': 'brand_created',
            'brand_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code
        }
    else:
        # Brand updated event
        event_data = {
            'event_type': 'brand_updated',
            'brand_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'brand:{instance.id}', event_data)

@receiver(post_save, sender=BrandSupplier)
def brand_supplier_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for BrandSupplier post_save event.
    Publishes brand supplier events to Kafka.
    """
    if created:
        # Brand supplier created event
        event_data = {
            'event_type': 'brand_supplier_created',
            'brand_id': str(instance.brand.id),
            'tenant_id': str(instance.tenant_id),
            'supplier_id': str(instance.supplier_id),
            'supplier_name': instance.supplier_name,
            'is_primary': instance.is_primary
        }
    else:
        # Brand supplier updated event
        event_data = {
            'event_type': 'brand_supplier_updated',
            'brand_id': str(instance.brand.id),
            'tenant_id': str(instance.tenant_id),
            'supplier_id': str(instance.supplier_id),
            'supplier_name': instance.supplier_name,
            'is_primary': instance.is_primary
        }
    
    publish_event('inventory-events', f'brand:{instance.brand.id}', event_data)

@receiver(post_delete, sender=BrandSupplier)
def brand_supplier_post_delete(sender, instance, **kwargs):
    """
    Signal handler for BrandSupplier post_delete event.
    Publishes brand supplier deleted events to Kafka.
    """
    # Brand supplier deleted event
    event_data = {
        'event_type': 'brand_supplier_deleted',
        'brand_id': str(instance.brand.id),
        'tenant_id': str(instance.tenant_id),
        'supplier_id': str(instance.supplier_id),
        'supplier_name': instance.supplier_name
    }
    
    publish_event('inventory-events', f'brand:{instance.brand.id}', event_data)