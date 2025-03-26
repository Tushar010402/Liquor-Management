import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import TenantAwareModel, ShopAwareModel
from accounting_service.accounts.models import Account, FiscalYear, AccountingPeriod


class Journal(TenantAwareModel):
    """
    Model for journals.
    """
    # Status choices
    STATUS_DRAFT = 'draft'
    STATUS_POSTED = 'posted'
    STATUS_REVERSED = 'reversed'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_POSTED, _('Posted')),
        (STATUS_REVERSED, _('Reversed')),
    ]
    
    # Type choices
    TYPE_GENERAL = 'general'
    TYPE_SALES = 'sales'
    TYPE_PURCHASE = 'purchase'
    TYPE_CASH = 'cash'
    TYPE_BANK = 'bank'
    TYPE_ADJUSTMENT = 'adjustment'
    TYPE_CLOSING = 'closing'
    
    TYPE_CHOICES = [
        (TYPE_GENERAL, _('General')),
        (TYPE_SALES, _('Sales')),
        (TYPE_PURCHASE, _('Purchase')),
        (TYPE_CASH, _('Cash')),
        (TYPE_BANK, _('Bank')),
        (TYPE_ADJUSTMENT, _('Adjustment')),
        (TYPE_CLOSING, _('Closing')),
    ]
    
    journal_number = models.CharField(_('journal number'), max_length=50, unique=True)
    journal_date = models.DateField(_('journal date'))
    
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT, related_name='journals')
    accounting_period = models.ForeignKey(AccountingPeriod, on_delete=models.PROTECT, related_name='journals')
    
    journal_type = models.CharField(_('journal type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_GENERAL)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True)
    reference_id = models.UUIDField(_('reference ID'), null=True, blank=True)
    
    description = models.TextField(_('description'), blank=True)
    
    total_debit = models.DecimalField(_('total debit'), max_digits=15, decimal_places=2, default=0)
    total_credit = models.DecimalField(_('total credit'), max_digits=15, decimal_places=2, default=0)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    posted_by = models.UUIDField(_('posted by'), null=True, blank=True)
    posted_at = models.DateTimeField(_('posted at'), null=True, blank=True)
    reversed_by = models.UUIDField(_('reversed by'), null=True, blank=True)
    reversed_at = models.DateTimeField(_('reversed at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('journal')
        verbose_name_plural = _('journals')
        ordering = ['-journal_date', '-created_at']
        indexes = [
            models.Index(fields=['tenant_id', 'journal_date']),
            models.Index(fields=['tenant_id', 'status']),
            models.Index(fields=['tenant_id', 'journal_type']),
            models.Index(fields=['journal_number']),
        ]
    
    def __str__(self):
        return f"{self.journal_number} - {self.get_journal_type_display()} - {self.journal_date}"


class JournalEntry(TenantAwareModel):
    """
    Model for journal entries.
    """
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='journal_entries')
    
    description = models.CharField(_('description'), max_length=255, blank=True)
    
    debit_amount = models.DecimalField(_('debit amount'), max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(_('credit amount'), max_digits=15, decimal_places=2, default=0)
    
    shop_id = models.UUIDField(_('shop ID'), null=True, blank=True)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True)
    reference_id = models.UUIDField(_('reference ID'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('journal entry')
        verbose_name_plural = _('journal entries')
        ordering = ['id']
    
    def __str__(self):
        if self.debit_amount > 0:
            return f"{self.account.name} - Dr {self.debit_amount}"
        else:
            return f"{self.account.name} - Cr {self.credit_amount}"


class RecurringJournal(TenantAwareModel):
    """
    Model for recurring journals.
    """
    # Status choices
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
    ]
    
    # Frequency choices
    FREQUENCY_DAILY = 'daily'
    FREQUENCY_WEEKLY = 'weekly'
    FREQUENCY_MONTHLY = 'monthly'
    FREQUENCY_QUARTERLY = 'quarterly'
    FREQUENCY_YEARLY = 'yearly'
    
    FREQUENCY_CHOICES = [
        (FREQUENCY_DAILY, _('Daily')),
        (FREQUENCY_WEEKLY, _('Weekly')),
        (FREQUENCY_MONTHLY, _('Monthly')),
        (FREQUENCY_QUARTERLY, _('Quarterly')),
        (FREQUENCY_YEARLY, _('Yearly')),
    ]
    
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    journal_type = models.CharField(_('journal type'), max_length=20, choices=Journal.TYPE_CHOICES, default=Journal.TYPE_GENERAL)
    
    frequency = models.CharField(_('frequency'), max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), null=True, blank=True)
    
    next_run_date = models.DateField(_('next run date'))
    
    total_debit = models.DecimalField(_('total debit'), max_digits=15, decimal_places=2, default=0)
    total_credit = models.DecimalField(_('total credit'), max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    class Meta:
        verbose_name = _('recurring journal')
        verbose_name_plural = _('recurring journals')
        ordering = ['next_run_date', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_frequency_display()}"


class RecurringJournalEntry(TenantAwareModel):
    """
    Model for recurring journal entries.
    """
    recurring_journal = models.ForeignKey(RecurringJournal, on_delete=models.CASCADE, related_name='entries')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='recurring_entries')
    
    description = models.CharField(_('description'), max_length=255, blank=True)
    
    debit_amount = models.DecimalField(_('debit amount'), max_digits=15, decimal_places=2, default=0)
    credit_amount = models.DecimalField(_('credit amount'), max_digits=15, decimal_places=2, default=0)
    
    shop_id = models.UUIDField(_('shop ID'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('recurring journal entry')
        verbose_name_plural = _('recurring journal entries')
        ordering = ['id']
    
    def __str__(self):
        if self.debit_amount > 0:
            return f"{self.account.name} - Dr {self.debit_amount}"
        else:
            return f"{self.account.name} - Cr {self.credit_amount}"
