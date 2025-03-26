from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel


class Shop(TenantAwareModel):
    """
    Model for shops (stores/outlets) in the system.
    """
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    
    # Location coordinates
    latitude = models.DecimalField(_('latitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Business details
    license_number = models.CharField(_('license number'), max_length=50, blank=True)
    license_expiry = models.DateField(_('license expiry'), null=True, blank=True)
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    
    # Shop manager
    manager_id = models.UUIDField(_('manager ID'), null=True, blank=True)
    manager_name = models.CharField(_('manager name'), max_length=100, blank=True)
    manager_phone = models.CharField(_('manager phone'), max_length=20, blank=True)
    manager_email = models.EmailField(_('manager email'), blank=True)
    
    # Shop status
    is_open = models.BooleanField(_('is open'), default=True)
    
    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ['name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ShopOperatingHours(TenantAwareModel):
    """
    Model for shop operating hours.
    """
    DAYS_OF_WEEK = [
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    ]
    
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='operating_hours')
    day_of_week = models.PositiveSmallIntegerField(_('day of week'), choices=DAYS_OF_WEEK)
    opening_time = models.TimeField(_('opening time'))
    closing_time = models.TimeField(_('closing time'))
    is_closed = models.BooleanField(_('is closed'), default=False)
    
    class Meta:
        verbose_name = _('shop operating hours')
        verbose_name_plural = _('shop operating hours')
        ordering = ['day_of_week', 'opening_time']
        unique_together = ('shop', 'day_of_week')
    
    def __str__(self):
        if self.is_closed:
            return f"{self.shop.name} - {self.get_day_of_week_display()} (Closed)"
        return f"{self.shop.name} - {self.get_day_of_week_display()} ({self.opening_time} - {self.closing_time})"


class ShopHoliday(TenantAwareModel):
    """
    Model for shop holidays.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='holidays')
    name = models.CharField(_('name'), max_length=100)
    date = models.DateField(_('date'))
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('shop holiday')
        verbose_name_plural = _('shop holidays')
        ordering = ['date']
        unique_together = ('shop', 'date')
    
    def __str__(self):
        return f"{self.shop.name} - {self.name} ({self.date})"


class ShopSettings(TenantAwareModel):
    """
    Model for shop-specific settings.
    """
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='settings')
    
    # Inventory settings
    enable_low_stock_alerts = models.BooleanField(_('enable low stock alerts'), default=True)
    low_stock_threshold = models.PositiveIntegerField(_('low stock threshold'), default=10)
    enable_expiry_alerts = models.BooleanField(_('enable expiry alerts'), default=True)
    expiry_alert_days = models.PositiveIntegerField(_('expiry alert days'), default=30)
    
    # Sales settings
    default_tax_rate = models.DecimalField(_('default tax rate'), max_digits=5, decimal_places=2, default=0)
    enable_discounts = models.BooleanField(_('enable discounts'), default=True)
    max_discount_percentage = models.DecimalField(_('max discount percentage'), max_digits=5, decimal_places=2, default=10)
    require_discount_approval = models.BooleanField(_('require discount approval'), default=True)
    discount_approval_threshold = models.DecimalField(_('discount approval threshold'), max_digits=5, decimal_places=2, default=5)
    
    # Receipt settings
    receipt_header = models.TextField(_('receipt header'), blank=True)
    receipt_footer = models.TextField(_('receipt footer'), blank=True)
    show_tax_on_receipt = models.BooleanField(_('show tax on receipt'), default=True)
    
    # Cash management settings
    enable_cash_management = models.BooleanField(_('enable cash management'), default=True)
    require_cash_verification = models.BooleanField(_('require cash verification'), default=True)
    
    class Meta:
        verbose_name = _('shop settings')
        verbose_name_plural = _('shop settings')
    
    def __str__(self):
        return f"{self.shop.name} Settings"