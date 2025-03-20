import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel


class Permission(BaseModel):
    """
    Permission model for defining granular permissions.
    """
    # Permission categories
    CATEGORY_INVENTORY = 'inventory'
    CATEGORY_SALES = 'sales'
    CATEGORY_PURCHASE = 'purchase'
    CATEGORY_ACCOUNTING = 'accounting'
    CATEGORY_REPORTS = 'reports'
    CATEGORY_SETTINGS = 'settings'
    CATEGORY_USERS = 'users'
    
    CATEGORY_CHOICES = [
        (CATEGORY_INVENTORY, _('Inventory')),
        (CATEGORY_SALES, _('Sales')),
        (CATEGORY_PURCHASE, _('Purchase')),
        (CATEGORY_ACCOUNTING, _('Accounting')),
        (CATEGORY_REPORTS, _('Reports')),
        (CATEGORY_SETTINGS, _('Settings')),
        (CATEGORY_USERS, _('Users')),
    ]
    
    code = models.CharField(_('permission code'), max_length=100, unique=True)
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    category = models.CharField(_('category'), max_length=20, choices=CATEGORY_CHOICES)
    
    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Role(BaseModel):
    """
    Role model for defining user roles.
    """
    tenant_id = models.UUIDField(_('tenant ID'), null=True, blank=True)
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    is_system_role = models.BooleanField(_('is system role'), default=False)
    permissions = models.ManyToManyField(Permission, through='RolePermission', related_name='roles')
    
    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        ordering = ['name']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return self.name


class RolePermission(BaseModel):
    """
    Many-to-many relationship between roles and permissions.
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('role permission')
        verbose_name_plural = _('role permissions')
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"