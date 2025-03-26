import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import ShopAwareModel


class CashTransaction(ShopAwareModel):
    """
    Model for cash transactions.
    """
    # Transaction type choices
    TYPE_SALE = 'sale'
    TYPE_RETURN = 'return'
    TYPE_DEPOSIT = 'deposit'
    TYPE_EXPENSE = 'expense'
    TYPE_ADJUSTMENT = 'adjustment'
    TYPE_OPENING_BALANCE = 'opening_balance'
    TYPE_CLOSING_BALANCE = 'closing_balance'
    
    TYPE_CHOICES = [
        (TYPE_SALE, _('Sale')),
        (TYPE_RETURN, _('Return')),
        (TYPE_DEPOSIT, _('Deposit')),
        (TYPE_EXPENSE, _('Expense')),
        (TYPE_ADJUSTMENT, _('Adjustment')),
        (TYPE_OPENING_BALANCE, _('Opening Balance')),
        (TYPE_CLOSING_BALANCE, _('Closing Balance')),
    ]
    
    # Transaction status choices
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_VERIFIED = 'verified'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_VERIFIED, _('Verified')),
    ]
    
    transaction_number = models.CharField(_('transaction number'), max_length=50, unique=True)
    transaction_date = models.DateTimeField(_('transaction date'))
    transaction_type = models.CharField(_('transaction type'), max_length=20, choices=TYPE_CHOICES)
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    running_balance = models.DecimalField(_('running balance'), max_digits=10, decimal_places=2)
    
    reference_id = models.UUIDField(_('reference ID'), null=True, blank=True)
    reference_type = models.CharField(_('reference type'), max_length=50, blank=True)
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    verified_by = models.UUIDField(_('verified by'), null=True, blank=True)
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    
    # Metadata
    is_synced = models.BooleanField(_('is synced'), default=True)
    sync_id = models.CharField(_('sync ID'), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _('cash transaction')
        verbose_name_plural = _('cash transactions')
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['tenant_id', 'shop_id', 'transaction_date']),
            models.Index(fields=['tenant_id', 'shop_id', 'transaction_type']),
            models.Index(fields=['tenant_id', 'shop_id', 'status']),
            models.Index(fields=['transaction_number']),
        ]
    
    def __str__(self):
        return f"{self.transaction_number} - {self.transaction_type} - {self.amount}"


class BankDeposit(ShopAwareModel):
    """
    Model for bank deposits.
    """
    # Deposit status choices
    STATUS_PENDING = 'pending'
    STATUS_VERIFIED = 'verified'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_VERIFIED, _('Verified')),
        (STATUS_REJECTED, _('Rejected')),
    ]
    
    # Deposit method choices
    METHOD_CASH = 'cash'
    METHOD_CHEQUE = 'cheque'
    METHOD_TRANSFER = 'transfer'
    
    METHOD_CHOICES = [
        (METHOD_CASH, _('Cash')),
        (METHOD_CHEQUE, _('Cheque')),
        (METHOD_TRANSFER, _('Transfer')),
    ]
    
    deposit_number = models.CharField(_('deposit number'), max_length=50, unique=True)
    deposit_date = models.DateTimeField(_('deposit date'))
    
    bank_name = models.CharField(_('bank name'), max_length=100)
    account_number = models.CharField(_('account number'), max_length=50)
    branch = models.CharField(_('branch'), max_length=100, blank=True)
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    deposit_method = models.CharField(_('deposit method'), max_length=20, choices=METHOD_CHOICES, default=METHOD_CASH)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    cheque_number = models.CharField(_('cheque number'), max_length=50, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # Receipt image
    receipt_image = models.ImageField(_('receipt image'), upload_to='deposit_receipts/', null=True, blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    verified_by = models.UUIDField(_('verified by'), null=True, blank=True)
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    # Cash transaction reference
    cash_transaction = models.OneToOneField(CashTransaction, on_delete=models.SET_NULL, related_name='bank_deposit', null=True, blank=True)
    
    class Meta:
        verbose_name = _('bank deposit')
        verbose_name_plural = _('bank deposits')
        ordering = ['-deposit_date']
    
    def __str__(self):
        return f"{self.deposit_number} - {self.bank_name} - {self.amount}"


class UPITransaction(ShopAwareModel):
    """
    Model for UPI transactions.
    """
    # Transaction status choices
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_FAILED, _('Failed')),
    ]
    
    transaction_number = models.CharField(_('transaction number'), max_length=50, unique=True)
    transaction_date = models.DateTimeField(_('transaction date'))
    
    upi_id = models.CharField(_('UPI ID'), max_length=100)
    payee_name = models.CharField(_('payee name'), max_length=100, blank=True)
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    reference_number = models.CharField(_('reference number'), max_length=100)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # Receipt image
    receipt_image = models.ImageField(_('receipt image'), upload_to='upi_receipts/', null=True, blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    
    # Cash transaction reference
    cash_transaction = models.OneToOneField(CashTransaction, on_delete=models.SET_NULL, related_name='upi_transaction', null=True, blank=True)
    
    class Meta:
        verbose_name = _('UPI transaction')
        verbose_name_plural = _('UPI transactions')
        ordering = ['-transaction_date']
    
    def __str__(self):
        return f"{self.transaction_number} - {self.upi_id} - {self.amount}"


class Expense(ShopAwareModel):
    """
    Model for expenses.
    """
    # Expense status choices
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
    ]
    
    # Expense category choices
    CATEGORY_UTILITIES = 'utilities'
    CATEGORY_RENT = 'rent'
    CATEGORY_SALARIES = 'salaries'
    CATEGORY_MAINTENANCE = 'maintenance'
    CATEGORY_SUPPLIES = 'supplies'
    CATEGORY_TRANSPORTATION = 'transportation'
    CATEGORY_MARKETING = 'marketing'
    CATEGORY_MISCELLANEOUS = 'miscellaneous'
    
    CATEGORY_CHOICES = [
        (CATEGORY_UTILITIES, _('Utilities')),
        (CATEGORY_RENT, _('Rent')),
        (CATEGORY_SALARIES, _('Salaries')),
        (CATEGORY_MAINTENANCE, _('Maintenance')),
        (CATEGORY_SUPPLIES, _('Supplies')),
        (CATEGORY_TRANSPORTATION, _('Transportation')),
        (CATEGORY_MARKETING, _('Marketing')),
        (CATEGORY_MISCELLANEOUS, _('Miscellaneous')),
    ]
    
    # Payment method choices
    METHOD_CASH = 'cash'
    METHOD_UPI = 'upi'
    METHOD_BANK_TRANSFER = 'bank_transfer'
    METHOD_CHEQUE = 'cheque'
    
    METHOD_CHOICES = [
        (METHOD_CASH, _('Cash')),
        (METHOD_UPI, _('UPI')),
        (METHOD_BANK_TRANSFER, _('Bank Transfer')),
        (METHOD_CHEQUE, _('Cheque')),
    ]
    
    expense_number = models.CharField(_('expense number'), max_length=50, unique=True)
    expense_date = models.DateTimeField(_('expense date'))
    
    category = models.CharField(_('category'), max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(_('description'))
    
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_('payment method'), max_length=20, choices=METHOD_CHOICES, default=METHOD_CASH)
    
    reference_number = models.CharField(_('reference number'), max_length=50, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_APPROVED)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # Receipt image
    receipt_image = models.ImageField(_('receipt image'), upload_to='expense_receipts/', null=True, blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    approved_by = models.UUIDField(_('approved by'), null=True, blank=True)
    approved_at = models.DateTimeField(_('approved at'), null=True, blank=True)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    # Cash transaction reference
    cash_transaction = models.OneToOneField(CashTransaction, on_delete=models.SET_NULL, related_name='expense', null=True, blank=True)
    
    class Meta:
        verbose_name = _('expense')
        verbose_name_plural = _('expenses')
        ordering = ['-expense_date']
    
    def __str__(self):
        return f"{self.expense_number} - {self.category} - {self.amount}"


class DailySummary(ShopAwareModel):
    """
    Model for daily cash summaries.
    """
    # Status choices
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_VERIFIED = 'verified'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_SUBMITTED, _('Submitted')),
        (STATUS_VERIFIED, _('Verified')),
    ]
    
    summary_date = models.DateField(_('summary date'))
    
    opening_balance = models.DecimalField(_('opening balance'), max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(_('closing balance'), max_digits=10, decimal_places=2)
    
    total_sales = models.DecimalField(_('total sales'), max_digits=10, decimal_places=2, default=0)
    total_returns = models.DecimalField(_('total returns'), max_digits=10, decimal_places=2, default=0)
    total_expenses = models.DecimalField(_('total expenses'), max_digits=10, decimal_places=2, default=0)
    total_deposits = models.DecimalField(_('total deposits'), max_digits=10, decimal_places=2, default=0)
    
    cash_sales = models.DecimalField(_('cash sales'), max_digits=10, decimal_places=2, default=0)
    upi_sales = models.DecimalField(_('UPI sales'), max_digits=10, decimal_places=2, default=0)
    card_sales = models.DecimalField(_('card sales'), max_digits=10, decimal_places=2, default=0)
    credit_sales = models.DecimalField(_('credit sales'), max_digits=10, decimal_places=2, default=0)
    
    expected_balance = models.DecimalField(_('expected balance'), max_digits=10, decimal_places=2)
    balance_difference = models.DecimalField(_('balance difference'), max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    
    notes = models.TextField(_('notes'), blank=True)
    
    # User information
    created_by = models.UUIDField(_('created by'))
    verified_by = models.UUIDField(_('verified by'), null=True, blank=True)
    verified_at = models.DateTimeField(_('verified at'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('daily summary')
        verbose_name_plural = _('daily summaries')
        ordering = ['-summary_date']
        unique_together = ('tenant_id', 'shop_id', 'summary_date')
    
    def __str__(self):
        return f"Summary for {self.summary_date} - {self.shop_id}"