from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel


class BrandCategory(TenantAwareModel):
    """
    Model for brand categories.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('brand category')
        verbose_name_plural = _('brand categories')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class Brand(TenantAwareModel):
    """
    Model for brands.
    """
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    description = models.TextField(_('description'), blank=True)
    category = models.ForeignKey(BrandCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='brands')
    manufacturer = models.CharField(_('manufacturer'), max_length=100, blank=True)
    country_of_origin = models.CharField(_('country of origin'), max_length=100, blank=True)
    website = models.URLField(_('website'), blank=True)
    logo = models.ImageField(_('logo'), upload_to='brand_logos/', null=True, blank=True)
    
    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return self.name


class BrandSupplier(TenantAwareModel):
    """
    Model for brand-supplier relationships.
    """
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='suppliers')
    supplier_id = models.UUIDField(_('supplier ID'))
    supplier_name = models.CharField(_('supplier name'), max_length=100)
    is_primary = models.BooleanField(_('is primary'), default=False)
    
    class Meta:
        verbose_name = _('brand supplier')
        verbose_name_plural = _('brand suppliers')
        ordering = ['-is_primary', 'supplier_name']
        unique_together = ('brand', 'supplier_id')
    
    def __str__(self):
        return f"{self.brand.name} - {self.supplier_name}"