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

class InventoryReportsAPITest(TestCase):
    """
    Test the inventory reports API endpoints.
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
        
        # Sample inventory data for mocking
        self.inventory_data = [
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'current_stock': 25,
                'reorder_level': 10,
                'unit_cost': '3500.00',
                'total_value': '87500.00'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Red Label',
                'variant_name': '750ml',
                'current_stock': 15,
                'reorder_level': 8,
                'unit_cost': '1500.00',
                'total_value': '22500.00'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Absolut Vodka',
                'variant_name': '750ml',
                'current_stock': 30,
                'reorder_level': 12,
                'unit_cost': '800.00',
                'total_value': '24000.00'
            }
        ]
        
        # Sample low stock data for mocking
        self.low_stock_data = [
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Jack Daniels',
                'variant_name': '750ml',
                'current_stock': 5,
                'reorder_level': 10,
                'unit_cost': '2800.00',
                'total_value': '14000.00'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Chivas Regal',
                'variant_name': '750ml',
                'current_stock': 3,
                'reorder_level': 8,
                'unit_cost': '3200.00',
                'total_value': '9600.00'
            }
        ]
        
        # Sample expiring stock data for mocking
        self.expiring_stock_data = [
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Corona Beer',
                'variant_name': '330ml',
                'batch_number': 'B12345',
                'current_stock': 48,
                'expiry_date': (date.today() + timedelta(days=15)).isoformat(),
                'unit_cost': '120.00',
                'total_value': '5760.00'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Heineken Beer',
                'variant_name': '330ml',
                'batch_number': 'B23456',
                'current_stock': 36,
                'expiry_date': (date.today() + timedelta(days=20)).isoformat(),
                'unit_cost': '130.00',
                'total_value': '4680.00'
            }
        ]
        
        # Sample stock movement data for mocking
        self.stock_movement_data = [
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'movement_type': 'purchase',
                'quantity': 10,
                'date': (date.today() - timedelta(days=5)).isoformat(),
                'reference': 'PO-2023-0001',
                'notes': 'Regular purchase'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'movement_type': 'sale',
                'quantity': -3,
                'date': (date.today() - timedelta(days=3)).isoformat(),
                'reference': 'INV-2023-0001',
                'notes': 'Regular sale'
            },
            {
                'id': str(uuid.uuid4()),
                'product_name': 'Johnnie Walker Black Label',
                'variant_name': '750ml',
                'movement_type': 'adjustment',
                'quantity': -1,
                'date': (date.today() - timedelta(days=2)).isoformat(),
                'reference': 'ADJ-2023-0001',
                'notes': 'Damaged bottle'
            }
        ]
        
        # Sample inventory summary data for mocking
        self.inventory_summary_data = {
            'total_products': 25,
            'total_variants': 35,
            'total_inventory_value': '250000.00',
            'low_stock_items': 5,
            'expiring_items': 3,
            'out_of_stock_items': 2
        }
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_inventory_report(self, mock_get_data):
        """
        Test getting inventory report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.inventory_data
        
        url = reverse('inventory-report')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['current_stock'], 25)
        self.assertEqual(response.data['data'][0]['total_value'], '87500.00')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/stock/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_excel_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_inventory_report_excel(self, mock_get_data, mock_generate_excel):
        """
        Test exporting inventory report as Excel.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.inventory_data
        
        # Mock the generate_excel_report function
        mock_generate_excel.return_value = '/media/reports/inventory_report.xlsx'
        
        url = reverse('export-inventory-report')
        params = {
            'shop_id': str(self.shop_id),
            'format': 'excel'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/inventory_report.xlsx')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/stock/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
        
        # Check that the Excel report was generated
        mock_generate_excel.assert_called_once_with(
            data=self.inventory_data,
            sheet_names=['Inventory Report'],
            filename=any
        )
    
    @patch('common.utils.report_utils.generate_csv_report')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_export_inventory_report_csv(self, mock_get_data, mock_generate_csv):
        """
        Test exporting inventory report as CSV.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.inventory_data
        
        # Mock the generate_csv_report function
        mock_generate_csv.return_value = '/media/reports/inventory_report.csv'
        
        url = reverse('export-inventory-report')
        params = {
            'shop_id': str(self.shop_id),
            'format': 'csv'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_url'], '/media/reports/inventory_report.csv')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/stock/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
        
        # Check that the CSV report was generated
        mock_generate_csv.assert_called_once_with(
            data=self.inventory_data,
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_low_stock_report(self, mock_get_data):
        """
        Test getting low stock report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.low_stock_data
        
        url = reverse('low-stock-report')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['product_name'], 'Jack Daniels')
        self.assertEqual(response.data['data'][0]['current_stock'], 5)
        self.assertEqual(response.data['data'][0]['reorder_level'], 10)
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/low-stock/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_expiring_stock_report(self, mock_get_data):
        """
        Test getting expiring stock report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.expiring_stock_data
        
        url = reverse('expiring-stock-report')
        params = {
            'shop_id': str(self.shop_id),
            'days': 30
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
        self.assertEqual(response.data['data'][0]['product_name'], 'Corona Beer')
        self.assertEqual(response.data['data'][0]['current_stock'], 48)
        self.assertEqual(response.data['data'][0]['batch_number'], 'B12345')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/expiring-stock/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'days': 30
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_stock_movement_report(self, mock_get_data):
        """
        Test getting stock movement report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.stock_movement_data
        
        url = reverse('stock-movement-report')
        params = {
            'shop_id': str(self.shop_id),
            'product_id': str(uuid.uuid4()),
            'start_date': (date.today() - timedelta(days=7)).isoformat(),
            'end_date': date.today().isoformat()
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'][0]['product_name'], 'Johnnie Walker Black Label')
        self.assertEqual(response.data['data'][0]['movement_type'], 'purchase')
        self.assertEqual(response.data['data'][0]['quantity'], 10)
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/stock-movements/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'product_id': params['product_id'],
                'start_date': params['start_date'],
                'end_date': params['end_date']
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_stock_movement_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating stock movement chart.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.stock_movement_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/stock_movement.png'
        
        url = reverse('stock-movement-chart')
        params = {
            'shop_id': str(self.shop_id),
            'product_id': str(uuid.uuid4()),
            'start_date': (date.today() - timedelta(days=7)).isoformat(),
            'end_date': date.today().isoformat(),
            'chart_type': 'line'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/stock_movement.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/stock-movements/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id),
                'product_id': params['product_id'],
                'start_date': params['start_date'],
                'end_date': params['end_date']
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=self.stock_movement_data,
            chart_type='line',
            x_column='date',
            y_column='quantity',
            title='Stock Movement',
            filename=any
        )
    
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_inventory_summary_report(self, mock_get_data):
        """
        Test getting inventory summary report.
        """
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = self.inventory_summary_data
        
        url = reverse('inventory-summary-report')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['total_products'], 25)
        self.assertEqual(response.data['data']['total_variants'], 35)
        self.assertEqual(response.data['data']['total_inventory_value'], '250000.00')
        self.assertEqual(response.data['data']['low_stock_items'], 5)
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/summary/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
    
    @patch('common.utils.report_utils.generate_chart')
    @patch('common.utils.report_utils.get_report_data_from_service')
    def test_inventory_value_by_category_chart(self, mock_get_data, mock_generate_chart):
        """
        Test generating inventory value by category chart.
        """
        # Sample inventory by category data
        inventory_by_category_data = [
            {'category_name': 'Whisky', 'total_value': '150000.00'},
            {'category_name': 'Vodka', 'total_value': '50000.00'},
            {'category_name': 'Rum', 'total_value': '30000.00'},
            {'category_name': 'Beer', 'total_value': '20000.00'}
        ]
        
        # Mock the get_report_data_from_service function
        mock_get_data.return_value = inventory_by_category_data
        
        # Mock the generate_chart function
        mock_generate_chart.return_value = '/media/reports/charts/inventory_by_category.png'
        
        url = reverse('inventory-by-category-chart')
        params = {
            'shop_id': str(self.shop_id),
            'chart_type': 'pie'
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chart_url'], '/media/reports/charts/inventory_by_category.png')
        
        # Check that the service was called with the correct parameters
        mock_get_data.assert_called_once_with(
            service_url=any,
            endpoint='/api/inventory/by-category/',
            params={
                'tenant_id': str(self.tenant_id),
                'shop_id': str(self.shop_id)
            },
            headers=any
        )
        
        # Check that the chart was generated
        mock_generate_chart.assert_called_once_with(
            data=inventory_by_category_data,
            chart_type='pie',
            x_column='category_name',
            y_column='total_value',
            title='Inventory Value by Category',
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
        
        url = reverse('inventory-report')
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
        
        url = reverse('inventory-report')
        params = {
            'shop_id': str(self.shop_id)
        }
        response = self.client.get(url, params)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Failed to retrieve inventory data from service')