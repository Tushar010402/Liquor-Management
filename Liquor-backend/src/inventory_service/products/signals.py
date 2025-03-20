from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import (
    ProductCategory, ProductType, Product, ProductVariant,
    ProductAttribute, ProductAttributeValue, ProductPriceHistory
)

@receiver(post_save, sender=ProductCategory)
def product_category_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductCategory post_save event.
    Publishes product category events to Kafka.
    """
    if created:
        # Product category created event
        event_data = {
            'event_type': 'product_category_created',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Product category updated event
        event_data = {
            'event_type': 'product_category_updated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'product-category:{instance.id}', event_data)

@receiver(post_save, sender=ProductType)
def product_type_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductType post_save event.
    Publishes product type events to Kafka.
    """
    if created:
        # Product type created event
        event_data = {
            'event_type': 'product_type_created',
            'product_type_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Product type updated event
        event_data = {
            'event_type': 'product_type_updated',
            'product_type_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'product-type:{instance.id}', event_data)

@receiver(post_save, sender=ProductAttribute)
def product_attribute_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductAttribute post_save event.
    Publishes product attribute events to Kafka.
    """
    if created:
        # Product attribute created event
        event_data = {
            'event_type': 'product_attribute_created',
            'attribute_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Product attribute updated event
        event_data = {
            'event_type': 'product_attribute_updated',
            'attribute_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'product-attribute:{instance.id}', event_data)

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Product post_save event.
    Publishes product events to Kafka.
    """
    if created:
        # Product created event
        event_data = {
            'event_type': 'product_created',
            'product_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'brand_id': str(instance.brand.id)
        }
    else:
        # Product updated event
        event_data = {
            'event_type': 'product_updated',
            'product_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'brand_id': str(instance.brand.id),
            'is_active': instance.is_active,
            'is_available': instance.is_available
        }
    
    publish_event('inventory-events', f'product:{instance.id}', event_data)

@receiver(post_save, sender=ProductVariant)
def product_variant_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductVariant post_save event.
    Publishes product variant events to Kafka.
    """
    if created:
        # Product variant created event
        event_data = {
            'event_type': 'product_variant_created',
            'variant_id': str(instance.id),
            'product_id': str(instance.product.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code
        }
    else:
        # Product variant updated event
        event_data = {
            'event_type': 'product_variant_updated',
            'variant_id': str(instance.id),
            'product_id': str(instance.product.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'is_active': instance.is_active,
            'is_available': instance.is_available
        }
    
    publish_event('inventory-events', f'product-variant:{instance.id}', event_data)

@receiver(post_save, sender=ProductAttributeValue)
def product_attribute_value_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductAttributeValue post_save event.
    Publishes product attribute value events to Kafka.
    """
    if created:
        # Product attribute value created event
        event_data = {
            'event_type': 'product_attribute_value_created',
            'product_id': str(instance.product.id),
            'tenant_id': str(instance.tenant_id),
            'attribute_id': str(instance.attribute.id),
            'attribute_name': instance.attribute.name,
            'value': instance.value
        }
    else:
        # Product attribute value updated event
        event_data = {
            'event_type': 'product_attribute_value_updated',
            'product_id': str(instance.product.id),
            'tenant_id': str(instance.tenant_id),
            'attribute_id': str(instance.attribute.id),
            'attribute_name': instance.attribute.name,
            'value': instance.value
        }
    
    publish_event('inventory-events', f'product:{instance.product.id}', event_data)

@receiver(post_save, sender=ProductPriceHistory)
def product_price_history_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ProductPriceHistory post_save event.
    Publishes product price history events to Kafka.
    """
    if created:
        # Product price history created event
        event_data = {
            'event_type': 'product_price_changed',
            'product_id': str(instance.product.id),
            'tenant_id': str(instance.tenant_id),
            'mrp': str(instance.mrp),
            'selling_price': str(instance.selling_price),
            'purchase_price': str(instance.purchase_price),
            'effective_from': instance.effective_from.isoformat()
        }
        
        publish_event('inventory-events', f'product:{instance.product.id}', event_data)