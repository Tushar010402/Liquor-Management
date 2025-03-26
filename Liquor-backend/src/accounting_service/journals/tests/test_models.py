import uuid
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from accounts.models import (
    AccountType, Account, FiscalYear, AccountingPeriod
)
from journals.models import (
    Journal, JournalEntry, RecurringJournal, RecurringJournalEntry
)

class JournalModelTest(TestCase):
    """
    Test the Journal model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        
        # Create account type
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
        
        self.bank_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="Bank",
            code="1002",
            is_bank_account=True,
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
            status=Journal.STATUS_DRAFT,
            description="Test journal entry",
            total_debit=1000,
            total_credit=1000,
            created_by=self.user_id
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
    
    def test_journal_creation(self):
        """
        Test Journal creation.
        """
        self.assertEqual(self.journal.journal_number, "JV-2023-0001")
        self.assertEqual(self.journal.journal_date, date(2023, 4, 15))
        self.assertEqual(self.journal.fiscal_year, self.fiscal_year)
        self.assertEqual(self.journal.accounting_period, self.accounting_period)
        self.assertEqual(self.journal.journal_type, Journal.TYPE_GENERAL)
        self.assertEqual(self.journal.status, Journal.STATUS_DRAFT)
        self.assertEqual(self.journal.description, "Test journal entry")
        self.assertEqual(self.journal.total_debit, 1000)
        self.assertEqual(self.journal.total_credit, 1000)
        self.assertEqual(self.journal.tenant_id, self.tenant_id)
        self.assertEqual(self.journal.created_by, self.user_id)
        self.assertIsNone(self.journal.posted_by)
        self.assertIsNone(self.journal.posted_at)
        self.assertIsNone(self.journal.reversed_by)
        self.assertIsNone(self.journal.reversed_at)
        self.assertTrue(self.journal.is_active)
    
    def test_journal_str(self):
        """
        Test Journal string representation.
        """
        self.assertEqual(
            str(self.journal), 
            f"JV-2023-0001 - General - {date(2023, 4, 15)}"
        )
    
    def test_journal_entries(self):
        """
        Test Journal entries.
        """
        entries = self.journal.entries.all()
        self.assertEqual(entries.count(), 2)
        
        # Check debit entry
        debit_entry = entries.filter(debit_amount__gt=0).first()
        self.assertEqual(debit_entry, self.debit_entry)
        self.assertEqual(debit_entry.account, self.cash_account)
        self.assertEqual(debit_entry.description, "Cash debit")
        self.assertEqual(debit_entry.debit_amount, 1000)
        self.assertEqual(debit_entry.credit_amount, 0)
        self.assertEqual(debit_entry.shop_id, self.shop_id)
        self.assertEqual(debit_entry.tenant_id, self.tenant_id)
        
        # Check credit entry
        credit_entry = entries.filter(credit_amount__gt=0).first()
        self.assertEqual(credit_entry, self.credit_entry)
        self.assertEqual(credit_entry.account, self.creditor_account)
        self.assertEqual(credit_entry.description, "Creditor credit")
        self.assertEqual(credit_entry.debit_amount, 0)
        self.assertEqual(credit_entry.credit_amount, 1000)
        self.assertEqual(credit_entry.shop_id, self.shop_id)
        self.assertEqual(credit_entry.tenant_id, self.tenant_id)
    
    def test_journal_entry_str(self):
        """
        Test JournalEntry string representation.
        """
        self.assertEqual(str(self.debit_entry), "Cash - Dr 1000")
        self.assertEqual(str(self.credit_entry), "Creditors - Cr 1000")


class RecurringJournalModelTest(TestCase):
    """
    Test the RecurringJournal model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        
        # Create account type
        self.asset_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            created_by=self.user_id
        )
        
        self.expense_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Expenses",
            code="EXP",
            type=AccountType.TYPE_EXPENSE,
            created_by=self.user_id
        )
        
        # Create accounts
        self.bank_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="Bank",
            code="1002",
            is_bank_account=True,
            created_by=self.user_id
        )
        
        self.rent_expense_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.expense_type,
            name="Rent Expense",
            code="5001",
            created_by=self.user_id
        )
        
        # Create recurring journal
        self.recurring_journal = RecurringJournal.objects.create(
            tenant_id=self.tenant_id,
            name="Monthly Rent",
            description="Monthly rent payment",
            journal_type=Journal.TYPE_GENERAL,
            frequency=RecurringJournal.FREQUENCY_MONTHLY,
            start_date=date(2023, 4, 1),
            end_date=date(2024, 3, 31),
            next_run_date=date(2023, 5, 1),
            total_debit=5000,
            total_credit=5000,
            status=RecurringJournal.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        # Create recurring journal entries
        self.debit_entry = RecurringJournalEntry.objects.create(
            tenant_id=self.tenant_id,
            recurring_journal=self.recurring_journal,
            account=self.rent_expense_account,
            description="Rent expense",
            debit_amount=5000,
            credit_amount=0,
            shop_id=self.shop_id
        )
        
        self.credit_entry = RecurringJournalEntry.objects.create(
            tenant_id=self.tenant_id,
            recurring_journal=self.recurring_journal,
            account=self.bank_account,
            description="Bank payment",
            debit_amount=0,
            credit_amount=5000,
            shop_id=self.shop_id
        )
    
    def test_recurring_journal_creation(self):
        """
        Test RecurringJournal creation.
        """
        self.assertEqual(self.recurring_journal.name, "Monthly Rent")
        self.assertEqual(self.recurring_journal.description, "Monthly rent payment")
        self.assertEqual(self.recurring_journal.journal_type, Journal.TYPE_GENERAL)
        self.assertEqual(self.recurring_journal.frequency, RecurringJournal.FREQUENCY_MONTHLY)
        self.assertEqual(self.recurring_journal.start_date, date(2023, 4, 1))
        self.assertEqual(self.recurring_journal.end_date, date(2024, 3, 31))
        self.assertEqual(self.recurring_journal.next_run_date, date(2023, 5, 1))
        self.assertEqual(self.recurring_journal.total_debit, 5000)
        self.assertEqual(self.recurring_journal.total_credit, 5000)
        self.assertEqual(self.recurring_journal.status, RecurringJournal.STATUS_ACTIVE)
        self.assertEqual(self.recurring_journal.tenant_id, self.tenant_id)
        self.assertEqual(self.recurring_journal.created_by, self.user_id)
        self.assertTrue(self.recurring_journal.is_active)
    
    def test_recurring_journal_str(self):
        """
        Test RecurringJournal string representation.
        """
        self.assertEqual(
            str(self.recurring_journal), 
            "Monthly Rent - Monthly"
        )
    
    def test_recurring_journal_entries(self):
        """
        Test RecurringJournal entries.
        """
        entries = self.recurring_journal.entries.all()
        self.assertEqual(entries.count(), 2)
        
        # Check debit entry
        debit_entry = entries.filter(debit_amount__gt=0).first()
        self.assertEqual(debit_entry, self.debit_entry)
        self.assertEqual(debit_entry.account, self.rent_expense_account)
        self.assertEqual(debit_entry.description, "Rent expense")
        self.assertEqual(debit_entry.debit_amount, 5000)
        self.assertEqual(debit_entry.credit_amount, 0)
        self.assertEqual(debit_entry.shop_id, self.shop_id)
        self.assertEqual(debit_entry.tenant_id, self.tenant_id)
        
        # Check credit entry
        credit_entry = entries.filter(credit_amount__gt=0).first()
        self.assertEqual(credit_entry, self.credit_entry)
        self.assertEqual(credit_entry.account, self.bank_account)
        self.assertEqual(credit_entry.description, "Bank payment")
        self.assertEqual(credit_entry.debit_amount, 0)
        self.assertEqual(credit_entry.credit_amount, 5000)
        self.assertEqual(credit_entry.shop_id, self.shop_id)
        self.assertEqual(credit_entry.tenant_id, self.tenant_id)
    
    def test_recurring_journal_entry_str(self):
        """
        Test RecurringJournalEntry string representation.
        """
        self.assertEqual(str(self.debit_entry), "Rent Expense - Dr 5000")
        self.assertEqual(str(self.credit_entry), "Bank - Cr 5000")