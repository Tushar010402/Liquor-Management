import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.utils import timezone
from accounts.models import FiscalYear, AccountingPeriod
from reports.models import (
    FinancialReport, ReportSchedule, ReportTemplate
)

class ReportsModelsTest(TestCase):
    """
    Test the reports models.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.tenant_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        
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
            generated_at=timezone.now()
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
    
    def test_financial_report_creation(self):
        """
        Test FinancialReport creation.
        """
        self.assertEqual(self.financial_report.report_number, "PL-2023-0001")
        self.assertEqual(self.financial_report.report_name, "Profit & Loss - April 2023")
        self.assertEqual(self.financial_report.report_type, FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(self.financial_report.fiscal_year, self.fiscal_year)
        self.assertEqual(self.financial_report.accounting_period, self.accounting_period)
        self.assertEqual(self.financial_report.start_date, date(2023, 4, 1))
        self.assertEqual(self.financial_report.end_date, date(2023, 4, 30))
        self.assertEqual(self.financial_report.parameters, {
            'include_zero_balances': False,
            'show_percentages': True
        })
        self.assertEqual(self.financial_report.status, FinancialReport.STATUS_GENERATED)
        self.assertEqual(self.financial_report.notes, "Monthly P&L report")
        self.assertEqual(self.financial_report.report_data['revenue'], 50000)
        self.assertEqual(self.financial_report.report_data['expenses'], 30000)
        self.assertEqual(self.financial_report.report_data['profit'], 20000)
        self.assertEqual(len(self.financial_report.report_data['details']), 4)
        self.assertEqual(self.financial_report.tenant_id, self.tenant_id)
        self.assertEqual(self.financial_report.created_by, self.user_id)
        self.assertEqual(self.financial_report.generated_by, self.user_id)
        self.assertIsNotNone(self.financial_report.generated_at)
        self.assertTrue(self.financial_report.is_active)
    
    def test_financial_report_str(self):
        """
        Test FinancialReport string representation.
        """
        self.assertEqual(
            str(self.financial_report), 
            f"Profit & Loss - April 2023 - {date(2023, 4, 1)} to {date(2023, 4, 30)}"
        )
    
    def test_report_schedule_creation(self):
        """
        Test ReportSchedule creation.
        """
        self.assertEqual(self.report_schedule.name, "Monthly P&L Report")
        self.assertEqual(self.report_schedule.report_type, FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(self.report_schedule.frequency, ReportSchedule.FREQUENCY_MONTHLY)
        self.assertEqual(self.report_schedule.next_run_date, date(2023, 5, 1))
        self.assertEqual(self.report_schedule.parameters, {
            'include_zero_balances': False,
            'show_percentages': True
        })
        self.assertEqual(len(self.report_schedule.recipients), 2)
        self.assertEqual(self.report_schedule.recipients[0]['email'], 'manager@example.com')
        self.assertEqual(self.report_schedule.recipients[1]['email'], 'accountant@example.com')
        self.assertEqual(self.report_schedule.status, ReportSchedule.STATUS_ACTIVE)
        self.assertEqual(self.report_schedule.tenant_id, self.tenant_id)
        self.assertEqual(self.report_schedule.created_by, self.user_id)
        self.assertTrue(self.report_schedule.is_active)
    
    def test_report_schedule_str(self):
        """
        Test ReportSchedule string representation.
        """
        self.assertEqual(
            str(self.report_schedule), 
            "Monthly P&L Report - Profit & Loss - Monthly"
        )
    
    def test_report_template_creation(self):
        """
        Test ReportTemplate creation.
        """
        self.assertEqual(self.report_template.name, "Standard P&L Template")
        self.assertEqual(self.report_template.report_type, FinancialReport.TYPE_PROFIT_LOSS)
        self.assertEqual(self.report_template.description, "Standard profit and loss report template")
        self.assertEqual(len(self.report_template.template_data['sections']), 3)
        self.assertEqual(self.report_template.template_data['sections'][0]['title'], 'Revenue')
        self.assertEqual(self.report_template.template_data['sections'][1]['title'], 'Expenses')
        self.assertEqual(self.report_template.template_data['sections'][2]['title'], 'Net Profit/Loss')
        self.assertTrue(self.report_template.template_data['show_percentages'])
        self.assertEqual(self.report_template.template_data['comparison_periods'], 1)
        self.assertEqual(self.report_template.status, ReportTemplate.STATUS_ACTIVE)
        self.assertEqual(self.report_template.tenant_id, self.tenant_id)
        self.assertEqual(self.report_template.created_by, self.user_id)
        self.assertTrue(self.report_template.is_active)
    
    def test_report_template_str(self):
        """
        Test ReportTemplate string representation.
        """
        self.assertEqual(
            str(self.report_template), 
            "Standard P&L Template - Profit & Loss"
        )