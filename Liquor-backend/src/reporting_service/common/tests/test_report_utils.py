import os
import json
import unittest
import pandas as pd
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock, mock_open
from django.test import TestCase
from django.conf import settings
from common.utils.report_utils import (
    generate_excel_report, generate_csv_report,
    generate_chart, get_report_data_from_service
)

class ReportUtilsTest(TestCase):
    """
    Test the report utilities.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.test_data = [
            {'id': 1, 'name': 'Product 1', 'price': 10.0},
            {'id': 2, 'name': 'Product 2', 'price': 20.0},
            {'id': 3, 'name': 'Product 3', 'price': 30.0}
        ]
        
        # Create a temporary directory for test files
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'reports', 'charts'), exist_ok=True)
    
    @patch('common.utils.report_utils.pd.ExcelWriter')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_excel_report_list(self, mock_dataframe, mock_excel_writer):
        """
        Test generate_excel_report function with list data.
        """
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Mock the ExcelWriter
        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Call the function
        result = generate_excel_report(self.test_data, sheet_names=['Products'])
        
        # Assertions
        self.assertIsNotNone(result)
        mock_dataframe.assert_called_once_with(self.test_data)
        mock_df.to_excel.assert_called_once_with(mock_writer, sheet_name='Products', index=False)
    
    @patch('common.utils.report_utils.pd.ExcelWriter')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_excel_report_dict(self, mock_dataframe, mock_excel_writer):
        """
        Test generate_excel_report function with dict data.
        """
        # Test data as dict
        test_data_dict = {
            'Products': self.test_data,
            'Categories': [
                {'id': 1, 'name': 'Category 1'},
                {'id': 2, 'name': 'Category 2'}
            ]
        }
        
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Mock the ExcelWriter
        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Call the function
        result = generate_excel_report(test_data_dict)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(mock_dataframe.call_count, 2)
        self.assertEqual(mock_df.to_excel.call_count, 2)
    
    @patch('common.utils.report_utils.pd.ExcelWriter')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_excel_report_exception(self, mock_dataframe, mock_excel_writer):
        """
        Test generate_excel_report function with exception.
        """
        # Mock the DataFrame to raise an exception
        mock_dataframe.side_effect = Exception('DataFrame error')
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            result = generate_excel_report(self.test_data)
        
        # Assertions
        self.assertIsNone(result)
        self.assertIn('Error generating Excel report: DataFrame error', cm.output[0])
    
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_csv_report(self, mock_dataframe):
        """
        Test generate_csv_report function.
        """
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Call the function
        result = generate_csv_report(self.test_data)
        
        # Assertions
        self.assertIsNotNone(result)
        mock_dataframe.assert_called_once_with(self.test_data)
        mock_df.to_csv.assert_called_once()
    
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_csv_report_exception(self, mock_dataframe):
        """
        Test generate_csv_report function with exception.
        """
        # Mock the DataFrame to raise an exception
        mock_dataframe.side_effect = Exception('DataFrame error')
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            result = generate_csv_report(self.test_data)
        
        # Assertions
        self.assertIsNone(result)
        self.assertIn('Error generating CSV report: DataFrame error', cm.output[0])
    
    @patch('common.utils.report_utils.plt.figure')
    @patch('common.utils.report_utils.plt.savefig')
    @patch('common.utils.report_utils.plt.close')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_chart_bar(self, mock_dataframe, mock_close, mock_savefig, mock_figure):
        """
        Test generate_chart function with bar chart.
        """
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_df.plot.return_value = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Call the function
        result = generate_chart(
            self.test_data,
            chart_type='bar',
            x_column='name',
            y_column='price',
            title='Product Prices'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        mock_dataframe.assert_called_once_with(self.test_data)
        mock_df.plot.assert_called_once_with(kind='bar', x='name', y='price')
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('common.utils.report_utils.plt.figure')
    @patch('common.utils.report_utils.plt.savefig')
    @patch('common.utils.report_utils.plt.close')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_chart_line(self, mock_dataframe, mock_close, mock_savefig, mock_figure):
        """
        Test generate_chart function with line chart.
        """
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_df.plot.return_value = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Call the function
        result = generate_chart(
            self.test_data,
            chart_type='line',
            x_column='name',
            y_column='price',
            title='Product Prices'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        mock_dataframe.assert_called_once_with(self.test_data)
        mock_df.plot.assert_called_once_with(kind='line', x='name', y='price')
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('common.utils.report_utils.plt.figure')
    @patch('common.utils.report_utils.plt.savefig')
    @patch('common.utils.report_utils.plt.close')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_chart_pie(self, mock_dataframe, mock_close, mock_savefig, mock_figure):
        """
        Test generate_chart function with pie chart.
        """
        # Mock the DataFrame
        mock_df = MagicMock()
        mock_df.plot.return_value = MagicMock()
        mock_dataframe.return_value = mock_df
        
        # Call the function
        result = generate_chart(
            self.test_data,
            chart_type='pie',
            x_column='name',
            y_column='price',
            title='Product Prices'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        mock_dataframe.assert_called_once_with(self.test_data)
        mock_df.plot.assert_called_once_with(kind='pie', y='price')
        mock_savefig.assert_called_once()
        mock_close.assert_called_once()
    
    @patch('common.utils.report_utils.plt.figure')
    @patch('common.utils.report_utils.plt.savefig')
    @patch('common.utils.report_utils.plt.close')
    @patch('common.utils.report_utils.pd.DataFrame')
    def test_generate_chart_exception(self, mock_dataframe, mock_close, mock_savefig, mock_figure):
        """
        Test generate_chart function with exception.
        """
        # Mock the DataFrame to raise an exception
        mock_dataframe.side_effect = Exception('DataFrame error')
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            result = generate_chart(
                self.test_data,
                chart_type='bar',
                x_column='name',
                y_column='price'
            )
        
        # Assertions
        self.assertIsNone(result)
        self.assertIn('Error generating chart: DataFrame error', cm.output[0])
    
    @patch('requests.get')
    def test_get_report_data_from_service(self, mock_get):
        """
        Test get_report_data_from_service function.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.test_data
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_report_data_from_service(
            'http://example.com',
            '/api/products/',
            params={'category': 'test'},
            headers={'Authorization': 'Bearer token'}
        )
        
        # Assertions
        self.assertEqual(result, self.test_data)
        mock_get.assert_called_once_with(
            'http://example.com/api/products/',
            params={'category': 'test'},
            headers={'Authorization': 'Bearer token'}
        )
    
    @patch('requests.get')
    def test_get_report_data_from_service_http_error(self, mock_get):
        """
        Test get_report_data_from_service function with HTTP error.
        """
        # Mock the response to raise an HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception('HTTP error')
        mock_get.return_value = mock_response
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            result = get_report_data_from_service(
                'http://example.com',
                '/api/products/'
            )
        
        # Assertions
        self.assertIsNone(result)
        self.assertIn('Error getting report data from service: HTTP error', cm.output[0])
    
    @patch('requests.get')
    def test_get_report_data_from_service_exception(self, mock_get):
        """
        Test get_report_data_from_service function with exception.
        """
        # Mock the get method to raise an exception
        mock_get.side_effect = Exception('Connection error')
        
        # Call the function
        with self.assertLogs(level='ERROR') as cm:
            result = get_report_data_from_service(
                'http://example.com',
                '/api/products/'
            )
        
        # Assertions
        self.assertIsNone(result)
        self.assertIn('Error getting report data from service: Connection error', cm.output[0])