from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, PurchaseOrderItem

@receiver(pre_save, sender=PurchaseOrder)
def purchase_order_pre_save(sender, instance, **kwargs):
    """Handle pre-save operations for PurchaseOrder"""
    if not instance.order_number:
        # Generate order number if not set
        last_order = PurchaseOrder.objects.filter(
            tenant_id=instance.tenant_id,
            shop_id=instance.shop_id
        ).order_by('-order_number').first()
        
        if last_order:
            last_number = int(last_order.order_number.split('-')[-1])
            instance.order_number = f"PO-{timezone.now().strftime('%Y%m%d')}-{last_number + 1:04d}"
        else:
            instance.order_number = f"PO-{timezone.now().strftime('%Y%m%d')}-0001"

@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for PurchaseOrder"""
    if created:
        # Initialize any necessary post-creation tasks
        pass

@receiver(pre_save, sender=PurchaseOrderItem)
def purchase_order_item_pre_save(sender, instance, **kwargs):
    """Handle pre-save operations for PurchaseOrderItem"""
    if not instance.line_number:
        # Generate line number if not set
        last_item = PurchaseOrderItem.objects.filter(
            purchase_order=instance.purchase_order
        ).order_by('-line_number').first()
        
        if last_item:
            instance.line_number = last_item.line_number + 1
        else:
            instance.line_number = 1

@receiver(post_save, sender=PurchaseOrderItem)
def purchase_order_item_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for PurchaseOrderItem"""
    if created:
        # Initialize any necessary post-creation tasks
        pass 