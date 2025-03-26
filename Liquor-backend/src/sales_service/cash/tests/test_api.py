import uuid
import json
from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from cash.models import (
    CashRegister, CashTransaction, BankDeposit,
    Expense, ExpenseCategory, DailySummary
)
from common.jwt_auth import MicroserviceUser

class CashAPITest(TestCase):
    """
    Test the cash API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.shop_id = uuid.uuid4()
        self.sale_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_cash', 'add_cash', 'change_cash']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
        
        # Create expense category
        self.expense_category = ExpenseCategory.objects.create(
            tenant_id=self.tenant_id,
            name="Utilities",
            code="UTIL",
            description="Utility expenses",
            created_by=self.user_id
        )
        
        # Create expense
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
        
        # Create cash transaction (expense)
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
    
    def test_list_cash_registers(self):
        """
        Test listing cash registers.
        """
        url = reverse('cashregister-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Main Register')
        self.assertEqual(response.data['results'][0]['code'], 'REG001')
    
    def test_filter_cash_registers_by_shop(self):
        """
        Test filtering cash registers by shop.
        """
        url = reverse('cashregister-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_create_cash_register(self):
        """
        Test creating a cash register.
        """
        url = reverse('cashregister-list')
        data = {
            'shop_id': str(self.shop_id),
            'name': 'Secondary Register',
            'code': 'REG002',
            'opening_balance': '2000.00',
            'current_balance': '2000.00',
            'status': CashRegister.STATUS_OPEN
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['name'], 'Secondary Register')
        self.assertEqual(response.data['code'], 'REG002')
        self.assertEqual(response.data['opening_balance'], '2000.00')
        self.assertEqual(response.data['current_balance'], '2000.00')
        self.assertEqual(response.data['status'], CashRegister.STATUS_OPEN)
        self.assertEqual(response.data['opened_by'], str(self.user_id))
        self.assertIsNotNone(response.data['opened_at'])
        
        # Check that the cash register was created in the database
        register = CashRegister.objects.get(code='REG002')
        self.assertEqual(register.name, 'Secondary Register')
        self.assertEqual(register.tenant_id, self.tenant_id)
        self.assertEqual(register.created_by, self.user_id)
    
    def test_retrieve_cash_register(self):
        """
        Test retrieving a cash register.
        """
        url = reverse('cashregister-detail', args=[self.cash_register.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['name'], 'Main Register')
        self.assertEqual(response.data['code'], 'REG001')
        self.assertEqual(response.data['opening_balance'], '5000.00')
        self.assertEqual(response.data['current_balance'], '8500.00')
        self.assertEqual(response.data['status'], CashRegister.STATUS_OPEN)
        self.assertEqual(response.data['opened_by'], str(self.user_id))
        self.assertIsNotNone(response.data['opened_at'])
    
    def test_close_cash_register(self):
        """
        Test closing a cash register.
        """
        url = reverse('cashregister-close', args=[self.cash_register.id])
        data = {
            'closing_balance': '8500.00',
            'notes': 'End of day closing'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], CashRegister.STATUS_CLOSED)
        self.assertEqual(response.data['current_balance'], '8500.00')
        self.assertEqual(response.data['closed_by'], str(self.user_id))
        self.assertIsNotNone(response.data['closed_at'])
        
        # Check that the cash register was closed in the database
        self.cash_register.refresh_from_db()
        self.assertEqual(self.cash_register.status, CashRegister.STATUS_CLOSED)
        self.assertEqual(self.cash_register.closed_by, self.user_id)
        self.assertIsNotNone(self.cash_register.closed_at)
    
    def test_list_cash_transactions(self):
        """
        Test listing cash transactions.
        """
        url = reverse('cashtransaction-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_filter_cash_transactions_by_shop(self):
        """
        Test filtering cash transactions by shop.
        """
        url = reverse('cashtransaction-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_cash_transactions_by_register(self):
        """
        Test filtering cash transactions by cash register.
        """
        url = reverse('cashtransaction-list')
        response = self.client.get(url, {'cash_register': self.cash_register.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['cash_register'], str(self.cash_register.id))
    
    def test_filter_cash_transactions_by_type(self):
        """
        Test filtering cash transactions by type.
        """
        url = reverse('cashtransaction-list')
        response = self.client.get(url, {'transaction_type': CashTransaction.TRANSACTION_TYPE_SALE})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['transaction_type'], CashTransaction.TRANSACTION_TYPE_SALE)
    
    def test_filter_cash_transactions_by_date_range(self):
        """
        Test filtering cash transactions by date range.
        """
        url = reverse('cashtransaction-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['transaction_date'], '2023-04-15')
    
    @patch('cash.views.generate_transaction_number')
    def test_create_cash_transaction(self, mock_generate_transaction_number):
        """
        Test creating a cash transaction.
        """
        mock_generate_transaction_number.return_value = "TRX-2023-0004"
        
        url = reverse('cashtransaction-list')
        data = {
            'shop_id': str(self.shop_id),
            'cash_register': str(self.cash_register.id),
            'transaction_date': '2023-04-16',
            'transaction_type': CashTransaction.TRANSACTION_TYPE_ADJUSTMENT,
            'reference_type': CashTransaction.REFERENCE_TYPE_MANUAL,
            'reference_id': str(uuid.uuid4()),
            'amount': '1000.00',
            'notes': 'Cash adjustment'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['transaction_number'], 'TRX-2023-0004')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['cash_register'], str(self.cash_register.id))
        self.assertEqual(response.data['transaction_date'], '2023-04-16')
        self.assertEqual(response.data['transaction_type'], CashTransaction.TRANSACTION_TYPE_ADJUSTMENT)
        self.assertEqual(response.data['reference_type'], CashTransaction.REFERENCE_TYPE_MANUAL)
        self.assertEqual(response.data['amount'], '1000.00')
        self.assertEqual(response.data['notes'], 'Cash adjustment')
        
        # Check that the cash transaction was created in the database
        transaction = CashTransaction.objects.get(transaction_number='TRX-2023-0004')
        self.assertEqual(transaction.transaction_type, CashTransaction.TRANSACTION_TYPE_ADJUSTMENT)
        self.assertEqual(transaction.amount, Decimal('1000.00'))
        self.assertEqual(transaction.tenant_id, self.tenant_id)
        self.assertEqual(transaction.created_by, self.user_id)
    
    def test_retrieve_cash_transaction(self):
        """
        Test retrieving a cash transaction.
        """
        url = reverse('cashtransaction-detail', args=[self.cash_transaction_sale.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['transaction_number'], 'TRX-2023-0001')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['cash_register'], str(self.cash_register.id))
        self.assertEqual(response.data['transaction_date'], '2023-04-15')
        self.assertEqual(response.data['transaction_type'], CashTransaction.TRANSACTION_TYPE_SALE)
        self.assertEqual(response.data['reference_type'], CashTransaction.REFERENCE_TYPE_SALE)
        self.assertEqual(response.data['reference_id'], str(self.sale_id))
        self.assertEqual(response.data['amount'], '4000.00')
        self.assertEqual(response.data['notes'], 'Sale transaction')
    
    def test_list_expense_categories(self):
        """
        Test listing expense categories.
        """
        url = reverse('expensecategory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Utilities')
        self.assertEqual(response.data['results'][0]['code'], 'UTIL')
    
    def test_create_expense_category(self):
        """
        Test creating an expense category.
        """
        url = reverse('expensecategory-list')
        data = {
            'name': 'Rent',
            'code': 'RENT',
            'description': 'Rent expenses'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Rent')
        self.assertEqual(response.data['code'], 'RENT')
        self.assertEqual(response.data['description'], 'Rent expenses')
        
        # Check that the expense category was created in the database
        category = ExpenseCategory.objects.get(code='RENT')
        self.assertEqual(category.name, 'Rent')
        self.assertEqual(category.tenant_id, self.tenant_id)
        self.assertEqual(category.created_by, self.user_id)
    
    def test_retrieve_expense_category(self):
        """
        Test retrieving an expense category.
        """
        url = reverse('expensecategory-detail', args=[self.expense_category.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Utilities')
        self.assertEqual(response.data['code'], 'UTIL')
        self.assertEqual(response.data['description'], 'Utility expenses')
    
    def test_update_expense_category(self):
        """
        Test updating an expense category.
        """
        url = reverse('expensecategory-detail', args=[self.expense_category.id])
        data = {
            'description': 'Updated utility expenses description'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated utility expenses description')
        
        # Check that the expense category was updated in the database
        self.expense_category.refresh_from_db()
        self.assertEqual(self.expense_category.description, 'Updated utility expenses description')
    
    def test_list_expenses(self):
        """
        Test listing expenses.
        """
        url = reverse('expense-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['expense_number'], 'EXP-2023-0001')
        self.assertEqual(response.data['results'][0]['amount'], '500.00')
    
    def test_filter_expenses_by_shop(self):
        """
        Test filtering expenses by shop.
        """
        url = reverse('expense-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_expenses_by_category(self):
        """
        Test filtering expenses by category.
        """
        url = reverse('expense-list')
        response = self.client.get(url, {'category': self.expense_category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], str(self.expense_category.id))
    
    def test_filter_expenses_by_date_range(self):
        """
        Test filtering expenses by date range.
        """
        url = reverse('expense-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['expense_date'], '2023-04-15')
    
    @patch('cash.views.generate_expense_number')
    def test_create_expense(self, mock_generate_expense_number):
        """
        Test creating an expense.
        """
        mock_generate_expense_number.return_value = "EXP-2023-0002"
        
        url = reverse('expense-list')
        data = {
            'shop_id': str(self.shop_id),
            'expense_date': '2023-04-16',
            'category': str(self.expense_category.id),
            'amount': '300.00',
            'payment_method': Expense.PAYMENT_METHOD_CASH,
            'status': Expense.STATUS_PENDING,
            'description': 'Water bill',
            'notes': 'Monthly water bill'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['expense_number'], 'EXP-2023-0002')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['expense_date'], '2023-04-16')
        self.assertEqual(response.data['category'], str(self.expense_category.id))
        self.assertEqual(response.data['amount'], '300.00')
        self.assertEqual(response.data['payment_method'], Expense.PAYMENT_METHOD_CASH)
        self.assertEqual(response.data['status'], Expense.STATUS_PENDING)
        self.assertEqual(response.data['description'], 'Water bill')
        self.assertEqual(response.data['notes'], 'Monthly water bill')
        
        # Check that the expense was created in the database
        expense = Expense.objects.get(expense_number='EXP-2023-0002')
        self.assertEqual(expense.description, 'Water bill')
        self.assertEqual(expense.amount, Decimal('300.00'))
        self.assertEqual(expense.tenant_id, self.tenant_id)
        self.assertEqual(expense.created_by, self.user_id)
    
    def test_retrieve_expense(self):
        """
        Test retrieving an expense.
        """
        url = reverse('expense-detail', args=[self.expense.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['expense_number'], 'EXP-2023-0001')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['expense_date'], '2023-04-15')
        self.assertEqual(response.data['category'], str(self.expense_category.id))
        self.assertEqual(response.data['amount'], '500.00')
        self.assertEqual(response.data['payment_method'], Expense.PAYMENT_METHOD_CASH)
        self.assertEqual(response.data['status'], Expense.STATUS_APPROVED)
        self.assertEqual(response.data['description'], 'Electricity bill')
        self.assertEqual(response.data['notes'], 'Monthly electricity bill')
    
    def test_approve_expense(self):
        """
        Test approving an expense.
        """
        # Create a pending expense for this test
        pending_expense = Expense.objects.create(
            tenant_id=self.tenant_id,
            shop_id=self.shop_id,
            expense_number="EXP-2023-0002",
            expense_date=date(2023, 4, 16),
            category=self.expense_category,
            amount=Decimal('300.00'),
            payment_method=Expense.PAYMENT_METHOD_CASH,
            status=Expense.STATUS_PENDING,
            description="Water bill",
            notes="Monthly water bill",
            created_by=self.user_id
        )
        
        url = reverse('expense-approve', args=[pending_expense.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Expense.STATUS_APPROVED)
        self.assertEqual(response.data['approved_by'], str(self.user_id))
        self.assertIsNotNone(response.data['approved_at'])
        
        # Check that the expense was approved in the database
        pending_expense.refresh_from_db()
        self.assertEqual(pending_expense.status, Expense.STATUS_APPROVED)
        self.assertEqual(pending_expense.approved_by, self.user_id)
        self.assertIsNotNone(pending_expense.approved_at)
    
    def test_list_bank_deposits(self):
        """
        Test listing bank deposits.
        """
        url = reverse('bankdeposit-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['deposit_number'], 'DEP-2023-0001')
        self.assertEqual(response.data['results'][0]['amount'], '3000.00')
    
    def test_filter_bank_deposits_by_shop(self):
        """
        Test filtering bank deposits by shop.
        """
        url = reverse('bankdeposit-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_bank_deposits_by_date_range(self):
        """
        Test filtering bank deposits by date range.
        """
        url = reverse('bankdeposit-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['deposit_date'], '2023-04-15')
    
    @patch('cash.views.generate_deposit_number')
    def test_create_bank_deposit(self, mock_generate_deposit_number):
        """
        Test creating a bank deposit.
        """
        mock_generate_deposit_number.return_value = "DEP-2023-0002"
        
        url = reverse('bankdeposit-list')
        data = {
            'shop_id': str(self.shop_id),
            'deposit_date': '2023-04-16',
            'bank_name': 'ICICI Bank',
            'account_number': '98765432109876',
            'amount': '2000.00',
            'status': BankDeposit.STATUS_PENDING,
            'notes': 'Another daily deposit'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['deposit_number'], 'DEP-2023-0002')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['deposit_date'], '2023-04-16')
        self.assertEqual(response.data['bank_name'], 'ICICI Bank')
        self.assertEqual(response.data['account_number'], '98765432109876')
        self.assertEqual(response.data['amount'], '2000.00')
        self.assertEqual(response.data['status'], BankDeposit.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Another daily deposit')
        
        # Check that the bank deposit was created in the database
        deposit = BankDeposit.objects.get(deposit_number='DEP-2023-0002')
        self.assertEqual(deposit.bank_name, 'ICICI Bank')
        self.assertEqual(deposit.amount, Decimal('2000.00'))
        self.assertEqual(deposit.tenant_id, self.tenant_id)
        self.assertEqual(deposit.created_by, self.user_id)
    
    def test_retrieve_bank_deposit(self):
        """
        Test retrieving a bank deposit.
        """
        url = reverse('bankdeposit-detail', args=[self.bank_deposit.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['deposit_number'], 'DEP-2023-0001')
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['deposit_date'], '2023-04-15')
        self.assertEqual(response.data['bank_name'], 'HDFC Bank')
        self.assertEqual(response.data['account_number'], '12345678901234')
        self.assertEqual(response.data['amount'], '3000.00')
        self.assertEqual(response.data['status'], BankDeposit.STATUS_PENDING)
        self.assertEqual(response.data['notes'], 'Daily deposit')
    
    def test_verify_bank_deposit(self):
        """
        Test verifying a bank deposit.
        """
        url = reverse('bankdeposit-verify', args=[self.bank_deposit.id])
        data = {
            'reference_number': 'REF123456',
            'notes': 'Verified deposit'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], BankDeposit.STATUS_VERIFIED)
        self.assertEqual(response.data['reference_number'], 'REF123456')
        self.assertEqual(response.data['notes'], 'Verified deposit')
        self.assertEqual(response.data['verified_by'], str(self.user_id))
        self.assertIsNotNone(response.data['verified_at'])
        
        # Check that the bank deposit was verified in the database
        self.bank_deposit.refresh_from_db()
        self.assertEqual(self.bank_deposit.status, BankDeposit.STATUS_VERIFIED)
        self.assertEqual(self.bank_deposit.reference_number, 'REF123456')
        self.assertEqual(self.bank_deposit.notes, 'Verified deposit')
        self.assertEqual(self.bank_deposit.verified_by, self.user_id)
        self.assertIsNotNone(self.bank_deposit.verified_at)
    
    def test_list_daily_summaries(self):
        """
        Test listing daily summaries.
        """
        url = reverse('dailysummary-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['summary_date'], '2023-04-15')
        self.assertEqual(response.data['results'][0]['closing_balance'], '5500.00')
    
    def test_filter_daily_summaries_by_shop(self):
        """
        Test filtering daily summaries by shop.
        """
        url = reverse('dailysummary-list')
        response = self.client.get(url, {'shop_id': self.shop_id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['shop_id'], str(self.shop_id))
    
    def test_filter_daily_summaries_by_date_range(self):
        """
        Test filtering daily summaries by date range.
        """
        url = reverse('dailysummary-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['summary_date'], '2023-04-15')
    
    def test_create_daily_summary(self):
        """
        Test creating a daily summary.
        """
        url = reverse('dailysummary-list')
        data = {
            'shop_id': str(self.shop_id),
            'summary_date': '2023-04-16',
            'opening_balance': '5500.00',
            'closing_balance': '6000.00',
            'total_sales': '3000.00',
            'total_returns': '0.00',
            'total_expenses': '200.00',
            'total_deposits': '2300.00',
            'cash_difference': '0.00',
            'notes': 'Daily summary for April 16'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['summary_date'], '2023-04-16')
        self.assertEqual(response.data['opening_balance'], '5500.00')
        self.assertEqual(response.data['closing_balance'], '6000.00')
        self.assertEqual(response.data['total_sales'], '3000.00')
        self.assertEqual(response.data['total_returns'], '0.00')
        self.assertEqual(response.data['total_expenses'], '200.00')
        self.assertEqual(response.data['total_deposits'], '2300.00')
        self.assertEqual(response.data['cash_difference'], '0.00')
        self.assertEqual(response.data['notes'], 'Daily summary for April 16')
        
        # Check that the daily summary was created in the database
        summary = DailySummary.objects.get(summary_date=date(2023, 4, 16))
        self.assertEqual(summary.closing_balance, Decimal('6000.00'))
        self.assertEqual(summary.tenant_id, self.tenant_id)
        self.assertEqual(summary.created_by, self.user_id)
    
    def test_retrieve_daily_summary(self):
        """
        Test retrieving a daily summary.
        """
        url = reverse('dailysummary-detail', args=[self.daily_summary.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shop_id'], str(self.shop_id))
        self.assertEqual(response.data['summary_date'], '2023-04-15')
        self.assertEqual(response.data['opening_balance'], '5000.00')
        self.assertEqual(response.data['closing_balance'], '5500.00')
        self.assertEqual(response.data['total_sales'], '4000.00')
        self.assertEqual(response.data['total_returns'], '0.00')
        self.assertEqual(response.data['total_expenses'], '500.00')
        self.assertEqual(response.data['total_deposits'], '3000.00')
        self.assertEqual(response.data['cash_difference'], '0.00')
        self.assertEqual(response.data['notes'], 'Daily summary')