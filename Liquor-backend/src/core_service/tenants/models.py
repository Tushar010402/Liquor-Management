from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class Tenant(BaseModel):
    """
    Model for tenants (companies/organizations) in the system.
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    state = models.CharField(_('state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), blank=True)
    
    # Business details
    business_type = models.CharField(_('business type'), max_length=50, blank=True)
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    license_number = models.CharField(_('license number'), max_length=50, blank=True)
    license_expiry = models.DateField(_('license expiry'), null=True, blank=True)
    
    # Subscription details
    subscription_plan = models.CharField(_('subscription plan'), max_length=50, default='basic')
    subscription_start_date = models.DateField(_('subscription start date'), null=True, blank=True)
    subscription_end_date = models.DateField(_('subscription end date'), null=True, blank=True)
    max_shops = models.PositiveIntegerField(_('maximum shops'), default=1)
    max_users = models.PositiveIntegerField(_('maximum users'), default=5)
    
    # Contact person
    contact_person_name = models.CharField(_('contact person name'), max_length=100, blank=True)
    contact_person_email = models.EmailField(_('contact person email'), blank=True)
    contact_person_phone = models.CharField(_('contact person phone'), max_length=20, blank=True)
    
    # Branding
    logo = models.ImageField(_('logo'), upload_to='tenant_logos/', null=True, blank=True)
    primary_color = models.CharField(_('primary color'), max_length=7, default='#4a6da7')
    secondary_color = models.CharField(_('secondary color'), max_length=7, default='#ffffff')
    
    class Meta:
        verbose_name = _('tenant')
        verbose_name_plural = _('tenants')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TenantSettings(BaseModel):
    """
    Model for tenant-specific settings.
    """
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
    
    # General settings
    timezone = models.CharField(_('timezone'), max_length=50, default='UTC')
    date_format = models.CharField(_('date format'), max_length=20, default='YYYY-MM-DD')
    time_format = models.CharField(_('time format'), max_length=20, default='HH:mm:ss')
    currency = models.CharField(_('currency'), max_length=3, default='USD')
    language = models.CharField(_('language'), max_length=10, default='en-US')
    
    # Business settings
    fiscal_year_start = models.CharField(_('fiscal year start'), max_length=5, default='01-01')
    tax_rate = models.DecimalField(_('tax rate'), max_digits=5, decimal_places=2, default=0)
    enable_tax = models.BooleanField(_('enable tax'), default=True)
    
    # Security settings
    require_2fa = models.BooleanField(_('require 2FA'), default=False)
    password_expiry_days = models.PositiveIntegerField(_('password expiry days'), default=90)
    session_timeout_minutes = models.PositiveIntegerField(_('session timeout minutes'), default=30)
    
    # Notification settings
    enable_email_notifications = models.BooleanField(_('enable email notifications'), default=True)
    enable_sms_notifications = models.BooleanField(_('enable SMS notifications'), default=False)
    
    # Approval settings
    require_sales_approval = models.BooleanField(_('require sales approval'), default=True)
    require_purchase_approval = models.BooleanField(_('require purchase approval'), default=True)
    require_expense_approval = models.BooleanField(_('require expense approval'), default=True)
    
    # Feature flags
    enable_inventory_management = models.BooleanField(_('enable inventory management'), default=True)
    enable_financial_management = models.BooleanField(_('enable financial management'), default=True)
    enable_reports = models.BooleanField(_('enable reports'), default=True)
    enable_analytics = models.BooleanField(_('enable analytics'), default=True)
    
    class Meta:
        verbose_name = _('tenant settings')
        verbose_name_plural = _('tenant settings')
    
    def __str__(self):
        return f"{self.tenant.name} Settings"