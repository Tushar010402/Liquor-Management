"""
Common models for the Liquor Management System.
This file defines base models that are used across all services.
"""

from django.db import models
from django.utils import timezone
import uuid

class BaseModel(models.Model):
    """
    Base model for all models in the system.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'common'

class TenantAwareModel(BaseModel):
    """
    Base model for all tenant-aware models in the system.
    """
    tenant_id = models.UUIDField()
    shop_id = models.UUIDField(null=True, blank=True)

    class Meta:
        abstract = True
        app_label = 'common'

class ShopAwareModel(BaseModel):
    """
    Base model for all shop-aware models in the system.
    """
    tenant_id = models.UUIDField()
    shop_id = models.UUIDField()

    class Meta:
        abstract = True
        app_label = 'common'
