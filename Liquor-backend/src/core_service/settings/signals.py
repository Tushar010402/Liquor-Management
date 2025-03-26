from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate

@receiver(post_save, sender=SystemSetting)
def system_setting_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for SystemSetting post_save event.
    Publishes system setting events to Kafka.
    """
    if created:
        # System setting created event
        event_data = {
            'event_type': 'system_setting_created',
            'setting_id': str(instance.id),
            'key': instance.key,
            'is_public': instance.is_public
        }
    else:
        # System setting updated event
        event_data = {
            'event_type': 'system_setting_updated',
            'setting_id': str(instance.id),
            'key': instance.key,
            'is_public': instance.is_public,
            'is_active': instance.is_active
        }
    
    publish_event('setting-events', f'system-setting:{instance.id}', event_data)

@receiver(post_save, sender=TenantSetting)
def tenant_setting_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for TenantSetting post_save event.
    Publishes tenant setting events to Kafka.
    """
    if created:
        # Tenant setting created event
        event_data = {
            'event_type': 'tenant_setting_created',
            'setting_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'key': instance.key
        }
    else:
        # Tenant setting updated event
        event_data = {
            'event_type': 'tenant_setting_updated',
            'setting_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'key': instance.key,
            'is_active': instance.is_active
        }
    
    publish_event('setting-events', f'tenant-setting:{instance.id}', event_data)

@receiver(post_save, sender=EmailTemplate)
def email_template_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for EmailTemplate post_save event.
    Publishes email template events to Kafka.
    """
    if created:
        # Email template created event
        event_data = {
            'event_type': 'email_template_created',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Email template updated event
        event_data = {
            'event_type': 'email_template_updated',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('setting-events', f'email-template:{instance.id}', event_data)

@receiver(post_save, sender=NotificationTemplate)
def notification_template_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for NotificationTemplate post_save event.
    Publishes notification template events to Kafka.
    """
    if created:
        # Notification template created event
        event_data = {
            'event_type': 'notification_template_created',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Notification template updated event
        event_data = {
            'event_type': 'notification_template_updated',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('setting-events', f'notification-template:{instance.id}', event_data)