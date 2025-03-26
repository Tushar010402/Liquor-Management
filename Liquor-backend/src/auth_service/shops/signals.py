from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Shop, ShopSettings

@receiver(post_save, sender=Shop)
def shop_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for when a Shop is saved.
    """
    if created:
        # Create shop settings automatically when a new shop is created
        ShopSettings.objects.create(shop=instance)
        
        # Log shop creation or perform other actions
        print(f"Shop created: {instance.name}")

@receiver(post_delete, sender=Shop)
def shop_post_delete(sender, instance, **kwargs):
    """
    Signal handler for when a Shop is deleted.
    """
    # Log shop deletion or perform cleanup
    print(f"Shop deleted: {instance.name}")

# Add more signal handlers as needed 