from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tenant

# Here you can add signal handlers for tenant-related models
# For example:

@receiver(post_save, sender=Tenant)
def tenant_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a Tenant is saved.
    """
    if created:
        # Log tenant creation or perform other actions
        print(f"Tenant created: {instance.name}")

@receiver(post_delete, sender=Tenant)
def tenant_post_delete(sender, instance, **kwargs):
    """
    Signal handler for when a Tenant is deleted.
    """
    # Log tenant deletion or perform cleanup
    print(f"Tenant deleted: {instance.name}")

# Add more signal handlers as needed 