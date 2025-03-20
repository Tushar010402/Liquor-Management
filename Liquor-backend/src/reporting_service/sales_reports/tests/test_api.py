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

class SalesReportsAPITest(TestCase):
    """
    Test the sales reports API endpoints.
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
            'permissions': ['view_reports', 'export_reports']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample sales data for mocking
        self.sales_data = [
            {
                'id': str(uuid.uuid4()),
                'invoice_number': 'INV-2023-0001',
                'invoice_date': '2023-04-15',
                'customer_name': 'John Doe',
                'total_amount': '3955.00',
                'status': 'completed'
            },
            {
                'id': str(uuid.uuid4()),
                'invoice_number': 'INV-2023-0002',
                'invoice_date': '2023-04-16',
                'customer_name': 'Jane Smith',
                'total_amount': '2825.00',
                'status': 'completed'
            },
            {
                'id': str(uuid.uuid4()),
                'invoice_number': 'INV-2023-0003',
                'invoice_date': '2023-04-17',
                'customer_name': 'Bob Johnson',
                'total_amount': '1750.00',
                'status': 'completed'
            }
        ]
        
        # Sample sales summary data for mocking
        self.sales_summary_data = {
            'total_sales': '8530.00',
            'total_invoices': 3,
            'average_sale': '2843.33',
            'highest_sale': '3955.00',
            'lowest_sale': '1750.00'
        }
        
        # Sample product sales data for mocking
        self.product_sales_data = [
            {
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'quantity_sold': 5,
                'total_amount': '17500.00'
            },
            {
                'product_name': 'Johnnie Walker Red Label',
                'variant_name': '750ml',
                'quantity_sold': 8,
                'total_amount': '12000.00'
            },
            {
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'quantity_sold': 10,
                'total_amount': '8000.00'
            }
        ]
        
        # Sample customer sales data for mocking
        self.customer_sales_data = [
            {
                'customer_name': 'John Doe',
                'total_purchases': 5,
                'total_amount': '15000.00',
                'average_purchase': '3000.00'
            },
            {
                'customer_name': 'Jane Smith',
                'total_purchases': 3,
                'total_amount': '8500.00',
                'average_purchase': '2833.33'
            },
            {
                'customer_name': 'Bob Johnson',
                'total_purchases': 2,
                'total_amount': '3500.00',
                'average_purchase': '1750.00'
            }
        ]
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_report(self, mock_get_data):
        """
        Test getting sales report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_data
        
        url = reverse('sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['invoice_number'], 'INV-2023-0001')
        self.assertEqual(response.data['data'][1]['invoice_number'], 'INV-2023-0002')
        self.assertEqual(response.data['data'][2]['invoice_number'], 'INV-2023-0003')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/',
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
    def test_export_sales_report_excel(self, mock_get_data, mock_generate_excel):
        """
        Test exporting sales report as Excel.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/sales_report.xlsx'
        
        url = reverse('export-sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'format': 'excel'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/sales_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once_with(
            data=self.sales_data,
            sheet_names=['Sales Report'],
            filename=any
        )
    
    @patch('common.utils.report_utils.generate_csv_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_sales_report_csv(self, mock_get_data, mock_generate_csv):
        """
        Test exporting sales report as CSV.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_data
        
        # Mock the generate_csv_report function
        mock_generate_csv.return_value = '/media/reports/sales_report.csv'
        
        url = reverse('export-sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'format': 'csv'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/sales_report.csv')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the CSV report was generated
        mock_generate_csv.assert_called_once_with(
            data=self.sales_data,
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_summary_report(self, mock_get_data):
        """
        Test getting sales summary report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_summary_data
        
        url = reverse('sales-summary-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['total_sales'], '8530.00')
        self.assertEqual(response.data['data']['total_invoices'], 3)
        self.assertEqual(response.data['data']['average_sale'], '2843.33')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/summary/',
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
    def test_sales_trend_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating sales trend chart.
        """
        # Sample sales trend data
        sales_trend_data = [
            {'date': '2023-04-01', 'total_sales': '1200.00'},
            {'date': '2023-04-02', 'total_sales': '1500.00'},
            {'date': '2023-04-03', 'total_sales': '1000.00'},
            {'date': '2023-04-04', 'total_sales': '1800.00'},
            {'date': '2023-04-05', 'total_sales': '2000.00'}
        ]
        
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = sales_trend_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/sales_trend.png'
        
        url = reverse('sales-trend-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-05',
            'chart_type': 'line'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/sales_trend.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/trend/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-04-01',
                'end_date': '2023-04-05'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=sales_trend_data,
            chart_type='line',
            x_column='date',
            y_column='total_sales',
            title='Sales Trend',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_product_sales_report(self, mock_get_data):
        """
        Test getting product sales report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.product_sales_data
        
        url = reverse('product-sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['quantity_sold'], 5)
        self.assertEqual(response.data['data'][0]['total_amount'], '17500.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/products/',
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
    def test_product_sales_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating product sales chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.product_sales_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/product_sales.png'
        
        url = reverse('product-sales-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'bar'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/product_sales.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/products/',
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
            data=self.product_sales_data,
            chart_type='bar',
            x_column='product_name',
            y_column='total_amount',
            title='Product Sales',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_customer_sales_report(self, mock_get_data):
        """
        Test getting customer sales report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.customer_sales_data
        
        url = reverse('customer-sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['customer_name'], 'John Doe')
        self.assertEqual(response.data['data'][0]['total_purchases'], 5)
        self.assertEqual(response.data['data'][0]['total_amount'], '15000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/customers/',
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
    def test_customer_sales_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating customer sales chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.customer_sales_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/customer_sales.png'
        
        url = reverse('customer-sales-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'pie'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/customer_sales.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/sales/customers/',
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
            data=self.customer_sales_data,
            chart_type='pie',
            x_column='customer_name',
            y_column='total_amount',
            title='Customer Sales',
            filename=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to reports.
        """
        # Create a user without report permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': []
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('sales-report')
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
        
        url = reverse('sales-report')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve sales data from service')