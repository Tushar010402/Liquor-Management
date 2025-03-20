from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel


class SupplierCategory(TenantAwareModel):
    """
    Model for supplier categories.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('supplier category')
        verbose_name_plural = _('supplier categories')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class Supplier(TenantAwareModel):
    """
    Model for suppliers.
    """
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    category = models.ForeignKey(SupplierCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='suppliers')
    
    # Contact information
    contact_person = models.CharField(_('contact person'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), blank=True)
    
    # Address
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    
    # Business details
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    license_number = models.CharField(_('license number'), max_length=50, blank=True)
    license_expiry = models.DateField(_('license expiry'), null=True, blank=True)
    
    # Payment terms
    payment_terms = models.CharField(_('payment terms'), max_length=100, blank=True)
    credit_limit = models.DecimalField(_('credit limit'), max_digits=10, decimal_places=2, null=True, blank=True)
    credit_days = models.PositiveIntegerField(_('credit days'), null=True, blank=True)
    
    # Status
    is_approved = models.BooleanField(_('is approved'), default=True)
    
    # Notes
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class SupplierContact(TenantAwareModel):
    """
    Model for supplier contacts.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(_('name'), max_length=100)
    designation = models.CharField(_('designation'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    is_primary = models.BooleanField(_('is primary'), default=False)
    
    class Meta:
        verbose_name = _('supplier contact')
        verbose_name_plural = _('supplier contacts')
        ordering = ['-is_primary', 'name']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.name}"


class SupplierBankAccount(TenantAwareModel):
    """
    Model for supplier bank accounts.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(_('bank name'), max_length=100)
    account_number = models.CharField(_('account number'), max_length=50)
    account_name = models.CharField(_('account name'), max_length=100)
    branch = models.CharField(_('branch'), max_length=100, blank=True)
    ifsc_code = models.CharField(_('IFSC code'), max_length=20, blank=True)
    is_primary = models.BooleanField(_('is primary'), default=False)
    
    class Meta:
        verbose_name = _('supplier bank account')
        verbose_name_plural = _('supplier bank accounts')
        ordering = ['-is_primary', 'bank_name']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.bank_name} - {self.account_number}"


class SupplierDocument(TenantAwareModel):
    """
    Model for supplier documents.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(_('name'), max_length=100)
    document_type = models.CharField(_('document type'), max_length=50)
    document = models.FileField(_('document'), upload_to='supplier_documents/')
    expiry_date = models.DateField(_('expiry date'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('supplier document')
        verbose_name_plural = _('supplier documents')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.supplier.name} - {self.name}"