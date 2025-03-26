import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel, ShopAwareModel


class Supplier(TenantAwareModel):
    """
    Model for suppliers.
    """
    # Status choices
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_BLACKLISTED = 'blacklisted'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
        (STATUS_BLACKLISTED, _('Blacklisted')),
    ]
    
    # Type choices
    TYPE_MANUFACTURER = 'manufacturer'
    TYPE_DISTRIBUTOR = 'distributor'
    TYPE_WHOLESALER = 'wholesaler'
    TYPE_RETAILER = 'retailer'
    TYPE_OTHER = 'other'
    
    TYPE_CHOICES = [
        (TYPE_MANUFACTURER, _('Manufacturer')),
        (TYPE_DISTRIBUTOR, _('Distributor')),
        (TYPE_WHOLESALER, _('Wholesaler')),
        (TYPE_RETAILER, _('Retailer')),
        (TYPE_OTHER, _('Other')),
    ]
    
    code = models.CharField(_('code'), max_length=50, unique=True)
    name = models.CharField(_('name'), max_length=200)
    legal_name = models.CharField(_('legal name'), max_length=200, blank=True)
    
    supplier_type = models.CharField(_('supplier type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_DISTRIBUTOR)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    registration_number = models.CharField(_('registration number'), max_length=50, blank=True)
    
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), blank=True)
    
    credit_limit = models.DecimalField(_('credit limit'), max_digits=10, decimal_places=2, default=0)
    credit_period = models.PositiveIntegerField(_('credit period (days)'), default=0)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ['name']
        indexes = [
            models.Index(fields=['tenant_id', 'name']),
            models.Index(fields=['tenant_id', 'status']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class SupplierContact(TenantAwareModel):
    """
    Model for supplier contacts.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    
    name = models.CharField(_('name'), max_length=100)
    designation = models.CharField(_('designation'), max_length=100, blank=True)
    department = models.CharField(_('department'), max_length=100, blank=True)
    
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    mobile = models.CharField(_('mobile'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    
    is_primary = models.BooleanField(_('is primary'), default=False)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('supplier contact')
        verbose_name_plural = _('supplier contacts')
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.name}"


class SupplierProduct(ShopAwareModel):
    """
    Model for products supplied by a supplier.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    
    product_id = models.UUIDField(_('product ID'))
    product_name = models.CharField(_('product name'), max_length=200)
    product_code = models.CharField(_('product code'), max_length=50)
    
    supplier_product_code = models.CharField(_('supplier product code'), max_length=50, blank=True)
    supplier_product_name = models.CharField(_('supplier product name'), max_length=200, blank=True)
    
    unit_price = models.DecimalField(_('unit price'), max_digits=10, decimal_places=2)
    minimum_order_quantity = models.DecimalField(_('minimum order quantity'), max_digits=10, decimal_places=3, default=1)
    
    lead_time_days = models.PositiveIntegerField(_('lead time (days)'), default=0)
    is_preferred_supplier = models.BooleanField(_('is preferred supplier'), default=False)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('supplier product')
        verbose_name_plural = _('supplier products')
        ordering = ['product_name']
        unique_together = ('supplier', 'product_id', 'shop_id')
    
    def __str__(self):
        return f"{self.supplier.name} - {self.product_name}"


class SupplierPayment(ShopAwareModel):
    """
    Model for payments to suppliers.
    """
    # Payment status choices
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Payment method choices
    METHOD_CASH = 'cash'
    METHOD_BANK_TRANSFER = 'bank_transfer'
    METHOD_CHEQUE = 'cheque'
    METHOD_UPI = 'upi'
    METHOD_CREDIT = 'credit'
    
    METHOD_CHOICES = [
        (METHOD_CASH, _('Cash')),
        (METHOD_BANK_TRANSFER, _('Bank Transfer')),
        (METHOD_CHEQUE, _('Cheque')),
        (METHOD_UPI, _('UPI')),
        (METHOD_CREDIT, _('Credit')),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='payments')
    
    payment_number = models.CharField(_('payment number'), max_length=50, unique=True)
    payment_date = models.DateField(_('payment date'))
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('payment method'), max_length=20, choices=METHOD_CHOICES)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    cheque_number = models.CharField(_('cheque number'), max_length=50, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('supplier payment')
        verbose_name_plural = _('supplier payments')
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.payment_number} - {self.supplier.name} - {self.amount}"


class SupplierInvoice(ShopAwareModel):
    """
    Model for supplier invoices.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_VERIFIED = 'verified'
    STATUS_PAID = 'paid'
    STATUS_PARTIALLY_PAID = 'partially_paid'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_VERIFIED, _('Verified')),
        (STATUS_PAID, _('Paid')),
        (STATUS_PARTIALLY_PAID, _('Partially Paid')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='invoices')
    goods_receipt = models.ForeignKey('goods_receipt.GoodsReceipt', on_delete=models.PROTECT, related_name='invoices', null=True, blank=True)
    
    invoice_number = models.CharField(_('invoice number'), max_length=50)
    invoice_date = models.DateField(_('invoice date'))
    
    due_date = models.DateField(_('due date'))
    
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(_('tax amount'), max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(_('discount amount'), max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(_('shipping amount'), max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2)
    
    amount_paid = models.DecimalField(_('amount paid'), max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(_('balance due'), max_digits=10, decimal_places=2)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # Invoice image
    invoice_image = models.ImageField(_('invoice image'), upload_to='supplier_invoices/', null=True, blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    verified_by = models.UUIDField(_('verified by'), null=True, blank=True)
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('supplier invoice')
        verbose_name_plural = _('supplier invoices')
        ordering = ['-invoice_date']
        unique_together = ('supplier', 'invoice_number')
    
    def __str__(self):
        return f"{self.invoice_number} - {self.supplier.name} - {self.total_amount}"


class SupplierInvoicePayment(ShopAwareModel):
    """
    Model for payments against supplier invoices.
    """
    supplier_payment = models.ForeignKey(SupplierPayment, on_delete=models.CASCADE, related_name='invoice_payments')
    supplier_invoice = models.ForeignKey(SupplierInvoice, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('supplier invoice payment')
        verbose_name_plural = _('supplier invoice payments')
        unique_together = ('supplier_payment', 'supplier_invoice')
    
    def __str__(self):
        return f"{self.supplier_payment.payment_number} - {self.supplier_invoice.invoice_number} - {self.amount}"