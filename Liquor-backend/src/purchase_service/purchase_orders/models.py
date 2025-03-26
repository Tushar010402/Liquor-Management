import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel


class PurchaseOrder(ShopAwareModel):
    """
    Model for purchase orders.
    """
    # Status choices
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_SENT = 'sent'
    STATUS_PARTIALLY_RECEIVED = 'partially_received'
    STATUS_RECEIVED = 'received'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PENDING, _('Pending Approval')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_SENT, _('Sent to Supplier')),
        (STATUS_PARTIALLY_RECEIVED, _('Partially Received')),
        (STATUS_RECEIVED, _('Received')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Priority choices
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_MEDIUM, _('Medium')),
        (PRIORITY_HIGH, _('High')),
    ]
    
    po_number = models.CharField(_('PO number'), max_length=50, unique=True)
    po_date = models.DateField(_('PO date'))
    
    supplier_id = models.UUIDField(_('supplier ID'))
    supplier_name = models.CharField(_('supplier name'), max_length=200)
    supplier_code = models.CharField(_('supplier code'), max_length=50)
    
    expected_delivery_date = models.DateField(_('expected delivery date'), null=True, blank=True)
    delivery_address = models.TextField(_('delivery address'), blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    priority = models.CharField(_('priority'), max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(_('shipping amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    payment_terms = models.CharField(_('payment terms'), max_length=100, blank=True)
    shipping_terms = models.CharField(_('shipping terms'), max_length=100, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    internal_notes = models.TextField(_('internal notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    approved_by = models.UUIDField(_('approved by'), null=True, blank=True)
    approved_at = models.DateTimeField(_('approved at'), null=True, blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    # Metadata
    is_synced = models.BooleanField(_('is synced'), default=True)
    sync_id = models.CharField(_('sync ID'), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _('purchase order')
        verbose_name_plural = _('purchase orders')
        ordering = ['-po_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'po_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['tenant_id', 'shop_id', 'supplier_id']),
            models.Index(fields=['po_number']),
        ]
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier_name} - {self.total_amount}"


class PurchaseOrderItem(ShopAwareModel):
    """
    Model for items in a purchase order.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    product_barcode = models.CharField(_('product barcode'), max_length=50, blank=True)
    
    variant_id = models.UUIDField(_('variant ID'), null=True, blank=True)
    variant_name = models.CharField(_('variant name'), max_length=200, blank=True)
    
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=3)
    received_quantity = models.DecimalField(_('received quantity'), max_digits=10, decimal_places=3, default=0)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    
    discount_percentage = models.DecimalField(_('discount percentage'), max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('purchase order item')
        verbose_name_plural = _('purchase order items')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} x {self.unit_price}"


class PurchaseOrderAttachment(ShopAwareModel):
    """
    Model for attachments to purchase orders.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='attachments')
    
    file = models.FileField(_('file'), upload_to='purchase_order_attachments/')
    file_name = models.CharField(_('file name'), max_length=255)
    file_type = models.CharField(_('file type'), max_length=100)
    file_size = models.PositiveIntegerField(_('file size'))
    
    description = models.CharField(_('description'), max_length=255, blank=True)
    
    # User information
    uploaded_by = models.UUIDField(_('uploaded by'))
    
    class Meta:
        verbose_name = _('purchase order attachment')
        verbose_name_plural = _('purchase order attachments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.file_name}"


class PurchaseOrderHistory(ShopAwareModel):
    """
    Model for purchase order history.
    """
    # Action choices
    ACTION_CREATED = 'created'
    ACTION_UPDATED = 'updated'
    ACTION_APPROVED = 'approved'
    ACTION_REJECTED = 'rejected'
    ACTION_SENT = 'sent'
    ACTION_RECEIVED = 'received'
    ACTION_CANCELLED = 'cancelled'
    
    ACTION_CHOICES = [
        (ACTION_CREATED, _('Created')),
        (ACTION_UPDATED, _('Updated')),
        (ACTION_APPROVED, _('Approved')),
        (ACTION_REJECTED, _('Rejected')),
        (ACTION_SENT, _('Sent to Supplier')),
        (ACTION_RECEIVED, _('Received')),
        (ACTION_CANCELLED, _('Cancelled')),
    ]
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='history')
    
    action = models.CharField(_('action'), max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(_('action date'), auto_now_add=True)
    
    user_id = models.UUIDField(_('user ID'))
    user_name = models.CharField(_('user name'), max_length=100, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('purchase order history')
        verbose_name_plural = _('purchase order history')
        ordering = ['-action_date']
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.action} - {self.action_date}"