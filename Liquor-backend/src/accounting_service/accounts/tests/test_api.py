import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from accounts.models import (
    AccountType, Account, FiscalYear, 
    AccountingPeriod, BankAccount
)
from common.jwt_auth import MicroserviceUser

class AccountsAPITest(TestCase):
    """
    Test the accounts API endpoints.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        
        # Create test user
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_accounts', 'add_accounts', 'change_accounts']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Create account types
        self.asset_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Assets",
            code="ASSET",
            type=AccountType.TYPE_ASSET,
            description="Asset accounts",
            created_by=self.user_id
        )
        
        self.liability_type = AccountType.objects.create(
            tenant_id=self.tenant_id,
            name="Liabilities",
            code="LIAB",
            type=AccountType.TYPE_LIABILITY,
            description="Liability accounts",
            created_by=self.user_id
        )
        
        # Create accounts
        self.parent_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="Current Assets",
            code="1000",
            description="Current assets",
            opening_balance=0,
            current_balance=0,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        self.cash_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
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
        
        self.bank_account_model = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="Bank Account",
            code="1002",
            description="Bank account",
            parent=self.parent_account,
            is_bank_account=True,
            opening_balance=5000,
            current_balance=7500,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        # Create bank account
        self.bank_account = BankAccount.objects.create(
            tenant_id=self.tenant_id,
            account=self.bank_account_model,
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
        
        # Create fiscal year
        self.fiscal_year = FiscalYear.objects.create(
            tenant_id=self.tenant_id,
            name="FY 2023-2024",
            start_date=date(2023, 4, 1),
            end_date=date(2024, 3, 31),
            status=FiscalYear.STATUS_ACTIVE,
            notes="Financial year 2023-2024",
            created_by=self.user_id
        )
        
        # Create accounting period
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
    
    def test_list_account_types(self):
        """
        Test listing account types.
        """
        url = reverse('accounttype-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], 'Assets')
        self.assertEqual(response.data['results'][1]['name'], 'Liabilities')
    
    def test_create_account_type(self):
        """
        Test creating an account type.
        """
        url = reverse('accounttype-list')
        data = {
            'name': 'Expenses',
            'code': 'EXP',
            'type': AccountType.TYPE_EXPENSE,
            'description': 'Expense accounts'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Expenses')
        self.assertEqual(response.data['code'], 'EXP')
        self.assertEqual(response.data['type'], AccountType.TYPE_EXPENSE)
        self.assertEqual(response.data['description'], 'Expense accounts')
        
        # Check that the account type was created in the database
        account_type = AccountType.objects.get(code='EXP')
        self.assertEqual(account_type.name, 'Expenses')
        self.assertEqual(account_type.tenant_id, self.tenant_id)
        self.assertEqual(account_type.created_by, self.user_id)
    
    def test_retrieve_account_type(self):
        """
        Test retrieving an account type.
        """
        url = reverse('accounttype-detail', args=[self.asset_type.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Assets')
        self.assertEqual(response.data['code'], 'ASSET')
        self.assertEqual(response.data['type'], AccountType.TYPE_ASSET)
    
    def test_update_account_type(self):
        """
        Test updating an account type.
        """
        url = reverse('accounttype-detail', args=[self.asset_type.id])
        data = {
            'name': 'Asset Accounts',
            'description': 'Updated description'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Asset Accounts')
        self.assertEqual(response.data['description'], 'Updated description')
        
        # Check that the account type was updated in the database
        self.asset_type.refresh_from_db()
        self.assertEqual(self.asset_type.name, 'Asset Accounts')
        self.assertEqual(self.asset_type.description, 'Updated description')
    
    def test_list_accounts(self):
        """
        Test listing accounts.
        """
        url = reverse('account-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_create_account(self):
        """
        Test creating an account.
        """
        url = reverse('account-list')
        data = {
            'account_type': str(self.liability_type.id),
            'name': 'Accounts Payable',
            'code': '2001',
            'description': 'Accounts payable',
            'parent': str(self.parent_account.id),
            'opening_balance': 0,
            'current_balance': 0,
            'status': Account.STATUS_ACTIVE
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Accounts Payable')
        self.assertEqual(response.data['code'], '2001')
        
        # Check that the account was created in the database
        account = Account.objects.get(code='2001')
        self.assertEqual(account.name, 'Accounts Payable')
        self.assertEqual(account.tenant_id, self.tenant_id)
        self.assertEqual(account.created_by, self.user_id)
    
    def test_retrieve_account(self):
        """
        Test retrieving an account.
        """
        url = reverse('account-detail', args=[self.cash_account.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cash')
        self.assertEqual(response.data['code'], '1001')
        self.assertEqual(response.data['is_cash_account'], True)
        self.assertEqual(response.data['current_balance'], '1500.00')
    
    def test_update_account(self):
        """
        Test updating an account.
        """
        url = reverse('account-detail', args=[self.cash_account.id])
        data = {
            'name': 'Cash on Hand',
            'description': 'Updated description'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cash on Hand')
        self.assertEqual(response.data['description'], 'Updated description')
        
        # Check that the account was updated in the database
        self.cash_account.refresh_from_db()
        self.assertEqual(self.cash_account.name, 'Cash on Hand')
        self.assertEqual(self.cash_account.description, 'Updated description')
    
    def test_list_fiscal_years(self):
        """
        Test listing fiscal years.
        """
        url = reverse('fiscalyear-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'FY 2023-2024')
    
    def test_create_fiscal_year(self):
        """
        Test creating a fiscal year.
        """
        url = reverse('fiscalyear-list')
        data = {
            'name': 'FY 2024-2025',
            'start_date': '2024-04-01',
            'end_date': '2025-03-31',
            'status': FiscalYear.STATUS_UPCOMING,
            'notes': 'Next financial year'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'FY 2024-2025')
        self.assertEqual(response.data['start_date'], '2024-04-01')
        self.assertEqual(response.data['end_date'], '2025-03-31')
        
        # Check that the fiscal year was created in the database
        fiscal_year = FiscalYear.objects.get(name='FY 2024-2025')
        self.assertEqual(fiscal_year.start_date, date(2024, 4, 1))
        self.assertEqual(fiscal_year.tenant_id, self.tenant_id)
        self.assertEqual(fiscal_year.created_by, self.user_id)
    
    def test_list_accounting_periods(self):
        """
        Test listing accounting periods.
        """
        url = reverse('accountingperiod-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'April 2023')
    
    def test_create_accounting_period(self):
        """
        Test creating an accounting period.
        """
        url = reverse('accountingperiod-list')
        data = {
            'fiscal_year': str(self.fiscal_year.id),
            'name': 'May 2023',
            'start_date': '2023-05-01',
            'end_date': '2023-05-31',
            'status': AccountingPeriod.STATUS_UPCOMING,
            'notes': 'May 2023 accounting period'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'May 2023')
        self.assertEqual(response.data['start_date'], '2023-05-01')
        self.assertEqual(response.data['end_date'], '2023-05-31')
        
        # Check that the accounting period was created in the database
        period = AccountingPeriod.objects.get(name='May 2023')
        self.assertEqual(period.start_date, date(2023, 5, 1))
        self.assertEqual(period.tenant_id, self.tenant_id)
        self.assertEqual(period.created_by, self.user_id)
    
    def test_list_bank_accounts(self):
        """
        Test listing bank accounts.
        """
        url = reverse('bankaccount-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['bank_name'], 'Test Bank')
        self.assertEqual(response.data['results'][0]['account_number'], '1234567890')
    
    def test_create_bank_account(self):
        """
        Test creating a bank account.
        """
        # First create a new account for the bank
        new_account = Account.objects.create(
            tenant_id=self.tenant_id,
            account_type=self.asset_type,
            name="New Bank Account",
            code="1003",
            description="New bank account",
            parent=self.parent_account,
            is_bank_account=True,
            opening_balance=0,
            current_balance=0,
            status=Account.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        url = reverse('bankaccount-list')
        data = {
            'account': str(new_account.id),
            'bank_name': 'New Test Bank',
            'account_number': '9876543210',
            'account_name': 'Test Company',
            'branch': 'New Branch',
            'ifsc_code': 'NEW1234',
            'opening_balance': 0,
            'current_balance': 0,
            'status': BankAccount.STATUS_ACTIVE,
            'notes': 'New test bank account'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['bank_name'], 'New Test Bank')
        self.assertEqual(response.data['account_number'], '9876543210')
        
        # Check that the bank account was created in the database
        bank_account = BankAccount.objects.get(account_number='9876543210')
        self.assertEqual(bank_account.bank_name, 'New Test Bank')
        self.assertEqual(bank_account.tenant_id, self.tenant_id)
        self.assertEqual(bank_account.created_by, self.user_id)