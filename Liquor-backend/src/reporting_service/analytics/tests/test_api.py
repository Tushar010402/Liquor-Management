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

class AnalyticsAPITest(TestCase):
    """
    Test the analytics API endpoints.
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
            'permissions': ['view_reports', 'view_analytics']
        })
        
        # Mock the authentication
        self.client.force_authenticate(user=self.user)
        
        # Sample sales forecast data for mocking
        self.sales_forecast_data = {
            'historical': [
                {'date': '2023-01-01', 'total_sales': '20000.00'},
                {'date': '2023-02-01', 'total_sales': '22000.00'},
                {'date': '2023-03-01', 'total_sales': '24000.00'},
                {'date': '2023-04-01', 'total_sales': '25000.00'},
                {'date': '2023-05-01', 'total_sales': '26000.00'},
                {'date': '2023-06-01', 'total_sales': '27000.00'}
            ],
            'forecast': [
                {'date': '2023-07-01', 'total_sales': '28000.00', 'lower_bound': '26000.00', 'upper_bound': '30000.00'},
                {'date': '2023-08-01', 'total_sales': '29000.00', 'lower_bound': '27000.00', 'upper_bound': '31000.00'},
                {'date': '2023-09-01', 'total_sales': '30000.00', 'lower_bound': '28000.00', 'upper_bound': '32000.00'}
            ],
            'accuracy': {
                'mape': '5.2',
                'rmse': '1200.00'
            }
        }
        
        # Sample customer segmentation data for mocking
        self.customer_segmentation_data = {
            'segments': [
                {
                    'segment': 'High Value',
                    'count': 120,
                    'percentage': '12.00',
                    'avg_purchase_value': '5000.00',
                    'avg_purchase_frequency': '2.5',
                    'total_revenue': '1500000.00',
                    'revenue_percentage': '30.00'
                },
                {
                    'segment': 'Regular',
                    'count': 350,
                    'percentage': '35.00',
                    'avg_purchase_value': '2000.00',
                    'avg_purchase_frequency': '1.8',
                    'total_revenue': '1260000.00',
                    'revenue_percentage': '25.20'
                },
                {
                    'segment': 'Occasional',
                    'count': 450,
                    'percentage': '45.00',
                    'avg_purchase_value': '1500.00',
                    'avg_purchase_frequency': '1.2',
                    'total_revenue': '810000.00',
                    'revenue_percentage': '16.20'
                },
                {
                    'segment': 'New',
                    'count': 80,
                    'percentage': '8.00',
                    'avg_purchase_value': '1800.00',
                    'avg_purchase_frequency': '1.0',
                    'total_revenue': '144000.00',
                    'revenue_percentage': '2.88'
                }
            ],
            'total_customers': 1000,
            'total_revenue': '5000000.00'
        }
        
        # Sample product recommendation data for mocking
        self.product_recommendation_data = [
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'recommended_products': [
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Chivas Regal 12 Year',
                        'variant_name': '750ml',
                        'confidence': '0.85'
                    },
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Jack Daniels',
                        'variant_name': '750ml',
                        'confidence': '0.75'
                    },
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Glenfiddich 12 Year',
                        'variant_name': '750ml',
                        'confidence': '0.70'
                    }
                ]
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'recommended_products': [
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Smirnoff Vodka',
                        'variant_name': '750ml',
                        'confidence': '0.90'
                    },
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Grey Goose Vodka',
                        'variant_name': '750ml',
                        'confidence': '0.80'
                    },
                    {
                        'product_id': str(uuid.uuid4()),
                        'product_name': 'Belvedere Vodka',
                        'variant_name': '750ml',
                        'confidence': '0.75'
                    }
                ]
            }
        ]
        
        # Sample inventory optimization data for mocking
        self.inventory_optimization_data = [
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'current_stock': 25,
                'recommended_stock': 30,
                'reorder_point': 10,
                'reorder_quantity': 20,
                'lead_time_days': 5,
                'safety_stock': 5,
                'stock_status': 'adequate'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Red Label',
                'variant_name': '750ml',
                'current_stock': 8,
                'recommended_stock': 25,
                'reorder_point': 10,
                'reorder_quantity': 20,
                'lead_time_days': 5,
                'safety_stock': 5,
                'stock_status': 'low'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'current_stock': 35,
                'recommended_stock': 25,
                'reorder_point': 10,
                'reorder_quantity': 15,
                'lead_time_days': 4,
                'safety_stock': 5,
                'stock_status': 'excess'
            }
        ]
        
        # Sample price optimization data for mocking
        self.price_optimization_data = [
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'current_price': '5000.00',
                'recommended_price': '5200.00',
                'min_price': '4500.00',
                'max_price': '5500.00',
                'price_elasticity': '-1.2',
                'expected_sales_change': '-4.80',
                'expected_revenue_change': '+3.20'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Red Label',
                'variant_name': '750ml',
                'current_price': '3000.00',
                'recommended_price': '2800.00',
                'min_price': '2500.00',
                'max_price': '3200.00',
                'price_elasticity': '-1.5',
                'expected_sales_change': '+10.00',
                'expected_revenue_change': '+3.33'
            },
            {
                'product_id': str(uuid.uuid4()),
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'current_price': '2500.00',
                'recommended_price': '2600.00',
                'min_price': '2200.00',
                'max_price': '2800.00',
                'price_elasticity': '-1.3',
                'expected_sales_change': '-5.20',
                'expected_revenue_change': '+3.64'
            }
        ]
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_forecast(self, mock_get_data):
        """
        Test getting sales forecast.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_forecast_data
        
        url = reverse('sales-forecast')
        params = {
            'shop_id': str(self.shop_id),
            'months': 3
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['historical']), 6)
        self.assertEqual(len(response.data['data']['forecast']), 3)
        self.assertEqual(response.data['data']['forecast'][0]['total_sales'], '28000.00')
        self.assertEqual(response.data['data']['forecast'][0]['lower_bound'], '26000.00')
        self.assertEqual(response.data['data']['forecast'][0]['upper_bound'], '30000.00')
        self.assertEqual(response.data['data']['accuracy']['mape'], '5.2')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/sales-forecast/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'months': 3
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_sales_forecast_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating sales forecast chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.sales_forecast_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/sales_forecast.png'
        
        url = reverse('sales-forecast-chart')
        params = {
            'shop_id': str(self.shop_id),
            'months': 3,
            'chart_type': 'line'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/sales_forecast.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/sales-forecast/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'months': 3
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_customer_segmentation(self, mock_get_data):
        """
        Test getting customer segmentation.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.customer_segmentation_data
        
        url = reverse('customer-segmentation')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-06-30'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['segments']), 4)
        self.assertEqual(response.data['data']['segments'][0]['segment'], 'High Value')
        self.assertEqual(response.data['data']['segments'][0]['count'], 120)
        self.assertEqual(response.data['data']['segments'][0]['percentage'], '12.00')
        self.assertEqual(response.data['data']['segments'][0]['avg_purchase_value'], '5000.00')
        self.assertEqual(response.data['data']['total_customers'], 1000)
        self.assertEqual(response.data['data']['total_revenue'], '5000000.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/customer-segmentation/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-06-30'
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_customer_segmentation_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating customer segmentation chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.customer_segmentation_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/customer_segmentation.png'
        
        url = reverse('customer-segmentation-chart')
        params = {
            'shop_id': str(self.shop_id),
            'start_date': '2023-01-01',
            'end_date': '2023-06-30',
            'chart_type': 'pie',
            'metric': 'count'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/customer_segmentation.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/customer-segmentation/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'start_date': '2023-01-01',
                'end_date': '2023-06-30'
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once()
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_product_recommendations(self, mock_get_data):
        """
        Test getting product recommendations.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.product_recommendation_data
        
        url = reverse('product-recommendations')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(len(response.data['data'][0]['recommended_products']), 3)
        self.assertEqual(response.data['data'][0]['recommended_products'][0]['product_name'], 'Chivas Regal 12 Year')
        self.assertEqual(response.data['data'][0]['recommended_products'][0]['confidence'], '0.85')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/product-recommendations/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_inventory_optimization(self, mock_get_data):
        """
        Test getting inventory optimization.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.inventory_optimization_data
        
        url = reverse('inventory-optimization')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['current_stock'], 25)
        self.assertEqual(response.data['data'][0]['recommended_stock'], 30)
        self.assertEqual(response.data['data'][0]['stock_status'], 'adequate')
        self.assertEqual(response.data['data'][1]['stock_status'], 'low')
        self.assertEqual(response.data['data'][2]['stock_status'], 'excess')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/inventory-optimization/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_price_optimization(self, mock_get_data):
        """
        Test getting price optimization.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.price_optimization_data
        
        url = reverse('price-optimization')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['current_price'], '5000.00')
        self.assertEqual(response.data['data'][0]['recommended_price'], '5200.00')
        self.assertEqual(response.data['data'][0]['expected_revenue_change'], '+3.20')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/analytics/price-optimization/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    def test_unauthorized_access(self):
        """
        Test unauthorized access to analytics.
        """
        # Create a user without analytics permissions
        user_without_permissions = MicroserviceUser({
            'id': str(uuid.uuid4()),
            'email': 'nopermissions@example.com',
            'tenant_id': str(self.tenant_id),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'executive',
            'permissions': ['view_reports']  # Has view_reports but not view_analytics
        })
        
        # Set up client with the new user
        client = APIClient()
        client.force_authenticate(user=user_without_permissions)
        
        url = reverse('sales-forecast')
        params = {
            'shop_id': str(self.shop_id),
            'months': 3
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
        
        url = reverse('sales-forecast')
        params = {
            'shop_id': str(self.shop_id),
            'months': 3
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve analytics data from service')