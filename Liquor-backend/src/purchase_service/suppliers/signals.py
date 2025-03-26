from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Supplier

@receiver(pre_save, sender=Supplier)
def supplier_pre_save(sender, instance, **kwargs):
    """Handle pre-save operations for Supplier"""
    if not instance.supplier_code:
        # Generate supplier code if not set
        last_supplier = Supplier.objects.filter(
            tenant_id=instance.tenant_id
        ).order_by('-supplier_code').first()
        
        if last_supplier:
            last_number = int(last_supplier.supplier_code.split('-')[-1])
            instance.supplier_code = f"SUP-{last_number + 1:04d}"
        else:
            instance.supplier_code = "SUP-0001"

@receiver(post_save, sender=Supplier)
def supplier_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for Supplier"""
    if created:
        # Initialize any necessary post-creation tasks
        pass 