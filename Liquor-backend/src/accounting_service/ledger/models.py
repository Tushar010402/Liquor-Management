import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel, ShopAwareModel
from accounting_service.accounts.models import Account, FiscalYear, AccountingPeriod
from accounting_service.journals.models import Journal, JournalEntry


class GeneralLedger(TenantAwareModel):
    """
    Model for general ledger entries.
    """
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='ledger_entries')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='ledger_entries')
    journal_entry = models.OneToOneField(JournalEntry, on_delete=models.CASCADE, related_name='ledger_entry')
    
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT, related_name='ledger_entries')
    accounting_period = models.ForeignKey(AccountingPeriod, on_delete=models.PROTECT, related_name='ledger_entries')
    
    transaction_date = models.DateField(_('transaction date'))
    
    description = models.CharField(_('description'), max_length=255, blank=True)
    
    debit_amount = models.DecimalField(_('debit amount'), max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(_('credit amount'), max_digits=15, decimal_places=2, default=0)
    balance = models.DecimalField(_('balance'), max_digits=15, decimal_places=2, default=0)
    
    shop_id = models.UUIDField(_('shop ID'), null=True, blank=True)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True)
    reference_id = models.UUIDField(_('reference ID'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('general ledger entry')
        verbose_name_plural = _('general ledger entries')
        ordering = ['transaction_date', 'id']
        indexes = [
            models.Index(fields=['tenant_id', 'account', 'transaction_date']),
            models.Index(fields=['tenant_id', 'fiscal_year', 'accounting_period']),
            models.Index(fields=['tenant_id', 'reference_type', 'reference_id']),
        ]
    
    def __str__(self):
        return f"{self.account.name} - {self.transaction_date} - {self.debit_amount or self.credit_amount}"


class AccountBalance(TenantAwareModel):
    """
    Model for account balances.
    """
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='balances')
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT, related_name='account_balances')
    accounting_period = models.ForeignKey(AccountingPeriod, on_delete=models.PROTECT, related_name='account_balances')
    
    opening_balance = models.DecimalField(_('opening balance'), max_digits=15, decimal_places=2, default=0)
    current_balance = models.DecimalField(_('current balance'), max_digits=15, decimal_places=2, default=0)
    
    total_debits = models.DecimalField(_('total debits'), max_digits=15, decimal_places=2, default=0)
    total_credits = models.DecimalField(_('total credits'), max_digits=15, decimal_places=2, default=0)
    
    shop_id = models.UUIDField(_('shop ID'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('account balance')
        verbose_name_plural = _('account balances')
        ordering = ['fiscal_year', 'accounting_period', 'account']
        unique_together = ('tenant_id', 'account', 'fiscal_year', 'accounting_period', 'shop_id')
    
    def __str__(self):
        return f"{self.account.name} - {self.accounting_period.name} - {self.current_balance}"


class TrialBalance(TenantAwareModel):
    """
    Model for trial balance.
    """
    # Status choices
    STATUS_DRAFT = 'draft'
    STATUS_FINAL = 'final'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_FINAL, _('Final')),
    ]
    
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT, related_name='trial_balances')
    accounting_period = models.ForeignKey(AccountingPeriod, on_delete=models.PROTECT, related_name='trial_balances')
    
    as_of_date = models.DateField(_('as of date'))
    
    total_debits = models.DecimalField(_('total debits'), max_digits=15, decimal_places=2, default=0)
    total_credits = models.DecimalField(_('total credits'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    finalized_by = models.UUIDField(_('finalized by'), null=True, blank=True)
    finalized_at = models.DateTimeField(_('finalized at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('trial balance')
        verbose_name_plural = _('trial balances')
        ordering = ['-as_of_date']
        unique_together = ('tenant_id', 'fiscal_year', 'accounting_period', 'as_of_date')
    
    def __str__(self):
        return f"Trial Balance - {self.accounting_period.name} - {self.as_of_date}"


class TrialBalanceEntry(TenantAwareModel):
    """
    Model for trial balance entries.
    """
    trial_balance = models.ForeignKey(TrialBalance, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='trial_balance_entries')
    
    debit_amount = models.DecimalField(_('debit amount'), max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(_('credit amount'), max_digits=15, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = _('trial balance entry')
        verbose_name_plural = _('trial balance entries')
        ordering = ['account__code']
        unique_together = ('trial_balance', 'account')
    
    def __str__(self):
        return f"{self.account.name} - Dr: {self.debit_amount}, Cr: {self.credit_amount}"
