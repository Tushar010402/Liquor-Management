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
from journals.models import (
    Journal, JournalEntry, RecurringJournal, RecurringJournalEntry
)
from common.jwt_auth import MicroserviceUser

class JournalsAPITest(TestCase):
    """
    Test the journals API endpoints.
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
            'permissions': ['view_journals', 'add_journals', 'change_journals']
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
        self.recurring_debit_entry = RecurringJournalEntry.objects.create(
            tenant_id=self.tenant_id,
            recurring_journal=self.recurring_journal,
            account=self.bank_account,
            description="Bank debit",
            debit_amount=0,
            credit_amount=5000,
            shop_id=self.shop_id
        )
        
        self.recurring_credit_entry = RecurringJournalEntry.objects.create(
            tenant_id=self.tenant_id,
            recurring_journal=self.recurring_journal,
            account=self.creditor_account,
            description="Creditor debit",
            debit_amount=5000,
            credit_amount=0,
            shop_id=self.shop_id
        )
    
    def test_list_journals(self):
        """
        Test listing journals.
        """
        url = reverse('journal-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['journal_number'], 'JV-2023-0001')
    
    def test_create_journal(self):
        """
        Test creating a journal.
        """
        url = reverse('journal-list')
        data = {
            'journal_number': 'JV-2023-0002',
            'journal_date': '2023-04-20',
            'fiscal_year': str(self.fiscal_year.id),
            'accounting_period': str(self.accounting_period.id),
            'journal_type': Journal.TYPE_GENERAL,
            'description': 'New test journal entry',
            'entries': [
                {
                    'account': str(self.bank_account.id),
                    'description': 'Bank debit',
                    'debit_amount': 2000,
                    'credit_amount': 0,
                    'shop_id': str(self.shop_id)
                },
                {
                    'account': str(self.creditor_account.id),
                    'description': 'Creditor credit',
                    'debit_amount': 0,
                    'credit_amount': 2000,
                    'shop_id': str(self.shop_id)
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['journal_number'], 'JV-2023-0002')
        self.assertEqual(response.data['journal_date'], '2023-04-20')
        self.assertEqual(response.data['total_debit'], '2000.00')
        self.assertEqual(response.data['total_credit'], '2000.00')
        self.assertEqual(len(response.data['entries']), 2)
        
        # Check that the journal was created in the database
        journal = Journal.objects.get(journal_number='JV-2023-0002')
        self.assertEqual(journal.description, 'New test journal entry')
        self.assertEqual(journal.tenant_id, self.tenant_id)
        self.assertEqual(journal.created_by, self.user_id)
        
        # Check that the journal entries were created
        entries = journal.entries.all()
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.filter(debit_amount__gt=0).first().debit_amount, 2000)
        self.assertEqual(entries.filter(credit_amount__gt=0).first().credit_amount, 2000)
    
    def test_retrieve_journal(self):
        """
        Test retrieving a journal.
        """
        url = reverse('journal-detail', args=[self.journal.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['journal_number'], 'JV-2023-0001')
        self.assertEqual(response.data['journal_date'], '2023-04-15')
        self.assertEqual(response.data['description'], 'Test journal entry')
        self.assertEqual(len(response.data['entries']), 2)
    
    def test_update_journal(self):
        """
        Test updating a journal.
        """
        url = reverse('journal-detail', args=[self.journal.id])
        data = {
            'description': 'Updated journal description'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated journal description')
        
        # Check that the journal was updated in the database
        self.journal.refresh_from_db()
        self.assertEqual(self.journal.description, 'Updated journal description')
    
    def test_post_journal(self):
        """
        Test posting a journal.
        """
        url = reverse('journal-post', args=[self.journal.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Journal.STATUS_POSTED)
        
        # Check that the journal was posted in the database
        self.journal.refresh_from_db()
        self.assertEqual(self.journal.status, Journal.STATUS_POSTED)
        self.assertEqual(self.journal.posted_by, self.user_id)
        self.assertIsNotNone(self.journal.posted_at)
    
    def test_reverse_journal(self):
        """
        Test reversing a journal.
        """
        # First post the journal
        self.journal.status = Journal.STATUS_POSTED
        self.journal.posted_by = self.user_id
        self.journal.posted_at = date(2023, 4, 16)
        self.journal.save()
        
        url = reverse('journal-reverse', args=[self.journal.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Journal.STATUS_REVERSED)
        
        # Check that the journal was reversed in the database
        self.journal.refresh_from_db()
        self.assertEqual(self.journal.status, Journal.STATUS_REVERSED)
        self.assertEqual(self.journal.reversed_by, self.user_id)
        self.assertIsNotNone(self.journal.reversed_at)
    
    def test_list_recurring_journals(self):
        """
        Test listing recurring journals.
        """
        url = reverse('recurringjournal-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Monthly Rent')
    
    def test_create_recurring_journal(self):
        """
        Test creating a recurring journal.
        """
        url = reverse('recurringjournal-list')
        data = {
            'name': 'Quarterly Insurance',
            'description': 'Quarterly insurance payment',
            'journal_type': Journal.TYPE_GENERAL,
            'frequency': RecurringJournal.FREQUENCY_QUARTERLY,
            'start_date': '2023-04-01',
            'end_date': '2024-03-31',
            'next_run_date': '2023-07-01',
            'entries': [
                {
                    'account': str(self.bank_account.id),
                    'description': 'Bank credit',
                    'debit_amount': 0,
                    'credit_amount': 3000,
                    'shop_id': str(self.shop_id)
                },
                {
                    'account': str(self.creditor_account.id),
                    'description': 'Insurance debit',
                    'debit_amount': 3000,
                    'credit_amount': 0,
                    'shop_id': str(self.shop_id)
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Quarterly Insurance')
        self.assertEqual(response.data['frequency'], RecurringJournal.FREQUENCY_QUARTERLY)
        self.assertEqual(response.data['total_debit'], '3000.00')
        self.assertEqual(response.data['total_credit'], '3000.00')
        self.assertEqual(len(response.data['entries']), 2)
        
        # Check that the recurring journal was created in the database
        journal = RecurringJournal.objects.get(name='Quarterly Insurance')
        self.assertEqual(journal.description, 'Quarterly insurance payment')
        self.assertEqual(journal.tenant_id, self.tenant_id)
        self.assertEqual(journal.created_by, self.user_id)
        
        # Check that the recurring journal entries were created
        entries = journal.entries.all()
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.filter(debit_amount__gt=0).first().debit_amount, 3000)
        self.assertEqual(entries.filter(credit_amount__gt=0).first().credit_amount, 3000)
    
    def test_retrieve_recurring_journal(self):
        """
        Test retrieving a recurring journal.
        """
        url = reverse('recurringjournal-detail', args=[self.recurring_journal.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Monthly Rent')
        self.assertEqual(response.data['frequency'], RecurringJournal.FREQUENCY_MONTHLY)
        self.assertEqual(response.data['description'], 'Monthly rent payment')
        self.assertEqual(len(response.data['entries']), 2)
    
    def test_update_recurring_journal(self):
        """
        Test updating a recurring journal.
        """
        url = reverse('recurringjournal-detail', args=[self.recurring_journal.id])
        data = {
            'description': 'Updated recurring journal description'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Updated recurring journal description')
        
        # Check that the recurring journal was updated in the database
        self.recurring_journal.refresh_from_db()
        self.assertEqual(self.recurring_journal.description, 'Updated recurring journal description')
    
    def test_generate_journal_from_recurring(self):
        """
        Test generating a journal from a recurring journal.
        """
        url = reverse('recurringjournal-generate', args=[self.recurring_journal.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('journal_id', response.data)
        
        # Check that the journal was created in the database
        journal_id = response.data['journal_id']
        journal = Journal.objects.get(id=journal_id)
        self.assertEqual(journal.description, 'Monthly rent payment')
        self.assertEqual(journal.total_debit, 5000)
        self.assertEqual(journal.total_credit, 5000)
        self.assertEqual(journal.tenant_id, self.tenant_id)
        self.assertEqual(journal.created_by, self.user_id)
        
        # Check that the journal entries were created
        entries = journal.entries.all()
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.filter(debit_amount__gt=0).first().debit_amount, 5000)
        self.assertEqual(entries.filter(credit_amount__gt=0).first().credit_amount, 5000)