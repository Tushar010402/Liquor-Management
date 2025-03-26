import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class BillingPlan(BaseModel):
    """
    Billing plans for tenants.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    price_monthly = models.DecimalField(_('monthly price'), max_digits=10, decimal_places=2)
    price_yearly = models.DecimalField(_('yearly price'), max_digits=10, decimal_places=2)
    max_shops = models.PositiveIntegerField(_('maximum shops'), default=1)
    max_users = models.PositiveIntegerField(_('maximum users'), default=5)
    features = models.JSONField(_('features'), default=dict)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        verbose_name = _('billing plan')
        verbose_name_plural = _('billing plans')
        ordering = ['price_monthly']
    
    def __str__(self):
        return self.name


class Tenant(BaseModel):
    """
    Tenant model for multi-tenant architecture.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_SUSPENDED, _('Suspended')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Billing cycle choices
    BILLING_MONTHLY = 'monthly'
    BILLING_YEARLY = 'yearly'
    
    BILLING_CYCLE_CHOICES = [
        (BILLING_MONTHLY, _('Monthly')),
        (BILLING_YEARLY, _('Yearly')),
    ]
    
    name = models.CharField(_('tenant name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    domain = models.CharField(_('domain'), max_length=100, blank=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    # Business details
    business_name = models.CharField(_('business name'), max_length=200)
    business_address = models.TextField(_('business address'))
    business_phone = models.CharField(_('business phone'), max_length=20)
    business_email = models.EmailField(_('business email'))
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    registration_number = models.CharField(_('registration number'), max_length=50, blank=True)
    
    # Contact person
    contact_name = models.CharField(_('contact name'), max_length=100)
    contact_email = models.EmailField(_('contact email'))
    contact_phone = models.CharField(_('contact phone'), max_length=20)
    
    # Billing information
    billing_plan = models.ForeignKey(BillingPlan, on_delete=models.PROTECT, related_name='tenants')
    billing_cycle = models.CharField(_('billing cycle'), max_length=10, choices=BILLING_CYCLE_CHOICES, default=BILLING_MONTHLY)
    billing_address = models.TextField(_('billing address'), blank=True)
    billing_email = models.EmailField(_('billing email'), blank=True)
    
    # Subscription details
    subscription_start_date = models.DateField(_('subscription start date'), null=True, blank=True)
    subscription_end_date = models.DateField(_('subscription end date'), null=True, blank=True)
    is_trial = models.BooleanField(_('is trial'), default=False)
    trial_end_date = models.DateField(_('trial end date'), null=True, blank=True)
    
    # Customization
    logo = models.ImageField(_('logo'), upload_to='tenant_logos/', null=True, blank=True)
    primary_color = models.CharField(_('primary color'), max_length=7, default='#007bff')
    secondary_color = models.CharField(_('secondary color'), max_length=7, default='#6c757d')
    
    # Metadata
    created_by = models.UUIDField(_('created by'), null=True, blank=True)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('tenant')
        verbose_name_plural = _('tenants')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TenantBillingHistory(BaseModel):
    """
    Billing history for tenants.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_PAID, _('Paid')),
        (STATUS_FAILED, _('Failed')),
        (STATUS_REFUNDED, _('Refunded')),
    ]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='billing_history')
    billing_plan = models.ForeignKey(BillingPlan, on_delete=models.PROTECT, related_name='billing_history')
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    invoice_number = models.CharField(_('invoice number'), max_length=50, unique=True)
    invoice_date = models.DateField(_('invoice date'))
    due_date = models.DateField(_('due date'))
    payment_date = models.DateField(_('payment date'), null=True, blank=True)
    payment_method = models.CharField(_('payment method'), max_length=50, blank=True)
    payment_reference = models.CharField(_('payment reference'), max_length=100, blank=True)
    billing_period_start = models.DateField(_('billing period start'))
    billing_period_end = models.DateField(_('billing period end'))
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('tenant billing history')
        verbose_name_plural = _('tenant billing history')
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.invoice_number}"


class TenantActivity(BaseModel):
    """
    Activity log for tenants.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='activities')
    user_id = models.UUIDField(_('user ID'), null=True, blank=True)
    activity_type = models.CharField(_('activity type'), max_length=50)
    description = models.TextField(_('description'))
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    user_agent = models.TextField(_('user agent'), blank=True)
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    
    class Meta:
        verbose_name = _('tenant activity')
        verbose_name_plural = _('tenant activities')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.activity_type} - {self.created_at}"