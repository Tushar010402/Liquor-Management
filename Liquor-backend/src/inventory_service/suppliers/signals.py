from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from common.utils.kafka_utils import publish_event
from .models import (
    SupplierCategory, Supplier, SupplierContact,
    SupplierBankAccount, SupplierDocument
)

@receiver(post_save, sender=SupplierCategory)
def supplier_category_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for SupplierCategory post_save event.
    Publishes supplier category events to Kafka.
    """
    if created:
        # Supplier category created event
        event_data = {
            'event_type': 'supplier_category_created',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name
        }
    else:
        # Supplier category updated event
        event_data = {
            'event_type': 'supplier_category_updated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'is_active': instance.is_active
        }
    
    publish_event('inventory-events', f'supplier-category:{instance.id}', event_data)

@receiver(post_save, sender=Supplier)
def supplier_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Supplier post_save event.
    Publishes supplier events to Kafka.
    """
    if created:
        # Supplier created event
        event_data = {
            'event_type': 'supplier_created',
            'supplier_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code
        }
    else:
        # Supplier updated event
        event_data = {
            'event_type': 'supplier_updated',
            'supplier_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'is_active': instance.is_active,
            'is_approved': instance.is_approved
        }
    
    publish_event('inventory-events', f'supplier:{instance.id}', event_data)

@receiver(post_save, sender=SupplierContact)
def supplier_contact_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for SupplierContact post_save event.
    Publishes supplier contact events to Kafka.
    """
    if created:
        # Supplier contact created event
        event_data = {
            'event_type': 'supplier_contact_created',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'contact_id': str(instance.id),
            'name': instance.name,
            'is_primary': instance.is_primary
        }
    else:
        # Supplier contact updated event
        event_data = {
            'event_type': 'supplier_contact_updated',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'contact_id': str(instance.id),
            'name': instance.name,
            'is_primary': instance.is_primary
        }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)

@receiver(post_delete, sender=SupplierContact)
def supplier_contact_post_delete(sender, instance, **kwargs):
    """
    Signal handler for SupplierContact post_delete event.
    Publishes supplier contact deleted events to Kafka.
    """
    # Supplier contact deleted event
    event_data = {
        'event_type': 'supplier_contact_deleted',
        'supplier_id': str(instance.supplier.id),
        'tenant_id': str(instance.tenant_id),
        'contact_id': str(instance.id),
        'name': instance.name
    }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)

@receiver(post_save, sender=SupplierBankAccount)
def supplier_bank_account_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for SupplierBankAccount post_save event.
    Publishes supplier bank account events to Kafka.
    """
    if created:
        # Supplier bank account created event
        event_data = {
            'event_type': 'supplier_bank_account_created',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'bank_account_id': str(instance.id),
            'bank_name': instance.bank_name,
            'account_number': instance.account_number,
            'is_primary': instance.is_primary
        }
    else:
        # Supplier bank account updated event
        event_data = {
            'event_type': 'supplier_bank_account_updated',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'bank_account_id': str(instance.id),
            'bank_name': instance.bank_name,
            'account_number': instance.account_number,
            'is_primary': instance.is_primary
        }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)

@receiver(post_delete, sender=SupplierBankAccount)
def supplier_bank_account_post_delete(sender, instance, **kwargs):
    """
    Signal handler for SupplierBankAccount post_delete event.
    Publishes supplier bank account deleted events to Kafka.
    """
    # Supplier bank account deleted event
    event_data = {
        'event_type': 'supplier_bank_account_deleted',
        'supplier_id': str(instance.supplier.id),
        'tenant_id': str(instance.tenant_id),
        'bank_account_id': str(instance.id),
        'bank_name': instance.bank_name,
        'account_number': instance.account_number
    }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)

@receiver(post_save, sender=SupplierDocument)
def supplier_document_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for SupplierDocument post_save event.
    Publishes supplier document events to Kafka.
    """
    if created:
        # Supplier document created event
        event_data = {
            'event_type': 'supplier_document_created',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'document_id': str(instance.id),
            'name': instance.name,
            'document_type': instance.document_type
        }
    else:
        # Supplier document updated event
        event_data = {
            'event_type': 'supplier_document_updated',
            'supplier_id': str(instance.supplier.id),
            'tenant_id': str(instance.tenant_id),
            'document_id': str(instance.id),
            'name': instance.name,
            'document_type': instance.document_type
        }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)

@receiver(post_delete, sender=SupplierDocument)
def supplier_document_post_delete(sender, instance, **kwargs):
    """
    Signal handler for SupplierDocument post_delete event.
    Publishes supplier document deleted events to Kafka.
    """
    # Supplier document deleted event
    event_data = {
        'event_type': 'supplier_document_deleted',
        'supplier_id': str(instance.supplier.id),
        'tenant_id': str(instance.tenant_id),
        'document_id': str(instance.id),
        'name': instance.name,
        'document_type': instance.document_type
    }
    
    publish_event('inventory-events', f'supplier:{instance.supplier.id}', event_data)