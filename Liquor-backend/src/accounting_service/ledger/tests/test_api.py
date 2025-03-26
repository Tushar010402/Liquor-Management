import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from accounts.models import (
    AccountType, Account, FiscalYear, AccountingPeriod
)
from journals.models import Journal, JournalEntry
from ledger.models import (
    GeneralLedger, AccountBalance, TrialBalance, TrialBalanceEntry
)
from common.jwt_auth import MicroserviceUser

class LedgerAPITest(TestCase):
    """
    Test the ledger API endpoints.
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
        
        self.user = MicroserviceUser({
            'id': str(self.user_id),
            'email': 'test@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'tenant_admin',
            'permissions': ['view_ledger', 'add_ledger', 'change_ledger']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
            posted_at=date(2023, 4, 15)
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
            finalized_at=date(2023, 4, 30)
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
    
    def test_list_general_ledger(self):
        """
        Test listing general ledger entries.
        """
        url = reverse('generalledger-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_general_ledger_by_account(self):
        """
        Test filtering general ledger entries by account.
        """
        url = reverse('generalledger-list')
        response = self.client.get(url, {'account': self.cash_account.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['account'], str(self.cash_account.id))
        self.assertEqual(response.data['results'][0]['debit_amount'], '1000.00')
    
    def test_filter_general_ledger_by_date_range(self):
        """
        Test filtering general ledger entries by date range.
        """
        url = reverse('generalledger-list')
        response = self.client.get(url, {
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_general_ledger(self):
        """
        Test retrieving a general ledger entry.
        """
        url = reverse('generalledger-detail', args=[self.debit_ledger.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account'], str(self.cash_account.id))
        self.assertEqual(response.data['debit_amount'], '1000.00')
        self.assertEqual(response.data['credit_amount'], '0.00')
        self.assertEqual(response.data['balance'], '1000.00')
    
    def test_list_account_balances(self):
        """
        Test listing account balances.
        """
        url = reverse('accountbalance-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_account_balances_by_account(self):
        """
        Test filtering account balances by account.
        """
        url = reverse('accountbalance-list')
        response = self.client.get(url, {'account': self.cash_account.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['account'], str(self.cash_account.id))
        self.assertEqual(response.data['results'][0]['current_balance'], '1000.00')
    
    def test_filter_account_balances_by_period(self):
        """
        Test filtering account balances by accounting period.
        """
        url = reverse('accountbalance-list')
        response = self.client.get(url, {'accounting_period': self.accounting_period.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_account_balance(self):
        """
        Test retrieving an account balance.
        """
        url = reverse('accountbalance-detail', args=[self.cash_balance.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['account'], str(self.cash_account.id))
        self.assertEqual(response.data['opening_balance'], '0.00')
        self.assertEqual(response.data['current_balance'], '1000.00')
        self.assertEqual(response.data['total_debits'], '1000.00')
        self.assertEqual(response.data['total_credits'], '0.00')
    
    def test_list_trial_balances(self):
        """
        Test listing trial balances.
        """
        url = reverse('trialbalance-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['as_of_date'], '2023-04-30')
    
    def test_filter_trial_balances_by_period(self):
        """
        Test filtering trial balances by accounting period.
        """
        url = reverse('trialbalance-list')
        response = self.client.get(url, {'accounting_period': self.accounting_period.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['accounting_period'], str(self.accounting_period.id))
    
    def test_retrieve_trial_balance(self):
        """
        Test retrieving a trial balance.
        """
        url = reverse('trialbalance-detail', args=[self.trial_balance.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['as_of_date'], '2023-04-30')
        self.assertEqual(response.data['total_debits'], '1000.00')
        self.assertEqual(response.data['total_credits'], '1000.00')
        self.assertEqual(response.data['status'], TrialBalance.STATUS_FINAL)
        self.assertEqual(len(response.data['entries']), 2)
    
    def test_generate_trial_balance(self):
        """
        Test generating a trial balance.
        """
        url = reverse('trialbalance-generate')
        data = {
            'fiscal_year': str(self.fiscal_year.id),
            'accounting_period': str(self.accounting_period.id),
            'as_of_date': '2023-04-30'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['as_of_date'], '2023-04-30')
        self.assertEqual(response.data['total_debits'], '1000.00')
        self.assertEqual(response.data['total_credits'], '1000.00')
        self.assertEqual(response.data['status'], TrialBalance.STATUS_DRAFT)
        self.assertEqual(len(response.data['entries']), 2)
        
        # Check that the trial balance was created in the database
        trial_balance_id = response.data['id']
        trial_balance = TrialBalance.objects.get(id=trial_balance_id)
        self.assertEqual(trial_balance.as_of_date, date(2023, 4, 30))
        self.assertEqual(trial_balance.total_debits, 1000)
        self.assertEqual(trial_balance.total_credits, 1000)
        self.assertEqual(trial_balance.status, TrialBalance.STATUS_DRAFT)
        self.assertEqual(trial_balance.tenant_id, self.tenant_id)
        self.assertEqual(trial_balance.created_by, self.user_id)
        
        # Check that the trial balance entries were created
        entries = trial_balance.entries.all()
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.filter(debit_amount__gt=0).first().debit_amount, 1000)
        self.assertEqual(entries.filter(credit_amount__gt=0).first().credit_amount, 1000)
    
    def test_finalize_trial_balance(self):
        """
        Test finalizing a trial balance.
        """
        # Create a draft trial balance
        draft_trial_balance = TrialBalance.objects.create(
            tenant_id=self.tenant_id,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            as_of_date=date(2023, 4, 30),
            total_debits=1000,
            total_credits=1000,
            status=TrialBalance.STATUS_DRAFT,
            created_by=self.user_id
        )
        
        # Create trial balance entries
        TrialBalanceEntry.objects.create(
            tenant_id=self.tenant_id,
            trial_balance=draft_trial_balance,
            account=self.cash_account,
            debit_amount=1000,
            credit_amount=0
        )
        
        TrialBalanceEntry.objects.create(
            tenant_id=self.tenant_id,
            trial_balance=draft_trial_balance,
            account=self.creditor_account,
            debit_amount=0,
            credit_amount=1000
        )
        
        url = reverse('trialbalance-finalize', args=[draft_trial_balance.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], TrialBalance.STATUS_FINAL)
        
        # Check that the trial balance was finalized in the database
        draft_trial_balance.refresh_from_db()
        self.assertEqual(draft_trial_balance.status, TrialBalance.STATUS_FINAL)
        self.assertEqual(draft_trial_balance.finalized_by, self.user_id)
        self.assertIsNotNone(draft_trial_balance.finalized_at)