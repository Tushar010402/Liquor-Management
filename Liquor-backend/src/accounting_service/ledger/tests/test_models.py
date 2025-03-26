import uuid
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from accounts.models import (
    AccountType, Account, FiscalYear, AccountingPeriod
)
from journals.models import Journal, JournalEntry
from ledger.models import (
    GeneralLedger, AccountBalance, TrialBalance, TrialBalanceEntry
)

class LedgerModelsTest(TestCase):
    """
    Test the ledger models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        
        # Create account types
        self.asset_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            created_by=self.user_id
        )
        
        self.liability_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Liabilities",
            code="LIAB",
            type=AccountType.TYPE_LIABILITY,
            created_by=self.user_id
        )
        
        # Create accounts
        self.cash_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="Cash",
            code="1001",
            is_cash_account=True,
            created_by=self.user_id
        )
        
        self.creditor_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.liability_type,
            name="Creditors",
            code="2001",
            created_by=self.user_id
        )
        
        # Create fiscal year and accounting period
        self.fiscal_year = FiscalYear.objects.create(
            tenant_id=self.tenant_id,
            name="FY 2023-2024",
            start_date=date(2023, 4, 1),
            end_date=date(2024, 3, 31),
            status=FiscalYear.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        self.accounting_period = AccountingPeriod.objects.create(
            tenant_id=self.tenant_id,
            fiscal_year=self.fiscal_year,
            name="April 2023",
            start_date=date(2023, 4, 1),
            end_date=date(2023, 4, 30),
            status=AccountingPeriod.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        # Create journal
        self.journal = Journal.objects.create(
            tenant_id=self.tenant_id,
            journal_number="JV-2023-0001",
            journal_date=date(2023, 4, 15),
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            journal_type=Journal.TYPE_GENERAL,
            status=Journal.STATUS_POSTED,
            description="Test journal entry",
            total_debit=1000,
            total_credit=1000,
            created_by=self.user_id,
            posted_by=self.user_id,
            posted_at=timezone.now()
        )
        
        # Create journal entries
        self.debit_entry = JournalEntry.objects.create(
            tenant_id=self.tenant_id,
            journal=self.journal,
            account=self.cash_account,
            description="Cash debit",
            debit_amount=1000,
            credit_amount=0,
            shop_id=self.shop_id
        )
        
        self.credit_entry = JournalEntry.objects.create(
            tenant_id=self.tenant_id,
            journal=self.journal,
            account=self.creditor_account,
            description="Creditor credit",
            debit_amount=0,
            credit_amount=1000,
            shop_id=self.shop_id
        )
        
        # Create general ledger entries
        self.debit_ledger = GeneralLedger.objects.create(
            tenant_id=self.tenant_id,
            account=self.cash_account,
            journal=self.journal,
            journal_entry=self.debit_entry,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            transaction_date=date(2023, 4, 15),
            description="Cash debit",
            debit_amount=1000,
            credit_amount=0,
            balance=1000,
            shop_id=self.shop_id
        )
        
        self.credit_ledger = GeneralLedger.objects.create(
            tenant_id=self.tenant_id,
            account=self.creditor_account,
            journal=self.journal,
            journal_entry=self.credit_entry,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            transaction_date=date(2023, 4, 15),
            description="Creditor credit",
            debit_amount=0,
            credit_amount=1000,
            balance=1000,
            shop_id=self.shop_id
        )
        
        # Create account balances
        self.cash_balance = AccountBalance.objects.create(
            tenant_id=self.tenant_id,
            account=self.cash_account,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            opening_balance=0,
            current_balance=1000,
            total_debits=1000,
            total_credits=0,
            shop_id=self.shop_id
        )
        
        self.creditor_balance = AccountBalance.objects.create(
            tenant_id=self.tenant_id,
            account=self.creditor_account,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            opening_balance=0,
            current_balance=1000,
            total_debits=0,
            total_credits=1000,
            shop_id=self.shop_id
        )
        
        # Create trial balance
        self.trial_balance = TrialBalance.objects.create(
            tenant_id=self.tenant_id,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            as_of_date=date(2023, 4, 30),
            total_debits=1000,
            total_credits=1000,
            status=TrialBalance.STATUS_FINAL,
            created_by=self.user_id,
            finalized_by=self.user_id,
            finalized_at=timezone.now()
        )
        
        # Create trial balance entries
        self.cash_tb_entry = TrialBalanceEntry.objects.create(
            tenant_id=self.tenant_id,
            trial_balance=self.trial_balance,
            account=self.cash_account,
            debit_amount=1000,
            credit_amount=0
        )
        
        self.creditor_tb_entry = TrialBalanceEntry.objects.create(
            tenant_id=self.tenant_id,
            trial_balance=self.trial_balance,
            account=self.creditor_account,
            debit_amount=0,
            credit_amount=1000
        )
    
    def test_general_ledger_creation(self):
        """
        Test GeneralLedger creation.
        """
        # Test debit ledger entry
        self.assertEqual(self.debit_ledger.account, self.cash_account)
        self.assertEqual(self.debit_ledger.journal, self.journal)
        self.assertEqual(self.debit_ledger.journal_entry, self.debit_entry)
        self.assertEqual(self.debit_ledger.fiscal_year, self.fiscal_year)
        self.assertEqual(self.debit_ledger.accounting_period, self.accounting_period)
        self.assertEqual(self.debit_ledger.transaction_date, date(2023, 4, 15))
        self.assertEqual(self.debit_ledger.description, "Cash debit")
        self.assertEqual(self.debit_ledger.debit_amount, 1000)
        self.assertEqual(self.debit_ledger.credit_amount, 0)
        self.assertEqual(self.debit_ledger.balance, 1000)
        self.assertEqual(self.debit_ledger.shop_id, self.shop_id)
        self.assertEqual(self.debit_ledger.tenant_id, self.tenant_id)
        self.assertTrue(self.debit_ledger.is_active)
        
        # Test credit ledger entry
        self.assertEqual(self.credit_ledger.account, self.creditor_account)
        self.assertEqual(self.credit_ledger.journal, self.journal)
        self.assertEqual(self.credit_ledger.journal_entry, self.credit_entry)
        self.assertEqual(self.credit_ledger.fiscal_year, self.fiscal_year)
        self.assertEqual(self.credit_ledger.accounting_period, self.accounting_period)
        self.assertEqual(self.credit_ledger.transaction_date, date(2023, 4, 15))
        self.assertEqual(self.credit_ledger.description, "Creditor credit")
        self.assertEqual(self.credit_ledger.debit_amount, 0)
        self.assertEqual(self.credit_ledger.credit_amount, 1000)
        self.assertEqual(self.credit_ledger.balance, 1000)
        self.assertEqual(self.credit_ledger.shop_id, self.shop_id)
        self.assertEqual(self.credit_ledger.tenant_id, self.tenant_id)
        self.assertTrue(self.credit_ledger.is_active)
    
    def test_general_ledger_str(self):
        """
        Test GeneralLedger string representation.
        """
        self.assertEqual(
            str(self.debit_ledger), 
            f"Cash - {date(2023, 4, 15)} - 1000"
        )
        self.assertEqual(
            str(self.credit_ledger), 
            f"Creditors - {date(2023, 4, 15)} - 1000"
        )
    
    def test_account_balance_creation(self):
        """
        Test AccountBalance creation.
        """
        # Test cash account balance
        self.assertEqual(self.cash_balance.account, self.cash_account)
        self.assertEqual(self.cash_balance.fiscal_year, self.fiscal_year)
        self.assertEqual(self.cash_balance.accounting_period, self.accounting_period)
        self.assertEqual(self.cash_balance.opening_balance, 0)
        self.assertEqual(self.cash_balance.current_balance, 1000)
        self.assertEqual(self.cash_balance.total_debits, 1000)
        self.assertEqual(self.cash_balance.total_credits, 0)
        self.assertEqual(self.cash_balance.shop_id, self.shop_id)
        self.assertEqual(self.cash_balance.tenant_id, self.tenant_id)
        self.assertTrue(self.cash_balance.is_active)
        
        # Test creditor account balance
        self.assertEqual(self.creditor_balance.account, self.creditor_account)
        self.assertEqual(self.creditor_balance.fiscal_year, self.fiscal_year)
        self.assertEqual(self.creditor_balance.accounting_period, self.accounting_period)
        self.assertEqual(self.creditor_balance.opening_balance, 0)
        self.assertEqual(self.creditor_balance.current_balance, 1000)
        self.assertEqual(self.creditor_balance.total_debits, 0)
        self.assertEqual(self.creditor_balance.total_credits, 1000)
        self.assertEqual(self.creditor_balance.shop_id, self.shop_id)
        self.assertEqual(self.creditor_balance.tenant_id, self.tenant_id)
        self.assertTrue(self.creditor_balance.is_active)
    
    def test_account_balance_str(self):
        """
        Test AccountBalance string representation.
        """
        self.assertEqual(
            str(self.cash_balance), 
            f"Cash - April 2023 - 1000"
        )
        self.assertEqual(
            str(self.creditor_balance), 
            f"Creditors - April 2023 - 1000"
        )
    
    def test_trial_balance_creation(self):
        """
        Test TrialBalance creation.
        """
        self.assertEqual(self.trial_balance.fiscal_year, self.fiscal_year)
        self.assertEqual(self.trial_balance.accounting_period, self.accounting_period)
        self.assertEqual(self.trial_balance.as_of_date, date(2023, 4, 30))
        self.assertEqual(self.trial_balance.total_debits, 1000)
        self.assertEqual(self.trial_balance.total_credits, 1000)
        self.assertEqual(self.trial_balance.status, TrialBalance.STATUS_FINAL)
        self.assertEqual(self.trial_balance.tenant_id, self.tenant_id)
        self.assertEqual(self.trial_balance.created_by, self.user_id)
        self.assertEqual(self.trial_balance.finalized_by, self.user_id)
        self.assertIsNotNone(self.trial_balance.finalized_at)
        self.assertTrue(self.trial_balance.is_active)
    
    def test_trial_balance_str(self):
        """
        Test TrialBalance string representation.
        """
        self.assertEqual(
            str(self.trial_balance), 
            f"Trial Balance - April 2023 - {date(2023, 4, 30)}"
        )
    
    def test_trial_balance_entries(self):
        """
        Test TrialBalance entries.
        """
        entries = self.trial_balance.entries.all()
        self.assertEqual(entries.count(), 2)
        
        # Check cash entry
        cash_entry = entries.filter(account=self.cash_account).first()
        self.assertEqual(cash_entry, self.cash_tb_entry)
        self.assertEqual(cash_entry.debit_amount, 1000)
        self.assertEqual(cash_entry.credit_amount, 0)
        self.assertEqual(cash_entry.tenant_id, self.tenant_id)
        
        # Check creditor entry
        creditor_entry = entries.filter(account=self.creditor_account).first()
        self.assertEqual(creditor_entry, self.creditor_tb_entry)
        self.assertEqual(creditor_entry.debit_amount, 0)
        self.assertEqual(creditor_entry.credit_amount, 1000)
        self.assertEqual(creditor_entry.tenant_id, self.tenant_id)
    
    def test_trial_balance_entry_str(self):
        """
        Test TrialBalanceEntry string representation.
        """
        self.assertEqual(
            str(self.cash_tb_entry), 
            "Cash - Dr: 1000, Cr: 0"
        )
        self.assertEqual(
            str(self.creditor_tb_entry), 
            "Creditors - Dr: 0, Cr: 1000"
        )