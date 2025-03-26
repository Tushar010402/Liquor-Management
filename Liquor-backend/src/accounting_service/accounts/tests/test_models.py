import uuid
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from accounts.models import (
    AccountType, Account, FiscalYear, 
    AccountingPeriod, BankAccount
)

class AccountTypeModelTest(TestCase):
    """
    Test the AccountType model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.account_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            description="Asset accounts",
            created_by=self.user_id
        )
    
    def test_account_type_creation(self):
        """
        Test AccountType creation.
        """
        self.assertEqual(self.account_type.name, "Assets")
        self.assertEqual(self.account_type.code, "ASSET")
        self.assertEqual(self.account_type.type, AccountType.TYPE_ASSET)
        self.assertEqual(self.account_type.description, "Asset accounts")
        self.assertEqual(self.account_type.tenant_id, self.tenant_id)
        self.assertEqual(self.account_type.created_by, self.user_id)
        self.assertTrue(self.account_type.is_active)
    
    def test_account_type_str(self):
        """
        Test AccountType string representation.
        """
        self.assertEqual(str(self.account_type), "ASSET - Assets")


class AccountModelTest(TestCase):
    """
    Test the Account model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.account_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            description="Asset accounts",
            created_by=self.user_id
        )
        
        self.parent_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.account_type,
            name="Current Assets",
            code="1000",
            description="Current assets",
            opening_balance=0,
            current_balance=0,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        self.account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.account_type,
            name="Cash",
            code="1001",
            description="Cash on hand",
            parent=self.parent_account,
            is_cash_account=True,
            opening_balance=1000,
            current_balance=1500,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
    
    def test_account_creation(self):
        """
        Test Account creation.
        """
        self.assertEqual(self.account.name, "Cash")
        self.assertEqual(self.account.code, "1001")
        self.assertEqual(self.account.description, "Cash on hand")
        self.assertEqual(self.account.parent, self.parent_account)
        self.assertEqual(self.account.account_type, self.account_type)
        self.assertTrue(self.account.is_cash_account)
        self.assertFalse(self.account.is_bank_account)
        self.assertFalse(self.account.is_control_account)
        self.assertEqual(self.account.opening_balance, 1000)
        self.assertEqual(self.account.current_balance, 1500)
        self.assertEqual(self.account.status, Account.STATUS_ACTIVE)
        self.assertEqual(self.account.tenant_id, self.tenant_id)
        self.assertEqual(self.account.created_by, self.user_id)
        self.assertTrue(self.account.is_active)
    
    def test_account_str(self):
        """
        Test Account string representation.
        """
        self.assertEqual(str(self.account), "1001 - Cash")


class FiscalYearModelTest(TestCase):
    """
    Test the FiscalYear model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.fiscal_year = FiscalYear.objects.create(
            tenant_id=self.tenant_id,
            name="FY 2023-2024",
            start_date=date(2023, 4, 1),
            end_date=date(2024, 3, 31),
            status=FiscalYear.STATUS_ACTIVE,
            notes="Financial year 2023-2024",
            created_by=self.user_id
        )
    
    def test_fiscal_year_creation(self):
        """
        Test FiscalYear creation.
        """
        self.assertEqual(self.fiscal_year.name, "FY 2023-2024")
        self.assertEqual(self.fiscal_year.start_date, date(2023, 4, 1))
        self.assertEqual(self.fiscal_year.end_date, date(2024, 3, 31))
        self.assertEqual(self.fiscal_year.status, FiscalYear.STATUS_ACTIVE)
        self.assertEqual(self.fiscal_year.notes, "Financial year 2023-2024")
        self.assertEqual(self.fiscal_year.tenant_id, self.tenant_id)
        self.assertEqual(self.fiscal_year.created_by, self.user_id)
        self.assertIsNone(self.fiscal_year.closed_by)
        self.assertIsNone(self.fiscal_year.closed_at)
        self.assertTrue(self.fiscal_year.is_active)
    
    def test_fiscal_year_str(self):
        """
        Test FiscalYear string representation.
        """
        self.assertEqual(
            str(self.fiscal_year), 
            f"FY 2023-2024 ({date(2023, 4, 1)} to {date(2024, 3, 31)})"
        )


class AccountingPeriodModelTest(TestCase):
    """
    Test the AccountingPeriod model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
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
            notes="April 2023 accounting period",
            created_by=self.user_id
        )
    
    def test_accounting_period_creation(self):
        """
        Test AccountingPeriod creation.
        """
        self.assertEqual(self.accounting_period.name, "April 2023")
        self.assertEqual(self.accounting_period.start_date, date(2023, 4, 1))
        self.assertEqual(self.accounting_period.end_date, date(2023, 4, 30))
        self.assertEqual(self.accounting_period.status, AccountingPeriod.STATUS_ACTIVE)
        self.assertEqual(self.accounting_period.notes, "April 2023 accounting period")
        self.assertEqual(self.accounting_period.fiscal_year, self.fiscal_year)
        self.assertEqual(self.accounting_period.tenant_id, self.tenant_id)
        self.assertEqual(self.accounting_period.created_by, self.user_id)
        self.assertIsNone(self.accounting_period.closed_by)
        self.assertIsNone(self.accounting_period.closed_at)
        self.assertTrue(self.accounting_period.is_active)
    
    def test_accounting_period_str(self):
        """
        Test AccountingPeriod string representation.
        """
        self.assertEqual(
            str(self.accounting_period), 
            f"April 2023 ({date(2023, 4, 1)} to {date(2023, 4, 30)})"
        )


class BankAccountModelTest(TestCase):
    """
    Test the BankAccount model.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.account_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            description="Asset accounts",
            created_by=self.user_id
        )
        
        self.account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.account_type,
            name="Bank Account",
            code="1002",
            description="Bank account",
            is_bank_account=True,
            opening_balance=5000,
            current_balance=7500,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        self.bank_account = BankAccount.objects.create(
            tenant_id=self.tenant_id,
            account=self.account,
            bank_name="Test Bank",
            account_number="1234567890",
            account_name="Test Company",
            branch="Main Branch",
            ifsc_code="TEST1234",
            opening_balance=5000,
            current_balance=7500,
            status=BankAccount.STATUS_ACTIVE,
            notes="Test bank account",
            created_by=self.user_id
        )
    
    def test_bank_account_creation(self):
        """
        Test BankAccount creation.
        """
        self.assertEqual(self.bank_account.bank_name, "Test Bank")
        self.assertEqual(self.bank_account.account_number, "1234567890")
        self.assertEqual(self.bank_account.account_name, "Test Company")
        self.assertEqual(self.bank_account.branch, "Main Branch")
        self.assertEqual(self.bank_account.ifsc_code, "TEST1234")
        self.assertEqual(self.bank_account.opening_balance, 5000)
        self.assertEqual(self.bank_account.current_balance, 7500)
        self.assertEqual(self.bank_account.status, BankAccount.STATUS_ACTIVE)
        self.assertEqual(self.bank_account.notes, "Test bank account")
        self.assertEqual(self.bank_account.account, self.account)
        self.assertEqual(self.bank_account.tenant_id, self.tenant_id)
        self.assertEqual(self.bank_account.created_by, self.user_id)
        self.assertTrue(self.bank_account.is_active)
    
    def test_bank_account_str(self):
        """
        Test BankAccount string representation.
        """
        self.assertEqual(str(self.bank_account), "Test Bank - 1234567890")