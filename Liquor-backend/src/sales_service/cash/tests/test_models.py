import uuid
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from cash.models import (
    CashRegister, CashTransaction, BankDeposit,
    Expense, ExpenseCategory, DailySummary
)

class CashModelsTest(TestCase):
    """
    Test the cash models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.sale_id = uuid.uuid4()
        
        # Create cash register
        self.cash_register = CashRegister.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            name="Main Register",
            code="REG001",
            opening_balance=Decimal('5000.00'),
            current_balance=Decimal('8500.00'),
            status=CashRegister.STATUS_OPEN,
            opened_by=self.user_id,
            opened_at=timezone.now() - timedelta(hours=8),
            created_by=self.user_id
        )
        
        # Create cash transaction (sale)
        self.cash_transaction_sale = CashTransaction.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            cash_register=self.cash_register,
            transaction_number="TRX-2023-0001",
            transaction_date=date(2023, 4, 15),
            transaction_type=CashTransaction.TRANSACTION_TYPE_SALE,
            reference_type=CashTransaction.REFERENCE_TYPE_SALE,
            reference_id=self.sale_id,
            amount=Decimal('4000.00'),
            notes="Sale transaction",
            created_by=self.user_id
        )
        
        # Create cash transaction (expense)
        self.expense_category = ExpenseCategory.objects.create(
            tenant_id=self.tenant_id,
            name="Utilities",
            code="UTIL",
            description="Utility expenses",
            created_by=self.user_id
        )
        
        self.expense = Expense.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            expense_number="EXP-2023-0001",
            expense_date=date(2023, 4, 15),
            category=self.expense_category,
            amount=Decimal('500.00'),
            payment_method=Expense.PAYMENT_METHOD_CASH,
            status=Expense.STATUS_APPROVED,
            description="Electricity bill",
            notes="Monthly electricity bill",
            created_by=self.user_id,
            approved_by=self.user_id,
            approved_at=timezone.now()
        )
        
        self.cash_transaction_expense = CashTransaction.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            cash_register=self.cash_register,
            transaction_number="TRX-2023-0002",
            transaction_date=date(2023, 4, 15),
            transaction_type=CashTransaction.TRANSACTION_TYPE_EXPENSE,
            reference_type=CashTransaction.REFERENCE_TYPE_EXPENSE,
            reference_id=self.expense.id,
            amount=Decimal('-500.00'),
            notes="Expense transaction",
            created_by=self.user_id
        )
        
        # Create bank deposit
        self.bank_deposit = BankDeposit.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            deposit_number="DEP-2023-0001",
            deposit_date=date(2023, 4, 15),
            bank_name="HDFC Bank",
            account_number="12345678901234",
            amount=Decimal('3000.00'),
            status=BankDeposit.STATUS_PENDING,
            notes="Daily deposit",
            created_by=self.user_id
        )
        
        # Create cash transaction (deposit)
        self.cash_transaction_deposit = CashTransaction.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            cash_register=self.cash_register,
            transaction_number="TRX-2023-0003",
            transaction_date=date(2023, 4, 15),
            transaction_type=CashTransaction.TRANSACTION_TYPE_DEPOSIT,
            reference_type=CashTransaction.REFERENCE_TYPE_BANK_DEPOSIT,
            reference_id=self.bank_deposit.id,
            amount=Decimal('-3000.00'),
            notes="Bank deposit",
            created_by=self.user_id
        )
        
        # Create daily summary
        self.daily_summary = DailySummary.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            summary_date=date(2023, 4, 15),
            opening_balance=Decimal('5000.00'),
            closing_balance=Decimal('5500.00'),
            total_sales=Decimal('4000.00'),
            total_returns=Decimal('0.00'),
            total_expenses=Decimal('500.00'),
            total_deposits=Decimal('3000.00'),
            cash_difference=Decimal('0.00'),
            notes="Daily summary",
            created_by=self.user_id
        )
    
    def test_cash_register_creation(self):
        """
        Test CashRegister creation.
        """
        self.assertEqual(self.cash_register.shop_id, self.shop_id)
        self.assertEqual(self.cash_register.name, "Main Register")
        self.assertEqual(self.cash_register.code, "REG001")
        self.assertEqual(self.cash_register.opening_balance, Decimal('5000.00'))
        self.assertEqual(self.cash_register.current_balance, Decimal('8500.00'))
        self.assertEqual(self.cash_register.status, CashRegister.STATUS_OPEN)
        self.assertEqual(self.cash_register.opened_by, self.user_id)
        self.assertIsNotNone(self.cash_register.opened_at)
        self.assertIsNone(self.cash_register.closed_by)
        self.assertIsNone(self.cash_register.closed_at)
        self.assertEqual(self.cash_register.tenant_id, self.tenant_id)
        self.assertEqual(self.cash_register.created_by, self.user_id)
        self.assertTrue(self.cash_register.is_active)
    
    def test_cash_register_str(self):
        """
        Test CashRegister string representation.
        """
        self.assertEqual(str(self.cash_register), "REG001 - Main Register")
    
    def test_cash_transaction_sale_creation(self):
        """
        Test CashTransaction (sale) creation.
        """
        self.assertEqual(self.cash_transaction_sale.shop_id, self.shop_id)
        self.assertEqual(self.cash_transaction_sale.cash_register, self.cash_register)
        self.assertEqual(self.cash_transaction_sale.transaction_number, "TRX-2023-0001")
        self.assertEqual(self.cash_transaction_sale.transaction_date, date(2023, 4, 15))
        self.assertEqual(self.cash_transaction_sale.transaction_type, CashTransaction.TRANSACTION_TYPE_SALE)
        self.assertEqual(self.cash_transaction_sale.reference_type, CashTransaction.REFERENCE_TYPE_SALE)
        self.assertEqual(self.cash_transaction_sale.reference_id, self.sale_id)
        self.assertEqual(self.cash_transaction_sale.amount, Decimal('4000.00'))
        self.assertEqual(self.cash_transaction_sale.notes, "Sale transaction")
        self.assertEqual(self.cash_transaction_sale.tenant_id, self.tenant_id)
        self.assertEqual(self.cash_transaction_sale.created_by, self.user_id)
    
    def test_cash_transaction_expense_creation(self):
        """
        Test CashTransaction (expense) creation.
        """
        self.assertEqual(self.cash_transaction_expense.shop_id, self.shop_id)
        self.assertEqual(self.cash_transaction_expense.cash_register, self.cash_register)
        self.assertEqual(self.cash_transaction_expense.transaction_number, "TRX-2023-0002")
        self.assertEqual(self.cash_transaction_expense.transaction_date, date(2023, 4, 15))
        self.assertEqual(self.cash_transaction_expense.transaction_type, CashTransaction.TRANSACTION_TYPE_EXPENSE)
        self.assertEqual(self.cash_transaction_expense.reference_type, CashTransaction.REFERENCE_TYPE_EXPENSE)
        self.assertEqual(self.cash_transaction_expense.reference_id, self.expense.id)
        self.assertEqual(self.cash_transaction_expense.amount, Decimal('-500.00'))
        self.assertEqual(self.cash_transaction_expense.notes, "Expense transaction")
        self.assertEqual(self.cash_transaction_expense.tenant_id, self.tenant_id)
        self.assertEqual(self.cash_transaction_expense.created_by, self.user_id)
    
    def test_cash_transaction_deposit_creation(self):
        """
        Test CashTransaction (deposit) creation.
        """
        self.assertEqual(self.cash_transaction_deposit.shop_id, self.shop_id)
        self.assertEqual(self.cash_transaction_deposit.cash_register, self.cash_register)
        self.assertEqual(self.cash_transaction_deposit.transaction_number, "TRX-2023-0003")
        self.assertEqual(self.cash_transaction_deposit.transaction_date, date(2023, 4, 15))
        self.assertEqual(self.cash_transaction_deposit.transaction_type, CashTransaction.TRANSACTION_TYPE_DEPOSIT)
        self.assertEqual(self.cash_transaction_deposit.reference_type, CashTransaction.REFERENCE_TYPE_BANK_DEPOSIT)
        self.assertEqual(self.cash_transaction_deposit.reference_id, self.bank_deposit.id)
        self.assertEqual(self.cash_transaction_deposit.amount, Decimal('-3000.00'))
        self.assertEqual(self.cash_transaction_deposit.notes, "Bank deposit")
        self.assertEqual(self.cash_transaction_deposit.tenant_id, self.tenant_id)
        self.assertEqual(self.cash_transaction_deposit.created_by, self.user_id)
    
    def test_cash_transaction_str(self):
        """
        Test CashTransaction string representation.
        """
        self.assertEqual(str(self.cash_transaction_sale), "TRX-2023-0001 - Sale - 4000.00")
        self.assertEqual(str(self.cash_transaction_expense), "TRX-2023-0002 - Expense - -500.00")
        self.assertEqual(str(self.cash_transaction_deposit), "TRX-2023-0003 - Deposit - -3000.00")
    
    def test_expense_category_creation(self):
        """
        Test ExpenseCategory creation.
        """
        self.assertEqual(self.expense_category.name, "Utilities")
        self.assertEqual(self.expense_category.code, "UTIL")
        self.assertEqual(self.expense_category.description, "Utility expenses")
        self.assertEqual(self.expense_category.tenant_id, self.tenant_id)
        self.assertEqual(self.expense_category.created_by, self.user_id)
        self.assertTrue(self.expense_category.is_active)
    
    def test_expense_category_str(self):
        """
        Test ExpenseCategory string representation.
        """
        self.assertEqual(str(self.expense_category), "UTIL - Utilities")
    
    def test_expense_creation(self):
        """
        Test Expense creation.
        """
        self.assertEqual(self.expense.shop_id, self.shop_id)
        self.assertEqual(self.expense.expense_number, "EXP-2023-0001")
        self.assertEqual(self.expense.expense_date, date(2023, 4, 15))
        self.assertEqual(self.expense.category, self.expense_category)
        self.assertEqual(self.expense.amount, Decimal('500.00'))
        self.assertEqual(self.expense.payment_method, Expense.PAYMENT_METHOD_CASH)
        self.assertEqual(self.expense.status, Expense.STATUS_APPROVED)
        self.assertEqual(self.expense.description, "Electricity bill")
        self.assertEqual(self.expense.notes, "Monthly electricity bill")
        self.assertEqual(self.expense.tenant_id, self.tenant_id)
        self.assertEqual(self.expense.created_by, self.user_id)
        self.assertEqual(self.expense.approved_by, self.user_id)
        self.assertIsNotNone(self.expense.approved_at)
        self.assertTrue(self.expense.is_active)
    
    def test_expense_str(self):
        """
        Test Expense string representation.
        """
        self.assertEqual(str(self.expense), "EXP-2023-0001 - Utilities - 500.00")
    
    def test_bank_deposit_creation(self):
        """
        Test BankDeposit creation.
        """
        self.assertEqual(self.bank_deposit.shop_id, self.shop_id)
        self.assertEqual(self.bank_deposit.deposit_number, "DEP-2023-0001")
        self.assertEqual(self.bank_deposit.deposit_date, date(2023, 4, 15))
        self.assertEqual(self.bank_deposit.bank_name, "HDFC Bank")
        self.assertEqual(self.bank_deposit.account_number, "12345678901234")
        self.assertEqual(self.bank_deposit.amount, Decimal('3000.00'))
        self.assertEqual(self.bank_deposit.status, BankDeposit.STATUS_PENDING)
        self.assertEqual(self.bank_deposit.notes, "Daily deposit")
        self.assertEqual(self.bank_deposit.tenant_id, self.tenant_id)
        self.assertEqual(self.bank_deposit.created_by, self.user_id)
        self.assertIsNone(self.bank_deposit.verified_by)
        self.assertIsNone(self.bank_deposit.verified_at)
        self.assertTrue(self.bank_deposit.is_active)
    
    def test_bank_deposit_str(self):
        """
        Test BankDeposit string representation.
        """
        self.assertEqual(str(self.bank_deposit), "DEP-2023-0001 - HDFC Bank - 3000.00")
    
    def test_daily_summary_creation(self):
        """
        Test DailySummary creation.
        """
        self.assertEqual(self.daily_summary.shop_id, self.shop_id)
        self.assertEqual(self.daily_summary.summary_date, date(2023, 4, 15))
        self.assertEqual(self.daily_summary.opening_balance, Decimal('5000.00'))
        self.assertEqual(self.daily_summary.closing_balance, Decimal('5500.00'))
        self.assertEqual(self.daily_summary.total_sales, Decimal('4000.00'))
        self.assertEqual(self.daily_summary.total_returns, Decimal('0.00'))
        self.assertEqual(self.daily_summary.total_expenses, Decimal('500.00'))
        self.assertEqual(self.daily_summary.total_deposits, Decimal('3000.00'))
        self.assertEqual(self.daily_summary.cash_difference, Decimal('0.00'))
        self.assertEqual(self.daily_summary.notes, "Daily summary")
        self.assertEqual(self.daily_summary.tenant_id, self.tenant_id)
        self.assertEqual(self.daily_summary.created_by, self.user_id)
        self.assertTrue(self.daily_summary.is_active)
    
    def test_daily_summary_str(self):
        """
        Test DailySummary string representation.
        """
        self.assertEqual(str(self.daily_summary), f"Summary for {date(2023, 4, 15)} - 5500.00")