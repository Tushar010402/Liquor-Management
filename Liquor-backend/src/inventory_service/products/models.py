from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel
from brands.models import Brand


class ProductCategory(TenantAwareModel):
    """
    Model for product categories.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    
    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class ProductType(TenantAwareModel):
    """
    Model for product types (e.g., Beer, Wine, Whiskey).
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('product type')
        verbose_name_plural = _('product types')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class Product(TenantAwareModel):
    """
    Model for products.
    """
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    barcode = models.CharField(_('barcode'), max_length=50, blank=True)
    description = models.TextField(_('description'), blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Pricing
    mrp = models.DecimalField(_('MRP'), max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(_('selling price'), max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(_('purchase price'), max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    
    # Physical attributes
    volume_ml = models.PositiveIntegerField(_('volume (ml)'), null=True, blank=True)
    weight_grams = models.PositiveIntegerField(_('weight (grams)'), null=True, blank=True)
    alcohol_percentage = models.DecimalField(_('alcohol percentage'), max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Images
    image = models.ImageField(_('image'), upload_to='product_images/', null=True, blank=True)
    
    # Status
    is_available = models.BooleanField(_('is available'), default=True)
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ProductVariant(TenantAwareModel):
    """
    Model for product variants (e.g., different sizes, flavors).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    barcode = models.CharField(_('barcode'), max_length=50, blank=True)
    
    # Pricing
    mrp = models.DecimalField(_('MRP'), max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(_('selling price'), max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(_('purchase price'), max_digits=10, decimal_places=2)
    
    # Physical attributes
    volume_ml = models.PositiveIntegerField(_('volume (ml)'), null=True, blank=True)
    weight_grams = models.PositiveIntegerField(_('weight (grams)'), null=True, blank=True)
    
    # Images
    image = models.ImageField(_('image'), upload_to='product_variant_images/', null=True, blank=True)
    
    # Status
    is_available = models.BooleanField(_('is available'), default=True)
    
    class Meta:
        verbose_name = _('product variant')
        verbose_name_plural = _('product variants')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.product.name} - {self.name} ({self.code})"


class ProductAttribute(TenantAwareModel):
    """
    Model for product attributes (e.g., color, flavor, region).
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('product attribute')
        verbose_name_plural = _('product attributes')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class ProductAttributeValue(TenantAwareModel):
    """
    Model for product attribute values.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(_('value'), max_length=100)
    
    class Meta:
        verbose_name = _('product attribute value')
        verbose_name_plural = _('product attribute values')
        ordering = ['attribute__name', 'value']
        unique_together = ('product', 'attribute')
    
    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class ProductPriceHistory(TenantAwareModel):
    """
    Model for tracking product price history.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    mrp = models.DecimalField(_('MRP'), max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(_('selling price'), max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(_('purchase price'), max_digits=10, decimal_places=2)
    effective_from = models.DateTimeField(_('effective from'))
    effective_to = models.DateTimeField(_('effective to'), null=True, blank=True)
    changed_by = models.UUIDField(_('changed by'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('product price history')
        verbose_name_plural = _('product price histories')
        ordering = ['-effective_from']
    
    def __str__(self):
        return f"{self.product.name} - {self.effective_from}"