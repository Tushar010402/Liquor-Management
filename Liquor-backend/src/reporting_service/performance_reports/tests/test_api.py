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

class PerformanceReportsAPITest(TestCase):
    """
    Test the performance reports API endpoints.
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
            'permissions': ['view_reports', 'export_reports', 'view_performance_reports']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample sales performance data for mocking
        self.sales_performance_data = {
            'current_period': {
                'start_date': '2023-04-01',
                'end_date': '2023-04-30',
                'total_sales': '250000.00',
                'total_invoices': 350,
                'average_sale': '714.29',
                'highest_sale': '5000.00',
                'lowest_sale': '100.00'
            },
            'previous_period': {
                'start_date': '2023-03-01',
                'end_date': '2023-03-31',
                'total_sales': '220000.00',
                'total_invoices': 320,
                'average_sale': '687.50',
                'highest_sale': '4800.00',
                'lowest_sale': '95.00'
            },
            'change': {
                'total_sales': '30000.00',
                'total_sales_percentage': '13.64',
                'total_invoices': 30,
                'total_invoices_percentage': '9.38',
                'average_sale': '26.79',
                'average_sale_percentage': '3.90'
            }
        }
        
        # Sample employee performance data for mocking
        self.employee_performance_data = [
            {
                'employee_id': str(uuid.uuid4()),
                'employee_name': 'John Smith',
                'total_sales': '85000.00',
                'total_invoices': 120,
                'average_sale': '708.33',
                'highest_sale': '5000.00',
                'sales_target': '100000.00',
                'target_achievement': '85.00'
            },
            {
                'employee_id': str(uuid.uuid4()),
                'employee_name': 'Jane Doe',
                'total_sales': '75000.00',
                'total_invoices': 105,
                'average_sale': '714.29',
                'highest_sale': '4500.00',
                'sales_target': '80000.00',
                'target_achievement': '93.75'
            },
            {
                'employee_id': str(uuid.uuid4()),
                'employee_name': 'Bob Johnson',
                'total_sales': '90000.00',
                'total_invoices': 125,
                'average_sale': '720.00',
                'highest_sale': '4800.00',
                'sales_target': '90000.00',
                'target_achievement': '100.00'
            }
        ]
        
        # Sample product performance data for mocking
        self.product_performance_data = [
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'quantity_sold': 85,
                'total_sales': '85000.00',
                'profit_margin': '25.00',
                'profit_amount': '21250.00',
                'stock_turnover': '2.5'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Red Label',
                'variant_name': '750ml',
                'quantity_sold': 120,
                'total_sales': '60000.00',
                'profit_margin': '20.00',
                'profit_amount': '12000.00',
                'stock_turnover': '3.0'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'quantity_sold': 100,
                'total_sales': '50000.00',
                'profit_margin': '22.00',
                'profit_amount': '11000.00',
                'stock_turnover': '2.8'
            }
        ]
        
        # Sample category performance data for mocking
        self.category_performance_data = [
            {
                'category_id': str(uuid.uuid4()),
                'category_name': 'Whisky',
                'total_sales': '145000.00',
                'quantity_sold': 205,
                'profit_amount': '33250.00',
                'profit_margin': '22.93',
                'sales_percentage': '58.00'
            },
            {
                'category_id': str(uuid.uuid4()),
                'category_name': 'Vodka',
                'total_sales': '50000.00',
                'quantity_sold': 100,
                'profit_amount': '11000.00',
                'profit_margin': '22.00',
                'sales_percentage': '20.00'
            },
            {
                'category_id': str(uuid.uuid4()),
                'category_name': 'Rum',
                'total_sales': '30000.00',
                'quantity_sold': 60,
                'profit_amount': '6600.00',
                'profit_margin': '22.00',
                'sales_percentage': '12.00'
            },
            {
                'category_id': str(uuid.uuid4()),
                'category_name': 'Beer',
                'total_sales': '25000.00',
                'quantity_sold': 250,
                'profit_amount': '5000.00',
                'profit_margin': '20.00',
                'sales_percentage': '10.00'
            }
        ]
        
        # Sample KPI data for mocking
        self.kpi_data = {
            'sales_growth': {
                'value': '13.64',
                'target': '10.00',
                'status': 'above_target'
            },
            'average_transaction_value': {
                'value': '714.29',
                'target': '700.00',
                'status': 'above_target'
            },
            'profit_margin': {
                'value': '22.50',
                'target': '25.00',
                'status': 'below_target'
            },
            'inventory_turnover': {
                'value': '2.8',
                'target': '3.0',
                'status': 'below_target'
            },
            'customer_retention': {
                'value': '85.00',
                'target': '80.00',
                'status': 'above_target'
            }
        }
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_performance_report(self, mock_get_data):
        """
        Test getting sales performance report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_performance_data
        
        url = reverse('sales-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'compare_with_previous': 'true'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['current_period']['total_sales'], '250000.00')
        self.assertEqual(response.data['data']['current_period']['total_invoices'], 350)
        self.assertEqual(response.data['data']['previous_period']['total_sales'], '220000.00')
        self.assertEqual(response.data['data']['change']['total_sales_percentage'], '13.64')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30',
                'compare_with_previous': 'true'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_sales_performance_report(self, mock_get_data, mock_generate_excel):
        """
        Test exporting sales performance report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_performance_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/sales_performance_report.xlsx'
        
        url = reverse('export-sales-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'compare_with_previous': 'true'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/sales_performance_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30',
                'compare_with_previous': 'true'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_employee_performance_report(self, mock_get_data):
        """
        Test getting employee performance report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.employee_performance_data
        
        url = reverse('employee-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['employee_name'], 'John Smith')
        self.assertEqual(response.data['data'][0]['total_sales'], '85000.00')
        self.assertEqual(response.data['data'][0]['target_achievement'], '85.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/employees/',
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
    def test_employee_performance_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating employee performance chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.employee_performance_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/employee_performance.png'
        
        url = reverse('employee-performance-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'bar',
            'metric': 'total_sales'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/employee_performance.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/employees/',
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
            data=self.employee_performance_data,
            chart_type='bar',
            x_column='employee_name',
            y_column='total_sales',
            title='Employee Performance - Total Sales',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_product_performance_report(self, mock_get_data):
        """
        Test getting product performance report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.product_performance_data
        
        url = reverse('product-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['total_sales'], '85000.00')
        self.assertEqual(response.data['data'][0]['profit_margin'], '25.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/products/',
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
    def test_product_performance_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating product performance chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.product_performance_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/product_performance.png'
        
        url = reverse('product-performance-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'bar',
            'metric': 'total_sales'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/product_performance.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/products/',
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
            data=self.product_performance_data,
            chart_type='bar',
            x_column='product_name',
            y_column='total_sales',
            title='Product Performance - Total Sales',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_category_performance_report(self, mock_get_data):
        """
        Test getting category performance report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.category_performance_data
        
        url = reverse('category-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 4)
        self.assertEqual(response.data['data'][0]['category_name'], 'Whisky')
        self.assertEqual(response.data['data'][0]['total_sales'], '145000.00')
        self.assertEqual(response.data['data'][0]['sales_percentage'], '58.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/categories/',
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
    def test_category_performance_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating category performance chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.category_performance_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/category_performance.png'
        
        url = reverse('category-performance-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'pie',
            'metric': 'total_sales'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/category_performance.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/categories/',
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
            data=self.category_performance_data,
            chart_type='pie',
            x_column='category_name',
            y_column='total_sales',
            title='Category Performance - Total Sales',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_kpi_report(self, mock_get_data):
        """
        Test getting KPI report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.kpi_data
        
        url = reverse('kpi-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['sales_growth']['value'], '13.64')
        self.assertEqual(response.data['data']['sales_growth']['status'], 'above_target')
        self.assertEqual(response.data['data']['profit_margin']['value'], '22.50')
        self.assertEqual(response.data['data']['profit_margin']['status'], 'below_target')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/performance/kpi/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to performance reports.
        """
        # Create a user without performance report permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': ['view_reports']  # Has view_reports but not view_performance_reports
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('sales-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'compare_with_previous': 'true'
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
        
        url = reverse('sales-performance-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'compare_with_previous': 'true'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve performance data from service')