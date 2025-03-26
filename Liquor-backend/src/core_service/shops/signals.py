from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import Shop, ShopOperatingHours, ShopHoliday, ShopSettings

@receiver(post_save, sender=Shop)
def shop_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Shop post_save event.
    Publishes shop events to Kafka.
    """
    if created:
        # Shop created event
        event_data = {
            'event_type': 'shop_created',
            'shop_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code
        }
    else:
        # Shop updated event
        event_data = {
            'event_type': 'shop_updated',
            'shop_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'is_active': instance.is_active,
            'is_open': instance.is_open
        }
    
    publish_event('shop-events', f'shop:{instance.id}', event_data)

@receiver(post_save, sender=ShopSettings)
def shop_settings_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ShopSettings post_save event.
    Publishes shop settings events to Kafka.
    """
    # Shop settings updated event
    event_data = {
        'event_type': 'shop_settings_updated',
        'shop_id': str(instance.shop.id),
        'tenant_id': str(instance.tenant_id),
        'settings_id': str(instance.id)
    }
    
    publish_event('shop-events', f'shop:{instance.shop.id}', event_data)

@receiver(post_save, sender=ShopOperatingHours)
def shop_operating_hours_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ShopOperatingHours post_save event.
    Publishes shop operating hours events to Kafka.
    """
    if created:
        # Shop operating hours created event
        event_data = {
            'event_type': 'shop_operating_hours_created',
            'shop_id': str(instance.shop.id),
            'tenant_id': str(instance.tenant_id),
            'day_of_week': instance.day_of_week,
            'is_closed': instance.is_closed
        }
    else:
        # Shop operating hours updated event
        event_data = {
            'event_type': 'shop_operating_hours_updated',
            'shop_id': str(instance.shop.id),
            'tenant_id': str(instance.tenant_id),
            'day_of_week': instance.day_of_week,
            'is_closed': instance.is_closed
        }
    
    publish_event('shop-events', f'shop:{instance.shop.id}', event_data)

@receiver(post_delete, sender=ShopOperatingHours)
def shop_operating_hours_post_delete(sender, instance, **kwargs):
    """
    Signal handler for ShopOperatingHours post_delete event.
    Publishes shop operating hours deleted events to Kafka.
    """
    # Shop operating hours deleted event
    event_data = {
        'event_type': 'shop_operating_hours_deleted',
        'shop_id': str(instance.shop.id),
        'tenant_id': str(instance.tenant_id),
        'day_of_week': instance.day_of_week
    }
    
    publish_event('shop-events', f'shop:{instance.shop.id}', event_data)

@receiver(post_save, sender=ShopHoliday)
def shop_holiday_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ShopHoliday post_save event.
    Publishes shop holiday events to Kafka.
    """
    if created:
        # Shop holiday created event
        event_data = {
            'event_type': 'shop_holiday_created',
            'shop_id': str(instance.shop.id),
            'tenant_id': str(instance.tenant_id),
            'holiday_id': str(instance.id),
            'name': instance.name,
            'date': instance.date.isoformat()
        }
    else:
        # Shop holiday updated event
        event_data = {
            'event_type': 'shop_holiday_updated',
            'shop_id': str(instance.shop.id),
            'tenant_id': str(instance.tenant_id),
            'holiday_id': str(instance.id),
            'name': instance.name,
            'date': instance.date.isoformat()
        }
    
    publish_event('shop-events', f'shop:{instance.shop.id}', event_data)

@receiver(post_delete, sender=ShopHoliday)
def shop_holiday_post_delete(sender, instance, **kwargs):
    """
    Signal handler for ShopHoliday post_delete event.
    Publishes shop holiday deleted events to Kafka.
    """
    # Shop holiday deleted event
    event_data = {
        'event_type': 'shop_holiday_deleted',
        'shop_id': str(instance.shop.id),
        'tenant_id': str(instance.tenant_id),
        'holiday_id': str(instance.id),
        'name': instance.name,
        'date': instance.date.isoformat()
    }
    
    publish_event('shop-events', f'shop:{instance.shop.id}', event_data)