from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import GoodsReceipt, GoodsReceiptItem

@receiver(pre_save, sender=GoodsReceipt)
def goods_receipt_pre_save(sender, instance, **kwargs):
    """Handle pre-save operations for GoodsReceipt"""
    if not instance.receipt_number:
        # Generate receipt number if not set
        last_receipt = GoodsReceipt.objects.filter(
            tenant_id=instance.tenant_id,
            shop_id=instance.shop_id
        ).order_by('-receipt_number').first()
        
        if last_receipt:
            last_number = int(last_receipt.receipt_number.split('-')[-1])
            instance.receipt_number = f"GR-{timezone.now().strftime('%Y%m%d')}-{last_number + 1:04d}"
        else:
            instance.receipt_number = f"GR-{timezone.now().strftime('%Y%m%d')}-0001"

@receiver(post_save, sender=GoodsReceipt)
def goods_receipt_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for GoodsReceipt"""
    if created:
        # Initialize any necessary post-creation tasks
        pass

@receiver(pre_save, sender=GoodsReceiptItem)
def goods_receipt_item_pre_save(sender, instance, **kwargs):
    """Handle pre-save operations for GoodsReceiptItem"""
    if not instance.line_number:
        # Generate line number if not set
        last_item = GoodsReceiptItem.objects.filter(
            goods_receipt=instance.goods_receipt
        ).order_by('-line_number').first()
        
        if last_item:
            instance.line_number = last_item.line_number + 1
        else:
            instance.line_number = 1

@receiver(post_save, sender=GoodsReceiptItem)
def goods_receipt_item_post_save(sender, instance, created, **kwargs):
    """Handle post-save operations for GoodsReceiptItem"""
    if created:
        # Initialize any necessary post-creation tasks
        pass 