import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel
from sales.models import Sale, SaleItem


class Return(ShopAwareModel):
    """
    Model for return transactions.
    """
    # Return status choices
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_PENDING, _('Pending Approval')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Return type choices
    TYPE_FULL = 'full'
    TYPE_PARTIAL = 'partial'
    
    TYPE_CHOICES = [
        (TYPE_FULL, _('Full Return')),
        (TYPE_PARTIAL, _('Partial Return')),
    ]
    
    # Refund method choices
    REFUND_CASH = 'cash'
    REFUND_UPI = 'upi'
    REFUND_CARD = 'card'
    REFUND_CREDIT = 'credit'
    REFUND_EXCHANGE = 'exchange'
    
    REFUND_METHOD_CHOICES = [
        (REFUND_CASH, _('Cash')),
        (REFUND_UPI, _('UPI')),
        (REFUND_CARD, _('Card')),
        (REFUND_CREDIT, _('Credit')),
        (REFUND_EXCHANGE, _('Exchange')),
    ]
    
    return_number = models.CharField(_('return number'), max_length=50, unique=True)
    return_date = models.DateTimeField(_('return date'))
    
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT, related_name='returns', null=True, blank=True)
    original_invoice_number = models.CharField(_('original invoice number'), max_length=50, blank=True)
    
    customer_name = models.CharField(_('customer name'), max_length=100, blank=True)
    customer_phone = models.CharField(_('customer phone'), max_length=20, blank=True)
    
    return_type = models.CharField(_('return type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_PARTIAL)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    refund_method = models.CharField(_('refund method'), max_length=20, choices=REFUND_METHOD_CHOICES, default=REFUND_CASH)
    refund_reference = models.CharField(_('refund reference'), max_length=100, blank=True)
    refund_details = models.JSONField(_('refund details'), default=dict, blank=True)
    
    reason = models.TextField(_('reason'))
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    approved_by = models.UUIDField(_('approved by'), null=True, blank=True)
    approved_at = models.DateTimeField(_('approved at'), null=True, blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    # Metadata
    is_synced = models.BooleanField(_('is synced'), default=True)
    sync_id = models.CharField(_('sync ID'), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _('return')
        verbose_name_plural = _('returns')
        ordering = ['-return_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'return_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['tenant_id', 'shop_id', 'created_by']),
            models.Index(fields=['return_number']),
        ]
    
    def __str__(self):
        return f"{self.return_number} - {self.total_amount}"


class ReturnItem(ShopAwareModel):
    """
    Model for items in a return.
    """
    # Return reason choices
    REASON_DEFECTIVE = 'defective'
    REASON_DAMAGED = 'damaged'
    REASON_WRONG_ITEM = 'wrong_item'
    REASON_CUSTOMER_DISSATISFIED = 'customer_dissatisfied'
    REASON_OTHER = 'other'
    
    REASON_CHOICES = [
        (REASON_DEFECTIVE, _('Defective')),
        (REASON_DAMAGED, _('Damaged')),
        (REASON_WRONG_ITEM, _('Wrong Item')),
        (REASON_CUSTOMER_DISSATISFIED, _('Customer Dissatisfied')),
        (REASON_OTHER, _('Other')),
    ]
    
    return_transaction = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items')
    
    sale_item = models.ForeignKey(SaleItem, on_delete=models.PROTECT, related_name='return_items', null=True, blank=True)
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    product_barcode = models.CharField(_('product barcode'), max_length=50, blank=True)
    
    variant_id = models.UUIDField(_('variant ID'), null=True, blank=True)
    variant_name = models.CharField(_('variant name'), max_length=200, blank=True)
    
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    reason = models.CharField(_('reason'), max_length=50, choices=REASON_CHOICES, default=REASON_OTHER)
    reason_details = models.TextField(_('reason details'), blank=True)
    
    class Meta:
        verbose_name = _('return item')
        verbose_name_plural = _('return items')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} x {self.unit_price}"


class ReturnExchange(ShopAwareModel):
    """
    Model for exchange items in a return.
    """
    return_transaction = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='exchanges')
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    product_barcode = models.CharField(_('product barcode'), max_length=50, blank=True)
    
    variant_id = models.UUIDField(_('variant ID'), null=True, blank=True)
    variant_name = models.CharField(_('variant name'), max_length=200, blank=True)
    
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('return exchange')
        verbose_name_plural = _('return exchanges')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} x {self.unit_price}"
