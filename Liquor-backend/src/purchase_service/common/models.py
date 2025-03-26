import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Base model for all models in the application.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        abstract = True


class TenantAwareModel(BaseModel):
    """
    Base model for all tenant-aware models in the application.
    """
    tenant_id = models.UUIDField(_('tenant ID'))
    
    class Meta:
        abstract = True


class ShopAwareModel(TenantAwareModel):
    """
    Base model for all shop-aware models in the application.
    """
    shop_id = models.UUIDField(_('shop ID'))
    
    class Meta:
        abstract = True