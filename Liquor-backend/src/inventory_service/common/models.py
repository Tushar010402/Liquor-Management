import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Base model for all models in the system.
    Provides common fields and functionality.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self):
        """
        Soft delete the object by setting is_active to False
        and updating the updated_at timestamp.
        """
        self.is_active = False
        self.updated_at = timezone.now()
        self.save(update_fields=['is_active', 'updated_at'])
        
    def restore(self):
        """
        Restore a soft-deleted object by setting is_active to True
        and updating the updated_at timestamp.
        """
        self.is_active = True
        self.updated_at = timezone.now()
        self.save(update_fields=['is_active', 'updated_at'])


class TenantAwareModel(BaseModel):
    """
    Base model for all tenant-aware models.
    Ensures data isolation between tenants.
    """
    tenant_id = models.UUIDField(db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class ShopAwareModel(TenantAwareModel):
    """
    Base model for all shop-aware models.
    Ensures data isolation between shops.
    """
    shop_id = models.UUIDField(db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']