import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel


class Sale(ShopAwareModel):
    """
    Model for sales transactions.
    """
    # Sale status choices
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
    
    # Sale type choices
    TYPE_REGULAR = 'regular'
    TYPE_WHOLESALE = 'wholesale'
    TYPE_SPECIAL = 'special'
    
    TYPE_CHOICES = [
        (TYPE_REGULAR, _('Regular')),
        (TYPE_WHOLESALE, _('Wholesale')),
        (TYPE_SPECIAL, _('Special')),
    ]
    
    # Payment method choices
    PAYMENT_CASH = 'cash'
    PAYMENT_UPI = 'upi'
    PAYMENT_CARD = 'card'
    PAYMENT_CREDIT = 'credit'
    PAYMENT_MIXED = 'mixed'
    
    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_CASH, _('Cash')),
        (PAYMENT_UPI, _('UPI')),
        (PAYMENT_CARD, _('Card')),
        (PAYMENT_CREDIT, _('Credit')),
        (PAYMENT_MIXED, _('Mixed')),
    ]
    
    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    sale_date = models.DateTimeField(_('sale date'))
    customer_name = models.CharField(_('customer name'), max_length=100, blank=True)
    customer_phone = models.CharField(_('customer phone'), max_length=20, blank=True)
    customer_address = models.TextField(_('customer address'), blank=True)
    
    sale_type = models.CharField(_('sale type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_REGULAR)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(_('discount percentage'), max_digits=5, decimal_places=2, default=0)
    discount_reason = models.CharField(_('discount reason'), max_length=200, blank=True)
    
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHOD_CHOICES, default=PAYMENT_CASH)
    payment_reference = models.CharField(_('payment reference'), max_length=100, blank=True)
    payment_details = models.JSONField(_('payment details'), default=dict, blank=True)
    
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
        verbose_name = _('sale')
        verbose_name_plural = _('sales')
        ordering = ['-sale_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'sale_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['tenant_id', 'shop_id', 'created_by']),
            models.Index(fields=['invoice_number']),
        ]
    
    def __str__(self):
        return f"{self.invoice_number} - {self.total_amount}"


class SaleItem(ShopAwareModel):
    """
    Model for items in a sale.
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    product_barcode = models.CharField(_('product barcode'), max_length=50, blank=True)
    
    variant_id = models.UUIDField(_('variant ID'), null=True, blank=True)
    variant_name = models.CharField(_('variant name'), max_length=200, blank=True)
    
    quantity = models.DecimalField(_('quantity'), max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(_('discount percentage'), max_digits=5, decimal_places=2, default=0)
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('sale item')
        verbose_name_plural = _('sale items')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity} x {self.unit_price}"


class SaleDraft(ShopAwareModel):
    """
    Model for draft sales.
    """
    name = models.CharField(_('name'), max_length=100)
    customer_name = models.CharField(_('customer name'), max_length=100, blank=True)
    customer_phone = models.CharField(_('customer phone'), max_length=20, blank=True)
    
    sale_type = models.CharField(_('sale type'), max_length=20, choices=Sale.TYPE_CHOICES, default=Sale.TYPE_REGULAR)
    
    items_data = models.JSONField(_('items data'), default=list)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(_('discount percentage'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('sale draft')
        verbose_name_plural = _('sale drafts')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.total_amount}"


class SalePayment(ShopAwareModel):
    """
    Model for payments associated with a sale.
    """
    # Payment method choices
    METHOD_CASH = 'cash'
    METHOD_UPI = 'upi'
    METHOD_CARD = 'card'
    METHOD_CREDIT = 'credit'
    
    METHOD_CHOICES = [
        (METHOD_CASH, _('Cash')),
        (METHOD_UPI, _('UPI')),
        (METHOD_CARD, _('Card')),
        (METHOD_CREDIT, _('Credit')),
    ]
    
    # Payment status choices
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_FAILED, _('Failed')),
        (STATUS_REFUNDED, _('Refunded')),
    ]
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(_('payment method'), max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    
    reference = models.CharField(_('reference'), max_length=100, blank=True)
    details = models.JSONField(_('details'), default=dict, blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('sale payment')
        verbose_name_plural = _('sale payments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sale.invoice_number} - {self.payment_method} - {self.amount}"


class BatchSale(ShopAwareModel):
    """
    Model for batch sales.
    """
    # Status choices
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
    
    batch_number = models.CharField(_('batch number'), max_length=50, unique=True)
    batch_date = models.DateTimeField(_('batch date'))
    description = models.TextField(_('description'), blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    total_sales = models.IntegerField(_('total sales'), default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    approved_by = models.UUIDField(_('approved by'), null=True, blank=True)
    approved_at = models.DateTimeField(_('approved at'), null=True, blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    class Meta:
        verbose_name = _('batch sale')
        verbose_name_plural = _('batch sales')
        ordering = ['-batch_date']
    
    def __str__(self):
        return f"{self.batch_number} - {self.total_sales} sales"


class BatchSaleItem(ShopAwareModel):
    """
    Model for sales in a batch.
    """
    batch = models.ForeignKey(BatchSale, on_delete=models.CASCADE, related_name='sales')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='batch_items')
    
    class Meta:
        verbose_name = _('batch sale item')
        verbose_name_plural = _('batch sale items')
        unique_together = ('batch', 'sale')
    
    def __str__(self):
        return f"{self.batch.batch_number} - {self.sale.invoice_number}"