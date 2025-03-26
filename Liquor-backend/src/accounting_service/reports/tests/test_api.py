import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from accounts.models import FiscalYear, AccountingPeriod
from reports.models import (
    FinancialReport, ReportSchedule, ReportTemplate
)
from common.jwt_auth import MicroserviceUser

class ReportsAPITest(TestCase):
    """
    Test the reports API endpoints.
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
            'permissions': ['view_reports', 'add_reports', 'change_reports']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
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
        
        # Create financial report
        self.financial_report = FinancialReport.objects.create(
            tenant_id=self.tenant_id,
            report_number="PL-2023-0001",
            report_name="Profit & Loss - April 2023",
            report_type=FinancialReport.TYPE_PROFIT_LOSS,
            fiscal_year=self.fiscal_year,
            accounting_period=self.accounting_period,
            start_date=date(2023, 4, 1),
            end_date=date(2023, 4, 30),
            parameters={
                'include_zero_balances': False,
                'show_percentages': True
            },
            status=FinancialReport.STATUS_GENERATED,
            notes="Monthly P&L report",
            report_data={
                'revenue': 50000,
                'expenses': 30000,
                'profit': 20000,
                'details': [
                    {'account': 'Sales', 'amount': 50000},
                    {'account': 'Rent', 'amount': 10000},
                    {'account': 'Salaries', 'amount': 15000},
                    {'account': 'Utilities', 'amount': 5000}
                ]
            },
            created_by=self.user_id,
            generated_by=self.user_id,
            generated_at=date(2023, 4, 30)
        )
        
        # Create report schedule
        self.report_schedule = ReportSchedule.objects.create(
            tenant_id=self.tenant_id,
            name="Monthly P&L Report",
            report_type=FinancialReport.TYPE_PROFIT_LOSS,
            frequency=ReportSchedule.FREQUENCY_MONTHLY,
            next_run_date=date(2023, 5, 1),
            parameters={
                'include_zero_balances': False,
                'show_percentages': True
            },
            recipients=[
                {'email': 'manager@example.com', 'name': 'Manager'},
                {'email': 'accountant@example.com', 'name': 'Accountant'}
            ],
            status=ReportSchedule.STATUS_ACTIVE,
            created_by=self.user_id
        )
        
        # Create report template
        self.report_template = ReportTemplate.objects.create(
            tenant_id=self.tenant_id,
            name="Standard P&L Template",
            report_type=FinancialReport.TYPE_PROFIT_LOSS,
            description="Standard profit and loss report template",
            template_data={
                'sections': [
                    {
                        'title': 'Revenue',
                        'account_types': ['revenue'],
                        'subtotal': True
                    },
                    {
                        'title': 'Expenses',
                        'account_types': ['expense'],
                        'subtotal': True
                    },
                    {
                        'title': 'Net Profit/Loss',
                        'calculation': 'Revenue - Expenses',
                        'bold': True
                    }
                ],
                'show_percentages': True,
                'comparison_periods': 1
            },
            status=ReportTemplate.STATUS_ACTIVE,
            created_by=self.user_id
        )
    
    def test_list_financial_reports(self):
        """
        Test listing financial reports.
        """
        url = reverse('financialreport-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['report_name'], 'Profit & Loss - April 2023')
    
    def test_filter_financial_reports_by_type(self):
        """
        Test filtering financial reports by type.
        """
        url = reverse('financialreport-list')
        response = self.client.get(url, {'report_type': FinancialReport.TYPE_PROFIT_LOSS})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['report_type'], FinancialReport.TYPE_PROFIT_LOSS)
    
    def test_filter_financial_reports_by_period(self):
        """
        Test filtering financial reports by accounting period.
        """
        url = reverse('financialreport-list')
        response = self.client.get(url, {'accounting_period': self.accounting_period.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['accounting_period'], str(self.accounting_period.id))
    
    def test_retrieve_financial_report(self):
        """
        Test retrieving a financial report.
        """
        url = reverse('financialreport-detail', args=[self.financial_report.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_name'], 'Profit & Loss - April 2023')
        self.assertEqual(response.data['report_type'], FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(response.data['status'], FinancialReport.STATUS_GENERATED)
        self.assertEqual(response.data['report_data']['revenue'], 50000)
        self.assertEqual(response.data['report_data']['expenses'], 30000)
        self.assertEqual(response.data['report_data']['profit'], 20000)
        self.assertEqual(len(response.data['report_data']['details']), 4)
    
    @patch('reports.views.generate_profit_loss_report')
    def test_generate_profit_loss_report(self, mock_generate):
        """
        Test generating a profit and loss report.
        """
        # Mock the report generation function
        mock_report_data = {
            'revenue': 60000,
            'expenses': 35000,
            'profit': 25000,
            'details': [
                {'account': 'Sales', 'amount': 60000},
                {'account': 'Rent', 'amount': 10000},
                {'account': 'Salaries', 'amount': 20000},
                {'account': 'Utilities', 'amount': 5000}
            ]
        }
        mock_generate.return_value = mock_report_data
        
        url = reverse('profit-loss-report')
        data = {
            'fiscal_year': str(self.fiscal_year.id),
            'accounting_period': str(self.accounting_period.id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'parameters': {
                'include_zero_balances': False,
                'show_percentages': True
            }
        }
        response = self.client.get(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_data']['revenue'], 60000)
        self.assertEqual(response.data['report_data']['expenses'], 35000)
        self.assertEqual(response.data['report_data']['profit'], 25000)
        self.assertEqual(len(response.data['report_data']['details']), 4)
        
        # Check that the mock function was called with the correct arguments
        mock_generate.assert_called_once()
        args, kwargs = mock_generate.call_args
        self.assertEqual(kwargs['fiscal_year_id'], str(self.fiscal_year.id))
        self.assertEqual(kwargs['accounting_period_id'], str(self.accounting_period.id))
        self.assertEqual(kwargs['start_date'], '2023-04-01')
        self.assertEqual(kwargs['end_date'], '2023-04-30')
    
    @patch('reports.views.generate_balance_sheet')
    def test_generate_balance_sheet(self, mock_generate):
        """
        Test generating a balance sheet.
        """
        # Mock the report generation function
        mock_report_data = {
            'assets': 100000,
            'liabilities': 60000,
            'equity': 40000,
            'details': {
                'assets': [
                    {'account': 'Cash', 'amount': 20000},
                    {'account': 'Inventory', 'amount': 80000}
                ],
                'liabilities': [
                    {'account': 'Accounts Payable', 'amount': 60000}
                ],
                'equity': [
                    {'account': 'Capital', 'amount': 40000}
                ]
            }
        }
        mock_generate.return_value = mock_report_data
        
        url = reverse('balance-sheet-report')
        data = {
            'fiscal_year': str(self.fiscal_year.id),
            'as_of_date': '2023-04-30',
            'parameters': {
                'include_zero_balances': False,
                'show_percentages': True
            }
        }
        response = self.client.get(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['report_data']['assets'], 100000)
        self.assertEqual(response.data['report_data']['liabilities'], 60000)
        self.assertEqual(response.data['report_data']['equity'], 40000)
        self.assertEqual(len(response.data['report_data']['details']['assets']), 2)
        self.assertEqual(len(response.data['report_data']['details']['liabilities']), 1)
        self.assertEqual(len(response.data['report_data']['details']['equity']), 1)
        
        # Check that the mock function was called with the correct arguments
        mock_generate.assert_called_once()
        args, kwargs = mock_generate.call_args
        self.assertEqual(kwargs['fiscal_year_id'], str(self.fiscal_year.id))
        self.assertEqual(kwargs['as_of_date'], '2023-04-30')
    
    def test_list_report_schedules(self):
        """
        Test listing report schedules.
        """
        url = reverse('reportschedule-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Monthly P&L Report')
    
    def test_create_report_schedule(self):
        """
        Test creating a report schedule.
        """
        url = reverse('reportschedule-list')
        data = {
            'name': 'Quarterly Balance Sheet',
            'report_type': FinancialReport.TYPE_BALANCE_SHEET,
            'frequency': ReportSchedule.FREQUENCY_QUARTERLY,
            'next_run_date': '2023-06-30',
            'parameters': {
                'include_zero_balances': False,
                'show_percentages': True
            },
            'recipients': [
                {'email': 'ceo@example.com', 'name': 'CEO'},
                {'email': 'cfo@example.com', 'name': 'CFO'}
            ],
            'status': ReportSchedule.STATUS_ACTIVE
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Quarterly Balance Sheet')
        self.assertEqual(response.data['report_type'], FinancialReport.TYPE_BALANCE_SHEET)
        self.assertEqual(response.data['frequency'], ReportSchedule.FREQUENCY_QUARTERLY)
        self.assertEqual(response.data['next_run_date'], '2023-06-30')
        self.assertEqual(len(response.data['recipients']), 2)
        
        # Check that the report schedule was created in the database
        schedule = ReportSchedule.objects.get(name='Quarterly Balance Sheet')
        self.assertEqual(schedule.report_type, FinancialReport.TYPE_BALANCE_SHEET)
        self.assertEqual(schedule.frequency, ReportSchedule.FREQUENCY_QUARTERLY)
        self.assertEqual(schedule.next_run_date, date(2023, 6, 30))
        self.assertEqual(schedule.tenant_id, self.tenant_id)
        self.assertEqual(schedule.created_by, self.user_id)
    
    def test_retrieve_report_schedule(self):
        """
        Test retrieving a report schedule.
        """
        url = reverse('reportschedule-detail', args=[self.report_schedule.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Monthly P&L Report')
        self.assertEqual(response.data['report_type'], FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(response.data['frequency'], ReportSchedule.FREQUENCY_MONTHLY)
        self.assertEqual(response.data['next_run_date'], '2023-05-01')
        self.assertEqual(len(response.data['recipients']), 2)
    
    def test_update_report_schedule(self):
        """
        Test updating a report schedule.
        """
        url = reverse('reportschedule-detail', args=[self.report_schedule.id])
        data = {
            'name': 'Updated Monthly P&L Report',
            'next_run_date': '2023-05-15'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Monthly P&L Report')
        self.assertEqual(response.data['next_run_date'], '2023-05-15')
        
        # Check that the report schedule was updated in the database
        self.report_schedule.refresh_from_db()
        self.assertEqual(self.report_schedule.name, 'Updated Monthly P&L Report')
        self.assertEqual(self.report_schedule.next_run_date, date(2023, 5, 15))
    
    def test_list_report_templates(self):
        """
        Test listing report templates.
        """
        url = reverse('reporttemplate-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Standard P&L Template')
    
    def test_create_report_template(self):
        """
        Test creating a report template.
        """
        url = reverse('reporttemplate-list')
        data = {
            'name': 'Standard Balance Sheet Template',
            'report_type': FinancialReport.TYPE_BALANCE_SHEET,
            'description': 'Standard balance sheet template',
            'template_data': {
                'sections': [
                    {
                        'title': 'Assets',
                        'account_types': ['asset'],
                        'subtotal': True
                    },
                    {
                        'title': 'Liabilities',
                        'account_types': ['liability'],
                        'subtotal': True
                    },
                    {
                        'title': 'Equity',
                        'account_types': ['equity'],
                        'subtotal': True
                    }
                ],
                'show_percentages': True
            },
            'status': ReportTemplate.STATUS_ACTIVE
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Standard Balance Sheet Template')
        self.assertEqual(response.data['report_type'], FinancialReport.TYPE_BALANCE_SHEET)
        self.assertEqual(response.data['description'], 'Standard balance sheet template')
        self.assertEqual(len(response.data['template_data']['sections']), 3)
        
        # Check that the report template was created in the database
        template = ReportTemplate.objects.get(name='Standard Balance Sheet Template')
        self.assertEqual(template.report_type, FinancialReport.TYPE_BALANCE_SHEET)
        self.assertEqual(template.description, 'Standard balance sheet template')
        self.assertEqual(template.tenant_id, self.tenant_id)
        self.assertEqual(template.created_by, self.user_id)
    
    def test_retrieve_report_template(self):
        """
        Test retrieving a report template.
        """
        url = reverse('reporttemplate-detail', args=[self.report_template.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Standard P&L Template')
        self.assertEqual(response.data['report_type'], FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(response.data['description'], 'Standard profit and loss report template')
        self.assertEqual(len(response.data['template_data']['sections']), 3)
    
    def test_update_report_template(self):
        """
        Test updating a report template.
        """
        url = reverse('reporttemplate-detail', args=[self.report_template.id])
        data = {
            'name': 'Updated P&L Template',
            'description': 'Updated profit and loss report template'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated P&L Template')
        self.assertEqual(response.data['description'], 'Updated profit and loss report template')
        
        # Check that the report template was updated in the database
        self.report_template.refresh_from_db()
        self.assertEqual(self.report_template.name, 'Updated P&L Template')
        self.assertEqual(self.report_template.description, 'Updated profit and loss report template')