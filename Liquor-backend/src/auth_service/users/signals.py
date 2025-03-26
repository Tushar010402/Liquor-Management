from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from common.utils.kafka_utils import publish_event
from .models import UserShopAssignment, UserPermission

User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for User post_save event.
    Publishes user events to Kafka.
    """
    if created:
        # User created event
        event_data = {
            'event_type': 'user_created',
            'user_id': str(instance.id),
            'email': instance.email,
            'role': instance.role,
            'tenant_id': str(instance.tenant_id) if instance.tenant_id else None
        }
    else:
        # User updated event
        event_data = {
            'event_type': 'user_updated',
            'user_id': str(instance.id),
            'email': instance.email,
            'role': instance.role,
            'tenant_id': str(instance.tenant_id) if instance.tenant_id else None,
            'is_active': instance.is_active
        }
    
    publish_event('user-events', f'user:{instance.id}', event_data)

@receiver(post_save, sender=UserShopAssignment)
def user_shop_assignment_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for UserShopAssignment post_save event.
    Publishes shop assignment events to Kafka.
    """
    if created:
        # Shop assigned event
        event_data = {
            'event_type': 'user_shop_assigned',
            'user_id': str(instance.user.id),
            'shop_id': str(instance.shop_id),
            'is_primary': instance.is_primary
        }
        
        publish_event('user-events', f'user:{instance.user.id}', event_data)

@receiver(post_delete, sender=UserShopAssignment)
def user_shop_assignment_post_delete(sender, instance, **kwargs):
    """
    Signal handler for UserShopAssignment post_delete event.
    Publishes shop unassignment events to Kafka.
    """
    # Shop unassigned event
    event_data = {
        'event_type': 'user_shop_unassigned',
        'user_id': str(instance.user.id),
        'shop_id': str(instance.shop_id)
    }
    
    publish_event('user-events', f'user:{instance.user.id}', event_data)

@receiver(post_save, sender=UserPermission)
def user_permission_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for UserPermission post_save event.
    Publishes permission events to Kafka.
    """
    if created:
        # Permission added event
        event_data = {
            'event_type': 'user_permission_added',
            'user_id': str(instance.user.id),
            'permission_key': instance.permission_key
        }
        
        publish_event('user-events', f'user:{instance.user.id}', event_data)

@receiver(post_delete, sender=UserPermission)
def user_permission_post_delete(sender, instance, **kwargs):
    """
    Signal handler for UserPermission post_delete event.
    Publishes permission removal events to Kafka.
    """
    # Permission removed event
    event_data = {
        'event_type': 'user_permission_removed',
        'user_id': str(instance.user.id),
        'permission_key': instance.permission_key
    }
    
    publish_event('user-events', f'user:{instance.user.id}', event_data)