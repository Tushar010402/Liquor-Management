from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel
from products.models import Product, ProductVariant


class StockLevel(ShopAwareModel):
    """
    Model for tracking stock levels of products in shops.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_levels')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_levels', null=True, blank=True)
    
    # Stock quantities
    current_stock = models.PositiveIntegerField(_('current stock'), default=0)
    minimum_stock = models.PositiveIntegerField(_('minimum stock'), default=10)
    maximum_stock = models.PositiveIntegerField(_('maximum stock'), default=100)
    
    # Stock status
    is_low_stock = models.BooleanField(_('is low stock'), default=False)
    is_out_of_stock = models.BooleanField(_('is out of stock'), default=False)
    
    # Last updated
    last_stock_update = models.DateTimeField(_('last stock update'), auto_now=True)
    
    class Meta:
        verbose_name = _('stock level')
        verbose_name_plural = _('stock levels')
        ordering = ['product__name']
        unique_together = ('shop_id', 'product', 'variant')
    
    def __str__(self):
        if self.variant:
            return f"{self.product.name} - {self.variant.name} - {self.shop_id} - {self.current_stock}"
        return f"{self.product.name} - {self.shop_id} - {self.current_stock}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to update stock status.
        """
        # Update stock status
        self.is_out_of_stock = self.current_stock == 0
        self.is_low_stock = 0 < self.current_stock < self.minimum_stock
        
        super().save(*args, **kwargs)


class StockTransaction(ShopAwareModel):
    """
    Model for tracking stock transactions.
    """
    TRANSACTION_TYPES = [
        ('purchase', _('Purchase')),
        ('sale', _('Sale')),
        ('return', _('Return')),
        ('adjustment', _('Adjustment')),
        ('transfer_in', _('Transfer In')),
        ('transfer_out', _('Transfer Out')),
        ('wastage', _('Wastage')),
        ('opening_stock', _('Opening Stock')),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_transactions')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_transactions', null=True, blank=True)
    
    # Transaction details
    transaction_type = models.CharField(_('transaction type'), max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField(_('quantity'))
    
    # Reference information
    reference_id = models.UUIDField(_('reference ID'), null=True, blank=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True)
    
    # User who performed the transaction
    performed_by = models.UUIDField(_('performed by'), null=True, blank=True)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('stock transaction')
        verbose_name_plural = _('stock transactions')
        ordering = ['-created_at']
    
    def __str__(self):
        if self.variant:
            return f"{self.transaction_type} - {self.product.name} - {self.variant.name} - {self.quantity}"
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"


class StockTransfer(ShopAwareModel):
    """
    Model for tracking stock transfers between shops.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('in_transit', _('In Transit')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    # Source and destination shops
    source_shop_id = models.UUIDField(_('source shop ID'))
    destination_shop_id = models.UUIDField(_('destination shop ID'))
    
    # Transfer details
    transfer_date = models.DateField(_('transfer date'))
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Reference information
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    
    # User who initiated the transfer
    initiated_by = models.UUIDField(_('initiated by'), null=True, blank=True)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('stock transfer')
        verbose_name_plural = _('stock transfers')
        ordering = ['-transfer_date', '-created_at']
    
    def __str__(self):
        return f"Transfer from {self.source_shop_id} to {self.destination_shop_id} - {self.status}"


class StockTransferItem(ShopAwareModel):
    """
    Model for tracking items in a stock transfer.
    """
    transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transfer_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='transfer_items', null=True, blank=True)
    
    # Transfer details
    quantity = models.PositiveIntegerField(_('quantity'))
    received_quantity = models.PositiveIntegerField(_('received quantity'), default=0)
    
    # Status
    is_received = models.BooleanField(_('is received'), default=False)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('stock transfer item')
        verbose_name_plural = _('stock transfer items')
        ordering = ['product__name']
    
    def __str__(self):
        if self.variant:
            return f"{self.transfer} - {self.product.name} - {self.variant.name} - {self.quantity}"
        return f"{self.transfer} - {self.product.name} - {self.quantity}"


class StockAdjustment(ShopAwareModel):
    """
    Model for tracking stock adjustments.
    """
    ADJUSTMENT_TYPES = [
        ('physical_count', _('Physical Count')),
        ('damaged', _('Damaged')),
        ('expired', _('Expired')),
        ('lost', _('Lost')),
        ('found', _('Found')),
        ('other', _('Other')),
    ]
    
    # Adjustment details
    adjustment_date = models.DateField(_('adjustment date'))
    adjustment_type = models.CharField(_('adjustment type'), max_length=20, choices=ADJUSTMENT_TYPES)
    
    # Reference information
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    
    # User who performed the adjustment
    performed_by = models.UUIDField(_('performed by'), null=True, blank=True)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('stock adjustment')
        verbose_name_plural = _('stock adjustments')
        ordering = ['-adjustment_date', '-created_at']
    
    def __str__(self):
        return f"{self.adjustment_type} - {self.adjustment_date} - {self.shop_id}"


class StockAdjustmentItem(ShopAwareModel):
    """
    Model for tracking items in a stock adjustment.
    """
    adjustment = models.ForeignKey(StockAdjustment, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='adjustment_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='adjustment_items', null=True, blank=True)
    
    # Adjustment details
    previous_quantity = models.PositiveIntegerField(_('previous quantity'))
    new_quantity = models.PositiveIntegerField(_('new quantity'))
    difference = models.IntegerField(_('difference'))
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('stock adjustment item')
        verbose_name_plural = _('stock adjustment items')
        ordering = ['product__name']
    
    def __str__(self):
        if self.variant:
            return f"{self.adjustment} - {self.product.name} - {self.variant.name} - {self.difference}"
        return f"{self.adjustment} - {self.product.name} - {self.difference}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to calculate difference.
        """
        # Calculate difference
        self.difference = self.new_quantity - self.previous_quantity
        
        super().save(*args, **kwargs)