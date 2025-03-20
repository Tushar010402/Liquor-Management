import uuid
import json
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from common.jwt_auth import MicroserviceUser

class FinancialReportsAPITest(TestCase):
    """
    Test the financial reports API endpoints.
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
            'permissions': ['view_reports', 'export_reports', 'view_financial_reports']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample profit and loss data for mocking
        self.profit_loss_data = {
            'revenue': {
                'sales': '250000.00',
                'other_income': '5000.00',
                'total_revenue': '255000.00'
            },
            'cost_of_goods_sold': {
                'purchases': '150000.00',
                'inventory_adjustment': '-2000.00',
                'total_cogs': '148000.00'
            },
            'gross_profit': '107000.00',
            'expenses': {
                'salaries': '30000.00',
                'rent': '15000.00',
                'utilities': '5000.00',
                'marketing': '10000.00',
                'other_expenses': '7000.00',
                'total_expenses': '67000.00'
            },
            'net_profit': '40000.00',
            'profit_margin': '15.69'
        }
        
        # Sample balance sheet data for mocking
        self.balance_sheet_data = {
            'assets': {
                'current_assets': {
                    'cash': '50000.00',
                    'accounts_receivable': '15000.00',
                    'inventory': '180000.00',
                    'total_current_assets': '245000.00'
                },
                'fixed_assets': {
                    'furniture_and_fixtures': '25000.00',
                    'equipment': '35000.00',
                    'vehicles': '40000.00',
                    'total_fixed_assets': '100000.00'
                },
                'total_assets': '345000.00'
            },
            'liabilities': {
                'current_liabilities': {
                    'accounts_payable': '30000.00',
                    'short_term_loans': '20000.00',
                    'taxes_payable': '15000.00',
                    'total_current_liabilities': '65000.00'
                },
                'long_term_liabilities': {
                    'long_term_loans': '80000.00',
                    'total_long_term_liabilities': '80000.00'
                },
                'total_liabilities': '145000.00'
            },
            'equity': {
                'capital': '150000.00',
                'retained_earnings': '50000.00',
                'total_equity': '200000.00'
            },
            'total_liabilities_and_equity': '345000.00'
        }
        
        # Sample cash flow data for mocking
        self.cash_flow_data = {
            'operating_activities': {
                'net_profit': '40000.00',
                'adjustments': {
                    'depreciation': '5000.00',
                    'inventory_changes': '-10000.00',
                    'accounts_receivable_changes': '-5000.00',
                    'accounts_payable_changes': '8000.00',
                    'total_adjustments': '-2000.00'
                },
                'net_cash_from_operating': '38000.00'
            },
            'investing_activities': {
                'purchase_of_equipment': '-15000.00',
                'sale_of_assets': '2000.00',
                'net_cash_from_investing': '-13000.00'
            },
            'financing_activities': {
                'loan_repayments': '-10000.00',
                'capital_injection': '0.00',
                'net_cash_from_financing': '-10000.00'
            },
            'net_increase_in_cash': '15000.00',
            'opening_cash_balance': '35000.00',
            'closing_cash_balance': '50000.00'
        }
        
        # Sample sales tax data for mocking
        self.sales_tax_data = [
            {
                'month': 'January 2023',
                'total_sales': '200000.00',
                'taxable_sales': '180000.00',
                'tax_collected': '32400.00',
                'tax_rate': '18.00'
            },
            {
                'month': 'February 2023',
                'total_sales': '220000.00',
                'taxable_sales': '198000.00',
                'tax_collected': '35640.00',
                'tax_rate': '18.00'
            },
            {
                'month': 'March 2023',
                'total_sales': '250000.00',
                'taxable_sales': '225000.00',
                'tax_collected': '40500.00',
                'tax_rate': '18.00'
            }
        ]
        
        # Sample expense data for mocking
        self.expense_data = [
            {
                'id': str(uuid.uuid4()),
                'expense_date': '2023-04-15',
                'category': 'Rent',
                'amount': '15000.00',
                'description': 'Monthly shop rent',
                'payment_method': 'Bank Transfer'
            },
            {
                'id': str(uuid.uuid4()),
                'expense_date': '2023-04-16',
                'category': 'Utilities',
                'amount': '5000.00',
                'description': 'Electricity and water bills',
                'payment_method': 'Cash'
            },
            {
                'id': str(uuid.uuid4()),
                'expense_date': '2023-04-20',
                'category': 'Salaries',
                'amount': '30000.00',
                'description': 'Staff salaries',
                'payment_method': 'Bank Transfer'
            }
        ]
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_profit_loss_report(self, mock_get_data):
        """
        Test getting profit and loss report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.profit_loss_data
        
        url = reverse('profit-loss-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['revenue']['total_revenue'], '255000.00')
        self.assertEqual(response.data['data']['gross_profit'], '107000.00')
        self.assertEqual(response.data['data']['net_profit'], '40000.00')
        self.assertEqual(response.data['data']['profit_margin'], '15.69')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/profit-loss/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_profit_loss_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting profit and loss report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.profit_loss_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/profit_loss_report.xlsx'
        
        url = reverse('export-profit-loss-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/profit_loss_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/profit-loss/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_balance_sheet_report(self, mock_get_data):
        """
        Test getting balance sheet report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.balance_sheet_data
        
        url = reverse('balance-sheet-report')
        params = {
            'shop_id': str(self.shop_id),
            'as_of_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['assets']['total_assets'], '345000.00')
        self.assertEqual(response.data['data']['liabilities']['total_liabilities'], '145000.00')
        self.assertEqual(response.data['data']['equity']['total_equity'], '200000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/balance-sheet/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'as_of_date': '2023-04-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_balance_sheet_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting balance sheet report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.balance_sheet_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/balance_sheet_report.xlsx'
        
        url = reverse('export-balance-sheet-report')
        params = {
            'shop_id': str(self.shop_id),
            'as_of_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/balance_sheet_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/balance-sheet/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'as_of_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_cash_flow_report(self, mock_get_data):
        """
        Test getting cash flow report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.cash_flow_data
        
        url = reverse('cash-flow-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['operating_activities']['net_cash_from_operating'], '38000.00')
        self.assertEqual(response.data['data']['investing_activities']['net_cash_from_investing'], '-13000.00')
        self.assertEqual(response.data['data']['financing_activities']['net_cash_from_financing'], '-10000.00')
        self.assertEqual(response.data['data']['net_increase_in_cash'], '15000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/cash-flow/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_cash_flow_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting cash flow report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.cash_flow_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/cash_flow_report.xlsx'
        
        url = reverse('export-cash-flow-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/cash_flow_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/cash-flow/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_tax_report(self, mock_get_data):
        """
        Test getting sales tax report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_tax_data
        
        url = reverse('sales-tax-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['month'], 'January 2023')
        self.assertEqual(response.data['data'][0]['total_sales'], '200000.00')
        self.assertEqual(response.data['data'][0]['tax_collected'], '32400.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/sales-tax/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_sales_tax_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting sales tax report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_tax_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/sales_tax_report.xlsx'
        
        url = reverse('export-sales-tax-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/sales_tax_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/sales-tax/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once_with(
            data=self.sales_tax_data,
            sheet_names=['Sales Tax Report'],
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_expense_report(self, mock_get_data):
        """
        Test getting expense report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.expense_data
        
        url = reverse('expense-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['category'], 'Rent')
        self.assertEqual(response.data['data'][0]['amount'], '15000.00')
        self.assertEqual(response.data['data'][1]['category'], 'Utilities')
        self.assertEqual(response.data['data'][1]['amount'], '5000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/expenses/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_expense_by_category_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating expense by category chart.
        """
        # Sample expense by category data
        expense_by_category_data = [
            {'category': 'Rent', 'total_amount': '15000.00'},
            {'category': 'Utilities', 'total_amount': '5000.00'},
            {'category': 'Salaries', 'total_amount': '30000.00'},
            {'category': 'Marketing', 'total_amount': '10000.00'},
            {'category': 'Other', 'total_amount': '7000.00'}
        ]
        
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = expense_by_category_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/expense_by_category.png'
        
        url = reverse('expense-by-category-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'pie'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/expense_by_category.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/expenses/by-category/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=expense_by_category_data,
            chart_type='pie',
            x_column='category',
            y_column='total_amount',
            title='Expenses by Category',
            filename=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to financial reports.
        """
        # Create a user without financial report permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': ['view_reports']  # Has view_reports but not view_financial_reports
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('profit-loss-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_service_error_handling(self, mock_get_data):
        """
        Test handling of service errors.
        """
        # Mock the get_report_data_from_service function to return None (error)
        mock_get_data.return_value = None
        
        url = reverse('profit-loss-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve financial data from service')