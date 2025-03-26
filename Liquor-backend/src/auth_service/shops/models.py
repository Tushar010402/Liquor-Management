import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class Shop(BaseModel):
    """
    Shop model for managing multiple shops under a tenant.
    """
    # Status choices
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_SUSPENDED = 'suspended'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
        (STATUS_SUSPENDED, _('Suspended')),
    ]
    
    # Shop type choices
    TYPE_RETAIL = 'retail'
    TYPE_WHOLESALE = 'wholesale'
    TYPE_BOTH = 'both'
    
    TYPE_CHOICES = [
        (TYPE_RETAIL, _('Retail')),
        (TYPE_WHOLESALE, _('Wholesale')),
        (TYPE_BOTH, _('Both')),
    ]
    
    tenant_id = models.UUIDField(_('tenant ID'))
    name = models.CharField(_('shop name'), max_length=100)
    code = models.CharField(_('shop code'), max_length=20)
    shop_type = models.CharField(_('shop type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_RETAIL)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    # Location details
    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=20)
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Contact information
    phone = models.CharField(_('phone'), max_length=20)
    email = models.EmailField(_('email'), blank=True)
    
    # License information
    license_number = models.CharField(_('license number'), max_length=50)
    license_type = models.CharField(_('license type'), max_length=50)
    license_expiry = models.DateField(_('license expiry'))
    
    # Operating hours
    opening_time = models.TimeField(_('opening time'))
    closing_time = models.TimeField(_('closing time'))
    is_open_on_sunday = models.BooleanField(_('open on Sunday'), default=True)
    is_open_on_monday = models.BooleanField(_('open on Monday'), default=True)
    is_open_on_tuesday = models.BooleanField(_('open on Tuesday'), default=True)
    is_open_on_wednesday = models.BooleanField(_('open on Wednesday'), default=True)
    is_open_on_thursday = models.BooleanField(_('open on Thursday'), default=True)
    is_open_on_friday = models.BooleanField(_('open on Friday'), default=True)
    is_open_on_saturday = models.BooleanField(_('open on Saturday'), default=True)
    
    # Additional information
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(_('image'), upload_to='shop_images/', null=True, blank=True)
    
    # Metadata
    created_by = models.UUIDField(_('created by'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ShopSettings(BaseModel):
    """
    Settings specific to a shop.
    """
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='settings')
    
    # Inventory settings
    enable_low_stock_alerts = models.BooleanField(_('enable low stock alerts'), default=True)
    low_stock_threshold = models.PositiveIntegerField(_('low stock threshold'), default=10)
    enable_expiry_alerts = models.BooleanField(_('enable expiry alerts'), default=True)
    expiry_alert_days = models.PositiveIntegerField(_('expiry alert days'), default=30)
    
    # Sales settings
    default_tax_rate = models.DecimalField(_('default tax rate'), max_digits=5, decimal_places=2, default=18.00)
    enable_discounts = models.BooleanField(_('enable discounts'), default=True)
    max_discount_percentage = models.DecimalField(_('maximum discount percentage'), max_digits=5, decimal_places=2, default=10.00)
    require_discount_approval = models.BooleanField(_('require discount approval'), default=True)
    discount_approval_threshold = models.DecimalField(_('discount approval threshold'), max_digits=5, decimal_places=2, default=5.00)
    
    # Approval settings
    require_sales_approval = models.BooleanField(_('require sales approval'), default=False)
    require_stock_adjustment_approval = models.BooleanField(_('require stock adjustment approval'), default=True)
    require_return_approval = models.BooleanField(_('require return approval'), default=True)
    
    # Receipt settings
    receipt_header = models.TextField(_('receipt header'), blank=True)
    receipt_footer = models.TextField(_('receipt footer'), blank=True)
    show_tax_on_receipt = models.BooleanField(_('show tax on receipt'), default=True)
    
    # Other settings
    settings_json = models.JSONField(_('additional settings'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('shop settings')
        verbose_name_plural = _('shop settings')
    
    def __str__(self):
        return f"Settings for {self.shop.name}"


class ShopActivity(BaseModel):
    """
    Activity log for shops.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='activities')
    user_id = models.UUIDField(_('user ID'), null=True, blank=True)
    activity_type = models.CharField(_('activity type'), max_length=50)
    description = models.TextField(_('description'))
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('shop activity')
        verbose_name_plural = _('shop activities')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.shop.name} - {self.activity_type} - {self.created_at}"