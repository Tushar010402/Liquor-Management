import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel


class Approval(ShopAwareModel):
    """
    Model for approval requests.
    """
    # Approval type choices
    TYPE_SALE = 'sale'
    TYPE_RETURN = 'return'
    TYPE_STOCK_ADJUSTMENT = 'stock_adjustment'
    TYPE_DEPOSIT = 'deposit'
    TYPE_EXPENSE = 'expense'
    TYPE_DISCOUNT = 'discount'
    TYPE_BATCH_SALE = 'batch_sale'
    
    TYPE_CHOICES = [
        (TYPE_SALE, _('Sale')),
        (TYPE_RETURN, _('Return')),
        (TYPE_STOCK_ADJUSTMENT, _('Stock Adjustment')),
        (TYPE_DEPOSIT, _('Deposit')),
        (TYPE_EXPENSE, _('Expense')),
        (TYPE_DISCOUNT, _('Discount')),
        (TYPE_BATCH_SALE, _('Batch Sale')),
    ]
    
    # Approval status choices
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Priority choices
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_MEDIUM, _('Medium')),
        (PRIORITY_HIGH, _('High')),
    ]
    
    approval_number = models.CharField(_('approval number'), max_length=50, unique=True)
    approval_date = models.DateTimeField(_('approval date'), auto_now_add=True)
    
    approval_type = models.CharField(_('approval type'), max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.CharField(_('priority'), max_length=20, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM)
    
    reference_id = models.UUIDField(_('reference ID'))
    reference_number = models.CharField(_('reference number'), max_length=50)
    reference_data = models.JSONField(_('reference data'), default=dict)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    requested_by = models.UUIDField(_('requested by'))
    requested_by_name = models.CharField(_('requested by name'), max_length=100)
    
    approved_by = models.UUIDField(_('approved by'), null=True, blank=True)
    approved_by_name = models.CharField(_('approved by name'), max_length=100, blank=True)
    approved_at = models.DateTimeField(_('approved at'), null=True, blank=True)
    
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    class Meta:
        verbose_name = _('approval')
        verbose_name_plural = _('approvals')
        ordering = ['-approval_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'approval_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['tenant_id', 'shop_id', 'approval_type']),
            models.Index(fields=['tenant_id', 'shop_id', 'requested_by']),
            models.Index(fields=['approval_number']),
        ]
    
    def __str__(self):
        return f"{self.approval_number} - {self.approval_type} - {self.status}"


class ApprovalHistory(ShopAwareModel):
    """
    Model for approval history.
    """
    # Action choices
    ACTION_CREATED = 'created'
    ACTION_UPDATED = 'updated'
    ACTION_APPROVED = 'approved'
    ACTION_REJECTED = 'rejected'
    ACTION_CANCELLED = 'cancelled'
    ACTION_RESUBMITTED = 'resubmitted'
    
    ACTION_CHOICES = [
        (ACTION_CREATED, _('Created')),
        (ACTION_UPDATED, _('Updated')),
        (ACTION_APPROVED, _('Approved')),
        (ACTION_REJECTED, _('Rejected')),
        (ACTION_CANCELLED, _('Cancelled')),
        (ACTION_RESUBMITTED, _('Resubmitted')),
    ]
    
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(_('action'), max_length=20, choices=ACTION_CHOICES)
    action_date = models.DateTimeField(_('action date'), auto_now_add=True)
    
    user_id = models.UUIDField(_('user ID'))
    user_name = models.CharField(_('user name'), max_length=100)
    
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('approval history')
        verbose_name_plural = _('approval history')
        ordering = ['-action_date']
    
    def __str__(self):
        return f"{self.approval.approval_number} - {self.action} - {self.action_date}"


class BatchApproval(ShopAwareModel):
    """
    Model for batch approvals.
    """
    # Status choices
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    batch_number = models.CharField(_('batch number'), max_length=50, unique=True)
    batch_date = models.DateTimeField(_('batch date'), auto_now_add=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    total_approvals = models.IntegerField(_('total approvals'), default=0)
    approved_count = models.IntegerField(_('approved count'), default=0)
    rejected_count = models.IntegerField(_('rejected count'), default=0)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    processed_by = models.UUIDField(_('processed by'))
    processed_by_name = models.CharField(_('processed by name'), max_length=100)
    
    class Meta:
        verbose_name = _('batch approval')
        verbose_name_plural = _('batch approvals')
        ordering = ['-batch_date']
    
    def __str__(self):
        return f"{self.batch_number} - {self.total_approvals} approvals"


class BatchApprovalItem(ShopAwareModel):
    """
    Model for items in a batch approval.
    """
    # Action choices
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    
    ACTION_CHOICES = [
        (ACTION_APPROVE, _('Approve')),
        (ACTION_REJECT, _('Reject')),
    ]
    
    batch = models.ForeignKey(BatchApproval, on_delete=models.CASCADE, related_name='items')
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE, related_name='batch_items')
    
    action = models.CharField(_('action'), max_length=20, choices=ACTION_CHOICES)
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('batch approval item')
        verbose_name_plural = _('batch approval items')
        unique_together = ('batch', 'approval')
    
    def __str__(self):
        return f"{self.batch.batch_number} - {self.approval.approval_number} - {self.action}"