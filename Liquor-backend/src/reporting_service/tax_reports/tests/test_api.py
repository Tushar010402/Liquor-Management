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

class TaxReportsAPITest(TestCase):
    """
    Test the tax reports API endpoints.
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
            'permissions': ['view_reports', 'export_reports', 'view_tax_reports']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample tax summary data for mocking
        self.tax_summary_data = {
            'total_sales': '500000.00',
            'taxable_sales': '450000.00',
            'tax_collected': {
                'CGST': '40500.00',
                'SGST': '40500.00',
                'IGST': '0.00',
                'total': '81000.00'
            },
            'tax_rates': {
                'CGST': '9.00',
                'SGST': '9.00',
                'IGST': '0.00'
            }
        }
        
        # Sample monthly tax data for mocking
        self.monthly_tax_data = [
            {
                'month': 'January 2023',
                'total_sales': '150000.00',
                'taxable_sales': '135000.00',
                'tax_collected': {
                    'CGST': '12150.00',
                    'SGST': '12150.00',
                    'IGST': '0.00',
                    'total': '24300.00'
                }
            },
            {
                'month': 'February 2023',
                'total_sales': '160000.00',
                'taxable_sales': '144000.00',
                'tax_collected': {
                    'CGST': '12960.00',
                    'SGST': '12960.00',
                    'IGST': '0.00',
                    'total': '25920.00'
                }
            },
            {
                'month': 'March 2023',
                'total_sales': '190000.00',
                'taxable_sales': '171000.00',
                'tax_collected': {
                    'CGST': '15390.00',
                    'SGST': '15390.00',
                    'IGST': '0.00',
                    'total': '30780.00'
                }
            }
        ]
        
        # Sample tax by product category data for mocking
        self.tax_by_category_data = [
            {
                'category': 'Whisky',
                'total_sales': '250000.00',
                'taxable_sales': '225000.00',
                'tax_collected': {
                    'CGST': '20250.00',
                    'SGST': '20250.00',
                    'IGST': '0.00',
                    'total': '40500.00'
                }
            },
            {
                'category': 'Vodka',
                'total_sales': '100000.00',
                'taxable_sales': '90000.00',
                'tax_collected': {
                    'CGST': '8100.00',
                    'SGST': '8100.00',
                    'IGST': '0.00',
                    'total': '16200.00'
                }
            },
            {
                'category': 'Rum',
                'total_sales': '80000.00',
                'taxable_sales': '72000.00',
                'tax_collected': {
                    'CGST': '6480.00',
                    'SGST': '6480.00',
                    'IGST': '0.00',
                    'total': '12960.00'
                }
            },
            {
                'category': 'Beer',
                'total_sales': '70000.00',
                'taxable_sales': '63000.00',
                'tax_collected': {
                    'CGST': '5670.00',
                    'SGST': '5670.00',
                    'IGST': '0.00',
                    'total': '11340.00'
                }
            }
        ]
        
        # Sample tax filing data for mocking
        self.tax_filing_data = [
            {
                'filing_period': 'Q1 2023',
                'start_date': '2023-01-01',
                'end_date': '2023-03-31',
                'total_sales': '500000.00',
                'taxable_sales': '450000.00',
                'tax_collected': {
                    'CGST': '40500.00',
                    'SGST': '40500.00',
                    'IGST': '0.00',
                    'total': '81000.00'
                },
                'filing_due_date': '2023-04-20',
                'filing_status': 'pending'
            },
            {
                'filing_period': 'Q4 2022',
                'start_date': '2022-10-01',
                'end_date': '2022-12-31',
                'total_sales': '450000.00',
                'taxable_sales': '405000.00',
                'tax_collected': {
                    'CGST': '36450.00',
                    'SGST': '36450.00',
                    'IGST': '0.00',
                    'total': '72900.00'
                },
                'filing_due_date': '2023-01-20',
                'filing_status': 'completed',
                'filing_date': '2023-01-15',
                'filing_reference': 'GST-Q4-2022-001'
            }
        ]
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_tax_summary_report(self, mock_get_data):
        """
        Test getting tax summary report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_summary_data
        
        url = reverse('tax-summary-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['total_sales'], '500000.00')
        self.assertEqual(response.data['data']['taxable_sales'], '450000.00')
        self.assertEqual(response.data['data']['tax_collected']['CGST'], '40500.00')
        self.assertEqual(response.data['data']['tax_collected']['SGST'], '40500.00')
        self.assertEqual(response.data['data']['tax_collected']['total'], '81000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/summary/',
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
    def test_export_tax_summary_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting tax summary report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_summary_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/tax_summary_report.xlsx'
        
        url = reverse('export-tax-summary-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/tax_summary_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/summary/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_monthly_tax_report(self, mock_get_data):
        """
        Test getting monthly tax report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.monthly_tax_data
        
        url = reverse('monthly-tax-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['month'], 'January 2023')
        self.assertEqual(response.data['data'][0]['total_sales'], '150000.00')
        self.assertEqual(response.data['data'][0]['tax_collected']['total'], '24300.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/monthly/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_monthly_tax_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating monthly tax chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.monthly_tax_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/monthly_tax.png'
        
        url = reverse('monthly-tax-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31',
            'chart_type': 'bar'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/monthly_tax.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/monthly/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=self.monthly_tax_data,
            chart_type='bar',
            x_column='month',
            y_column='tax_collected.total',
            title='Monthly Tax Collection',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_tax_by_category_report(self, mock_get_data):
        """
        Test getting tax by category report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_by_category_data
        
        url = reverse('tax-by-category-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 4)
        self.assertEqual(response.data['data'][0]['category'], 'Whisky')
        self.assertEqual(response.data['data'][0]['total_sales'], '250000.00')
        self.assertEqual(response.data['data'][0]['tax_collected']['total'], '40500.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/by-category/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_tax_by_category_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating tax by category chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_by_category_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/tax_by_category.png'
        
        url = reverse('tax-by-category-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31',
            'chart_type': 'pie'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/tax_by_category.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/by-category/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-03-31'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=self.tax_by_category_data,
            chart_type='pie',
            x_column='category',
            y_column='tax_collected.total',
            title='Tax Collection by Category',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_tax_filing_report(self, mock_get_data):
        """
        Test getting tax filing report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_filing_data
        
        url = reverse('tax-filing-report')
        params = {
            'shop_id': str(self.shop_id),
            'year': '2023'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['filing_period'], 'Q1 2023')
        self.assertEqual(response.data['data'][0]['total_sales'], '500000.00')
        self.assertEqual(response.data['data'][0]['tax_collected']['total'], '81000.00')
        self.assertEqual(response.data['data'][0]['filing_status'], 'pending')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/filings/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'year': '2023'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_tax_filing_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting tax filing report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.tax_filing_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/tax_filing_report.xlsx'
        
        url = reverse('export-tax-filing-report')
        params = {
            'shop_id': str(self.shop_id),
            'year': '2023'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/tax_filing_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/accounting/tax/filings/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'year': '2023'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once_with(
            data=self.tax_filing_data,
            sheet_names=['Tax Filings'],
            filename=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to tax reports.
        """
        # Create a user without tax report permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': ['view_reports']  # Has view_reports but not view_tax_reports
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('tax-summary-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
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
        
        url = reverse('tax-summary-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-03-31'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve tax data from service')