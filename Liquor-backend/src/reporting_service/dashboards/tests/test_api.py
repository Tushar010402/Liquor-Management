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

class DashboardsAPITest(TestCase):
    """
    Test the dashboards API endpoints.
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
            'permissions': ['view_reports', 'view_dashboards']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample dashboard data for mocking
        self.dashboard_data = {
            'sales_summary': {
                'today': {
                    'total_sales': '25000.00',
                    'total_invoices': 35,
                    'average_sale': '714.29'
                },
                'yesterday': {
                    'total_sales': '22000.00',
                    'total_invoices': 30,
                    'average_sale': '733.33'
                },
                'this_week': {
                    'total_sales': '150000.00',
                    'total_invoices': 210,
                    'average_sale': '714.29'
                },
                'this_month': {
                    'total_sales': '600000.00',
                    'total_invoices': 840,
                    'average_sale': '714.29'
                }
            },
            'inventory_summary': {
                'total_products': 250,
                'total_variants': 350,
                'total_inventory_value': '2500000.00',
                'low_stock_items': 15,
                'expiring_items': 8,
                'out_of_stock_items': 5
            },
            'top_selling_products': [
                {
                    'product_id': str(uuid.uuid4()),
                    'product_name': 'Johnnie Walker Black Label',
                    'variant_name': '750ml',
                    'quantity_sold': 85,
                    'total_sales': '85000.00'
                },
                {
                    'product_id': str(uuid.uuid4()),
                    'product_name': 'Johnnie Walker Red Label',
                    'variant_name': '750ml',
                    'quantity_sold': 120,
                    'total_sales': '60000.00'
                },
                {
                    'product_id': str(uuid.uuid4()),
                    'product_name': 'Absolut Vodka',
                    'variant_name': '750ml',
                    'quantity_sold': 100,
                    'total_sales': '50000.00'
                },
                {
                    'product_id': str(uuid.uuid4()),
                    'product_name': 'Jack Daniels',
                    'variant_name': '750ml',
                    'quantity_sold': 75,
                    'total_sales': '45000.00'
                },
                {
                    'product_id': str(uuid.uuid4()),
                    'product_name': 'Bacardi White Rum',
                    'variant_name': '750ml',
                    'quantity_sold': 90,
                    'total_sales': '40500.00'
                }
            ],
            'sales_by_category': [
                {
                    'category_id': str(uuid.uuid4()),
                    'category_name': 'Whisky',
                    'total_sales': '190000.00',
                    'sales_percentage': '58.46'
                },
                {
                    'category_id': str(uuid.uuid4()),
                    'category_name': 'Vodka',
                    'total_sales': '50000.00',
                    'sales_percentage': '15.38'
                },
                {
                    'category_id': str(uuid.uuid4()),
                    'category_name': 'Rum',
                    'total_sales': '40500.00',
                    'sales_percentage': '12.46'
                },
                {
                    'category_id': str(uuid.uuid4()),
                    'category_name': 'Beer',
                    'total_sales': '25000.00',
                    'sales_percentage': '7.69'
                },
                {
                    'category_id': str(uuid.uuid4()),
                    'category_name': 'Wine',
                    'total_sales': '20000.00',
                    'sales_percentage': '6.15'
                }
            ],
            'recent_sales': [
                {
                    'invoice_number': 'INV-2023-0001',
                    'invoice_date': '2023-04-30T15:30:00Z',
                    'customer_name': 'John Doe',
                    'total_amount': '3500.00',
                    'payment_method': 'cash',
                    'status': 'completed'
                },
                {
                    'invoice_number': 'INV-2023-0002',
                    'invoice_date': '2023-04-30T16:15:00Z',
                    'customer_name': 'Jane Smith',
                    'total_amount': '2800.00',
                    'payment_method': 'card',
                    'status': 'completed'
                },
                {
                    'invoice_number': 'INV-2023-0003',
                    'invoice_date': '2023-04-30T17:00:00Z',
                    'customer_name': 'Bob Johnson',
                    'total_amount': '1500.00',
                    'payment_method': 'upi',
                    'status': 'completed'
                },
                {
                    'invoice_number': 'INV-2023-0004',
                    'invoice_date': '2023-04-30T17:45:00Z',
                    'customer_name': 'Alice Brown',
                    'total_amount': '4200.00',
                    'payment_method': 'cash',
                    'status': 'completed'
                },
                {
                    'invoice_number': 'INV-2023-0005',
                    'invoice_date': '2023-04-30T18:30:00Z',
                    'customer_name': 'Charlie Wilson',
                    'total_amount': '3000.00',
                    'payment_method': 'card',
                    'status': 'completed'
                }
            ],
            'pending_approvals': [
                {
                    'approval_number': 'APR-2023-0001',
                    'approval_date': '2023-04-30T14:30:00Z',
                    'approval_type': 'sale',
                    'reference_number': 'INV-2023-0006',
                    'requested_by': 'Jane Smith',
                    'priority': 'high'
                },
                {
                    'approval_number': 'APR-2023-0002',
                    'approval_date': '2023-04-30T15:45:00Z',
                    'approval_type': 'discount',
                    'reference_number': 'INV-2023-0007',
                    'requested_by': 'Bob Johnson',
                    'priority': 'medium'
                },
                {
                    'approval_number': 'APR-2023-0003',
                    'approval_date': '2023-04-30T16:30:00Z',
                    'approval_type': 'return',
                    'reference_number': 'RET-2023-0001',
                    'requested_by': 'Alice Brown',
                    'priority': 'medium'
                }
            ]
        }
        
        # Sample sales trend data for mocking
        self.sales_trend_data = [
            {'date': '2023-04-24', 'total_sales': '20000.00'},
            {'date': '2023-04-25', 'total_sales': '22000.00'},
            {'date': '2023-04-26', 'total_sales': '21000.00'},
            {'date': '2023-04-27', 'total_sales': '23000.00'},
            {'date': '2023-04-28', 'total_sales': '24000.00'},
            {'date': '2023-04-29', 'total_sales': '25000.00'},
            {'date': '2023-04-30', 'total_sales': '25000.00'}
        ]
        
        # Sample hourly sales data for mocking
        self.hourly_sales_data = [
            {'hour': '09:00', 'total_sales': '1500.00'},
            {'hour': '10:00', 'total_sales': '2000.00'},
            {'hour': '11:00', 'total_sales': '2500.00'},
            {'hour': '12:00', 'total_sales': '3000.00'},
            {'hour': '13:00', 'total_sales': '2800.00'},
            {'hour': '14:00', 'total_sales': '2500.00'},
            {'hour': '15:00', 'total_sales': '2200.00'},
            {'hour': '16:00', 'total_sales': '2000.00'},
            {'hour': '17:00', 'total_sales': '2300.00'},
            {'hour': '18:00', 'total_sales': '2700.00'},
            {'hour': '19:00', 'total_sales': '3000.00'},
            {'hour': '20:00', 'total_sales': '3200.00'},
            {'hour': '21:00', 'total_sales': '2800.00'}
        ]
        
        # Sample payment method distribution data for mocking
        self.payment_method_data = [
            {'payment_method': 'cash', 'total_sales': '150000.00', 'percentage': '50.00'},
            {'payment_method': 'card', 'total_sales': '90000.00', 'percentage': '30.00'},
            {'payment_method': 'upi', 'total_sales': '45000.00', 'percentage': '15.00'},
            {'payment_method': 'credit', 'total_sales': '15000.00', 'percentage': '5.00'}
        ]
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_dashboard_data(self, mock_get_data):
        """
        Test getting dashboard data.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.dashboard_data
        
        url = reverse('dashboard-data')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['sales_summary']['today']['total_sales'], '25000.00')
        self.assertEqual(response.data['data']['inventory_summary']['total_products'], 250)
        self.assertEqual(len(response.data['data']['top_selling_products']), 5)
        self.assertEqual(len(response.data['data']['sales_by_category']), 5)
        self.assertEqual(len(response.data['data']['recent_sales']), 5)
        self.assertEqual(len(response.data['data']['pending_approvals']), 3)
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/main/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_trend_data(self, mock_get_data):
        """
        Test getting sales trend data.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_trend_data
        
        url = reverse('sales-trend-data')
        params = {
            'shop_id': str(self.shop_id),
            'period': 'week'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 7)
        self.assertEqual(response.data['data'][0]['date'], '2023-04-24')
        self.assertEqual(response.data['data'][0]['total_sales'], '20000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/sales-trend/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'period': 'week'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_trend_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating sales trend chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_trend_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/sales_trend.png'
        
        url = reverse('sales-trend-chart')
        params = {
            'shop_id': str(self.shop_id),
            'period': 'week',
            'chart_type': 'line'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/sales_trend.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/sales-trend/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'period': 'week'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=self.sales_trend_data,
            chart_type='line',
            x_column='date',
            y_column='total_sales',
            title='Sales Trend - Last 7 Days',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_hourly_sales_data(self, mock_get_data):
        """
        Test getting hourly sales data.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.hourly_sales_data
        
        url = reverse('hourly-sales-data')
        params = {
            'shop_id': str(self.shop_id),
            'date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 13)
        self.assertEqual(response.data['data'][0]['hour'], '09:00')
        self.assertEqual(response.data['data'][0]['total_sales'], '1500.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/hourly-sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'date': '2023-04-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_hourly_sales_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating hourly sales chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.hourly_sales_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/hourly_sales.png'
        
        url = reverse('hourly-sales-chart')
        params = {
            'shop_id': str(self.shop_id),
            'date': '2023-04-30',
            'chart_type': 'bar'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/hourly_sales.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/hourly-sales/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'date': '2023-04-30'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=self.hourly_sales_data,
            chart_type='bar',
            x_column='hour',
            y_column='total_sales',
            title='Hourly Sales - 2023-04-30',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_payment_method_data(self, mock_get_data):
        """
        Test getting payment method distribution data.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.payment_method_data
        
        url = reverse('payment-method-data')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 4)
        self.assertEqual(response.data['data'][0]['payment_method'], 'cash')
        self.assertEqual(response.data['data'][0]['total_sales'], '150000.00')
        self.assertEqual(response.data['data'][0]['percentage'], '50.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/payment-methods/',
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
    def test_payment_method_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating payment method distribution chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.payment_method_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/payment_methods.png'
        
        url = reverse('payment-method-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-04-01',
            'end_date': '2023-04-30',
            'chart_type': 'pie'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/payment_methods.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/dashboards/payment-methods/',
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
            data=self.payment_method_data,
            chart_type='pie',
            x_column='payment_method',
            y_column='total_sales',
            title='Payment Method Distribution',
            filename=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to dashboards.
        """
        # Create a user without dashboard permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': ['view_reports']  # Has view_reports but not view_dashboards
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('dashboard-data')
        params = {
            'shop_id': str(self.shop_id)
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
        
        url = reverse('dashboard-data')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve dashboard data from service')