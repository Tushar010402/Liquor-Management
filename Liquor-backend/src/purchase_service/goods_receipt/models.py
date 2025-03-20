import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel
from purchase_orders.models import PurchaseOrder, PurchaseOrderItem


class GoodsReceipt(ShopAwareModel):
    """
    Model for goods receipt.
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
    
    gr_number = models.CharField(_('GR number'), max_length=50, unique=True)
    gr_date = models.DateField(_('GR date'))
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='goods_receipts', null=True, blank=True)
    po_number = models.CharField(_('PO number'), max_length=50, blank=True)
    
    supplier_id = models.UUIDField(_('supplier ID'))
    supplier_name = models.CharField(_('supplier name'), max_length=200)
    supplier_code = models.CharField(_('supplier code'), max_length=50)
    
    delivery_date = models.DateField(_('delivery date'))
    delivery_note_number = models.CharField(_('delivery note number'), max_length=50, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(_('shipping amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
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
        verbose_name = _('goods receipt')
        verbose_name_plural = _('goods receipts')
        ordering = ['-gr_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'gr_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['tenant_id', 'shop_id', 'supplier_id']),
            models.Index(fields=['gr_number']),
        ]
    
    def __str__(self):
        return f"{self.gr_number} - {self.supplier_name} - {self.total_amount}"


class GoodsReceiptItem(ShopAwareModel):
    """
    Model for items in a goods receipt.
    """
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='items')
    
    purchase_order_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.PROTECT, related_name='receipt_items', null=True, blank=True)
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    product_barcode = models.CharField(_('product barcode'), max_length=50, blank=True)
    
    variant_id = models.UUIDField(_('variant ID'), null=True, blank=True)
    variant_name = models.CharField(_('variant name'), max_length=200, blank=True)
    
    expected_quantity = models.DecimalField(_('expected quantity'), max_digits=10, decimal_places=3, default=0)
    received_quantity = models.DecimalField(_('received quantity'), max_digits=10, decimal_places=3)
    accepted_quantity = models.DecimalField(_('accepted quantity'), max_digits=10, decimal_places=3)
    rejected_quantity = models.DecimalField(_('rejected quantity'), max_digits=10, decimal_places=3, default=0)
    
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    
    discount_percentage = models.DecimalField(_('discount percentage'), max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    batch_number = models.CharField(_('batch number'), max_length=50, blank=True)
    expiry_date = models.DateField(_('expiry date'), null=True, blank=True)
    manufacturing_date = models.DateField(_('manufacturing date'), null=True, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    class Meta:
        verbose_name = _('goods receipt item')
        verbose_name_plural = _('goods receipt items')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.received_quantity} x {self.unit_price}"


class GoodsReceiptAttachment(ShopAwareModel):
    """
    Model for attachments to goods receipts.
    """
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='attachments')
    
    file = models.FileField(_('file'), upload_to='goods_receipt_attachments/')
    file_name = models.CharField(_('file name'), max_length=255)
    file_type = models.CharField(_('file type'), max_length=100)
    file_size = models.PositiveIntegerField(_('file size'))
    
    description = models.CharField(_('description'), max_length=255, blank=True)
    
    # User information
    uploaded_by = models.UUIDField(_('uploaded by'))
    
    class Meta:
        verbose_name = _('goods receipt attachment')
        verbose_name_plural = _('goods receipt attachments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.goods_receipt.gr_number} - {self.file_name}"


class GoodsReceiptHistory(ShopAwareModel):
    """
    Model for goods receipt history.
    """
    # Action choices
    ACTION_CREATED = 'created'
    ACTION_UPDATED = 'updated'
    ACTION_APPROVED = 'approved'
    ACTION_REJECTED = 'rejected'
    ACTION_COMPLETED = 'completed'
    ACTION_CANCELLED = 'cancelled'
    
    ACTION_CHOICES = [
        (ACTION_CREATED, _('Created')),
        (ACTION_UPDATED, _('Updated')),
        (ACTION_APPROVED, _('Approved')),
        (ACTION_REJECTED, _('Rejected')),
        (ACTION_COMPLETED, _('Completed')),
        (ACTION_CANCELLED, _('Cancelled')),
    ]
    
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='history')
    
    action = models.CharField(_('action'), max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(_('action date'), auto_now_add=True)
    
    user_id = models.UUIDField(_('user ID'))
    user_name = models.CharField(_('user name'), max_length=100, blank=True)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('goods receipt history')
        verbose_name_plural = _('goods receipt history')
        ordering = ['-action_date']
    
    def __str__(self):
        return f"{self.goods_receipt.gr_number} - {self.action} - {self.action_date}"


class QualityCheck(ShopAwareModel):
    """
    Model for quality checks on received goods.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    STATUS_PARTIALLY_PASSED = 'partially_passed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_PASSED, _('Passed')),
        (STATUS_FAILED, _('Failed')),
        (STATUS_PARTIALLY_PASSED, _('Partially Passed')),
    ]
    
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='quality_checks')
    
    check_number = models.CharField(_('check number'), max_length=50, unique=True)
    check_date = models.DateField(_('check date'))
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    checked_by = models.UUIDField(_('checked by'))
    
    class Meta:
        verbose_name = _('quality check')
        verbose_name_plural = _('quality checks')
        ordering = ['-check_date']
    
    def __str__(self):
        return f"{self.check_number} - {self.goods_receipt.gr_number} - {self.status}"


class QualityCheckItem(ShopAwareModel):
    """
    Model for items in a quality check.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_PASSED = 'passed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_PASSED, _('Passed')),
        (STATUS_FAILED, _('Failed')),
    ]
    
    quality_check = models.ForeignKey(QualityCheck, on_delete=models.CASCADE, related_name='items')
    goods_receipt_item = models.ForeignKey(GoodsReceiptItem, on_delete=models.CASCADE, related_name='quality_checks')
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    
    quantity_checked = models.DecimalField(_('quantity checked'), max_digits=10, decimal_places=3)
    quantity_passed = models.DecimalField(_('quantity passed'), max_digits=10, decimal_places=3)
    quantity_failed = models.DecimalField(_('quantity failed'), max_digits=10, decimal_places=3)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    notes = models.TextField(_('notes'), blank=True)
    failure_reason = models.TextField(_('failure reason'), blank=True)
    
    class Meta:
        verbose_name = _('quality check item')
        verbose_name_plural = _('quality check items')
        ordering = ['product_name']
    
    def __str__(self):
        return f"{self.product_name} - {self.quantity_checked} - {self.status}"