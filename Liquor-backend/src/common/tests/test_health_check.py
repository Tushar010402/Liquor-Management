import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from common.views import HealthCheckView

class HealthCheckTest(TestCase):
    """
    Test the health check endpoint.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.url = reverse('health-check')
    
    @patch('common.views.connection')
    @patch('common.views.cache')
    def test_health_check_healthy(self, mock_cache, mock_connection):
        """
        Test health check when all systems are healthy.
        """
        # Mock the database connection
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock the cache
        mock_cache.set.return_value = True
        mock_cache.get.return_value = 'ok'
        
        # Make the request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertEqual(response.data['checks']['database'], 'ok')
        self.assertEqual(response.data['checks']['cache'], 'ok')
    
    @patch('common.views.connection')
    @patch('common.views.cache')
    def test_health_check_database_unhealthy(self, mock_cache, mock_connection):
        """
        Test health check when database is unhealthy.
        """
        # Mock the database connection to raise an exception
        mock_connection.cursor.return_value.__enter__.side_effect = Exception('Database error')
        
        # Mock the cache
        mock_cache.set.return_value = True
        mock_cache.get.return_value = 'ok'
        
        # Make the request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'unhealthy')
        self.assertEqual(response.data['checks']['database'], 'error: Database error')
        self.assertEqual(response.data['checks']['cache'], 'ok')
    
    @patch('common.views.connection')
    @patch('common.views.cache')
    def test_health_check_cache_unhealthy(self, mock_cache, mock_connection):
        """
        Test health check when cache is unhealthy.
        """
        # Mock the database connection
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock the cache to raise an exception
        mock_cache.set.side_effect = Exception('Cache error')
        
        # Make the request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'unhealthy')
        self.assertEqual(response.data['checks']['database'], 'ok')
        self.assertEqual(response.data['checks']['cache'], 'error: Cache error')
    
    @patch('common.views.connection')
    @patch('common.views.cache')
    def test_health_check_cache_value_mismatch(self, mock_cache, mock_connection):
        """
        Test health check when cache value doesn't match.
        """
        # Mock the database connection
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value = None
        mock_cursor.fetchone.return_value = (1,)
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Mock the cache with wrong value
        mock_cache.set.return_value = True
        mock_cache.get.return_value = 'not_ok'
        
        # Make the request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'unhealthy')
        self.assertEqual(response.data['checks']['database'], 'ok')
        self.assertEqual(response.data['checks']['cache'], 'error: cache value mismatch')
    
    @patch('common.views.connection')
    @patch('common.views.cache')
    def test_health_check_all_unhealthy(self, mock_cache, mock_connection):
        """
        Test health check when all systems are unhealthy.
        """
        # Mock the database connection to raise an exception
        mock_connection.cursor.return_value.__enter__.side_effect = Exception('Database error')
        
        # Mock the cache to raise an exception
        mock_cache.set.side_effect = Exception('Cache error')
        
        # Make the request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['status'], 'unhealthy')
        self.assertEqual(response.data['checks']['database'], 'error: Database error')
        self.assertEqual(response.data['checks']['cache'], 'error: Cache error')