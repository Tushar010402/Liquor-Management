from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel, TenantAwareModel


class SystemSetting(BaseModel):
    """
    Model for system-wide settings.
    """
    key = models.CharField(_('key'), max_length=100, unique=True)
    value = models.TextField(_('value'))
    description = models.TextField(_('description'), blank=True)
    is_public = models.BooleanField(_('is public'), default=False)
    
    class Meta:
        verbose_name = _('system setting')
        verbose_name_plural = _('system settings')
        ordering = ['key']
    
    def __str__(self):
        return self.key


class TenantSetting(TenantAwareModel):
    """
    Model for tenant-specific settings.
    """
    key = models.CharField(_('key'), max_length=100)
    value = models.TextField(_('value'))
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('tenant setting')
        verbose_name_plural = _('tenant settings')
        ordering = ['key']
        unique_together = ('tenant_id', 'key')
    
    def __str__(self):
        return f"{self.tenant_id} - {self.key}"


class EmailTemplate(TenantAwareModel):
    """
    Model for email templates.
    """
    name = models.CharField(_('name'), max_length=100)
    subject = models.CharField(_('subject'), max_length=255)
    body = models.TextField(_('body'))
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return f"{self.tenant_id} - {self.name}"


class NotificationTemplate(TenantAwareModel):
    """
    Model for notification templates.
    """
    name = models.CharField(_('name'), max_length=100)
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('body'))
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('notification template')
        verbose_name_plural = _('notification templates')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return f"{self.tenant_id} - {self.name}"