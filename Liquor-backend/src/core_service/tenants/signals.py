from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import Tenant, TenantSettings

@receiver(post_save, sender=Tenant)
def tenant_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Tenant post_save event.
    Publishes tenant events to Kafka.
    """
    if created:
        # Tenant created event
        event_data = {
            'event_type': 'tenant_created',
            'tenant_id': str(instance.id),
            'name': instance.name,
            'slug': instance.slug
        }
    else:
        # Tenant updated event
        event_data = {
            'event_type': 'tenant_updated',
            'tenant_id': str(instance.id),
            'name': instance.name,
            'slug': instance.slug,
            'is_active': instance.is_active
        }
    
    publish_event('tenant-events', f'tenant:{instance.id}', event_data)

@receiver(post_save, sender=TenantSettings)
def tenant_settings_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for TenantSettings post_save event.
    Publishes tenant settings events to Kafka.
    """
    # Tenant settings updated event
    event_data = {
        'event_type': 'tenant_settings_updated',
        'tenant_id': str(instance.tenant.id),
        'settings_id': str(instance.id)
    }
    
    publish_event('tenant-events', f'tenant:{instance.tenant.id}', event_data)