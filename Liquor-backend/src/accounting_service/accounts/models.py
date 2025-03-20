import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel


class AccountType(TenantAwareModel):
    """
    Model for account types.
    """
    # Type choices
    TYPE_ASSET = 'asset'
    TYPE_LIABILITY = 'liability'
    TYPE_EQUITY = 'equity'
    TYPE_REVENUE = 'revenue'
    TYPE_EXPENSE = 'expense'
    
    TYPE_CHOICES = [
        (TYPE_ASSET, _('Asset')),
        (TYPE_LIABILITY, _('Liability')),
        (TYPE_EQUITY, _('Equity')),
        (TYPE_REVENUE, _('Revenue')),
        (TYPE_EXPENSE, _('Expense')),
    ]
    
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(_('description'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('account type')
        verbose_name_plural = _('account types')
        ordering = ['code', 'name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Account(TenantAwareModel):
    """
    Model for accounts in the chart of accounts.
    """
    # Status choices
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
        (STATUS_ARCHIVED, _('Archived')),
    ]
    
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='accounts')
    
    name = models.CharField(_('name'), max_length=100)
    code = models.CharField(_('code'), max_length=20)
    description = models.TextField(_('description'), blank=True)
    
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True)
    
    is_bank_account = models.BooleanField(_('is bank account'), default=False)
    is_cash_account = models.BooleanField(_('is cash account'), default=False)
    is_control_account = models.BooleanField(_('is control account'), default=False)
    
    opening_balance = models.DecimalField(_('opening balance'), max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(_('current balance'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
        ordering = ['code', 'name']
        unique_together = ('tenant_id', 'code')
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class FiscalYear(TenantAwareModel):
    """
    Model for fiscal years.
    """
    # Status choices
    STATUS_UPCOMING = 'upcoming'
    STATUS_ACTIVE = 'active'
    STATUS_CLOSED = 'closed'
    
    STATUS_CHOICES = [
        (STATUS_UPCOMING, _('Upcoming')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_CLOSED, _('Closed')),
    ]
    
    name = models.CharField(_('name'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_UPCOMING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    closed_by = models.UUIDField(_('closed by'), null=True, blank=True)
    closed_at = models.DateTimeField(_('closed at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('fiscal year')
        verbose_name_plural = _('fiscal years')
        ordering = ['-start_date']
        unique_together = ('tenant_id', 'name')
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"


class AccountingPeriod(TenantAwareModel):
    """
    Model for accounting periods.
    """
    # Status choices
    STATUS_UPCOMING = 'upcoming'
    STATUS_ACTIVE = 'active'
    STATUS_CLOSED = 'closed'
    
    STATUS_CHOICES = [
        (STATUS_UPCOMING, _('Upcoming')),
        (STATUS_ACTIVE, _('Active')),
        (STATUS_CLOSED, _('Closed')),
    ]
    
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, related_name='periods')
    
    name = models.CharField(_('name'), max_length=100)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_UPCOMING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    closed_by = models.UUIDField(_('closed by'), null=True, blank=True)
    closed_at = models.DateTimeField(_('closed at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('accounting period')
        verbose_name_plural = _('accounting periods')
        ordering = ['-start_date']
        unique_together = ('tenant_id', 'fiscal_year', 'name')
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"


class BankAccount(TenantAwareModel):
    """
    Model for bank accounts.
    """
    # Status choices
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
    ]
    
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='bank_account')
    
    bank_name = models.CharField(_('bank name'), max_length=100)
    account_number = models.CharField(_('account number'), max_length=50)
    account_name = models.CharField(_('account name'), max_length=100)
    branch = models.CharField(_('branch'), max_length=100, blank=True)
    ifsc_code = models.CharField(_('IFSC code'), max_length=20, blank=True)
    
    opening_balance = models.DecimalField(_('opening balance'), max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(_('current balance'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('bank account')
        verbose_name_plural = _('bank accounts')
        ordering = ['bank_name', 'account_number']
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"