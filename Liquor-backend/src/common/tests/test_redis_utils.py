import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from common.utils.redis_utils import (
    cache_get, cache_set, cache_delete,
    cache_get_json, cache_set_json
)

class RedisUtilsTest(TestCase):
    """
    Test the Redis utilities.
    """
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get(self, mock_cache):
        """
        Test cache_get function.
        """
        # Mock the cache
        mock_cache.get.return_value = 'test_value'
        
        # Call the function
        result = cache_get('test_key')
        
        # Assertions
        self.assertEqual(result, 'test_value')
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get_default(self, mock_cache):
        """
        Test cache_get function with default value.
        """
        # Mock the cache to return None
        mock_cache.get.return_value = None
        
        # Call the function
        result = cache_get('test_key', default='default_value')
        
        # Assertions
        self.assertEqual(result, 'default_value')
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get_exception(self, mock_cache):
        """
        Test cache_get function with exception.
        """
        # Mock the cache to raise an exception
        mock_cache.get.side_effect = Exception('Cache error')
        
        # Call the function
        result = cache_get('test_key', default='default_value')
        
        # Assertions
        self.assertEqual(result, 'default_value')
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set(self, mock_cache):
        """
        Test cache_set function.
        """
        # Call the function
        result = cache_set('test_key', 'test_value')
        
        # Assertions
        self.assertTrue(result)
        mock_cache.set.assert_called_once_with('test_key', 'test_value', timeout=None)
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set_with_timeout(self, mock_cache):
        """
        Test cache_set function with timeout.
        """
        # Call the function
        result = cache_set('test_key', 'test_value', timeout=60)
        
        # Assertions
        self.assertTrue(result)
        mock_cache.set.assert_called_once_with('test_key', 'test_value', timeout=60)
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set_exception(self, mock_cache):
        """
        Test cache_set function with exception.
        """
        # Mock the cache to raise an exception
        mock_cache.set.side_effect = Exception('Cache error')
        
        # Call the function
        result = cache_set('test_key', 'test_value')
        
        # Assertions
        self.assertFalse(result)
        mock_cache.set.assert_called_once_with('test_key', 'test_value', timeout=None)
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_delete(self, mock_cache):
        """
        Test cache_delete function.
        """
        # Call the function
        result = cache_delete('test_key')
        
        # Assertions
        self.assertTrue(result)
        mock_cache.delete.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_delete_exception(self, mock_cache):
        """
        Test cache_delete function with exception.
        """
        # Mock the cache to raise an exception
        mock_cache.delete.side_effect = Exception('Cache error')
        
        # Call the function
        result = cache_delete('test_key')
        
        # Assertions
        self.assertFalse(result)
        mock_cache.delete.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get_json(self, mock_cache):
        """
        Test cache_get_json function.
        """
        # Mock the cache
        mock_cache.get.return_value = json.dumps({'key': 'value'})
        
        # Call the function
        result = cache_get_json('test_key')
        
        # Assertions
        self.assertEqual(result, {'key': 'value'})
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get_json_none(self, mock_cache):
        """
        Test cache_get_json function with None value.
        """
        # Mock the cache to return None
        mock_cache.get.return_value = None
        
        # Call the function
        result = cache_get_json('test_key', default={'default': 'value'})
        
        # Assertions
        self.assertEqual(result, {'default': 'value'})
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_get_json_exception(self, mock_cache):
        """
        Test cache_get_json function with exception.
        """
        # Mock the cache to return invalid JSON
        mock_cache.get.return_value = 'invalid json'
        
        # Call the function
        result = cache_get_json('test_key', default={'default': 'value'})
        
        # Assertions
        self.assertEqual(result, {'default': 'value'})
        mock_cache.get.assert_called_once_with('test_key')
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set_json(self, mock_cache):
        """
        Test cache_set_json function.
        """
        # Call the function
        result = cache_set_json('test_key', {'key': 'value'})
        
        # Assertions
        self.assertTrue(result)
        mock_cache.set.assert_called_once_with('test_key', json.dumps({'key': 'value'}), timeout=None)
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set_json_with_timeout(self, mock_cache):
        """
        Test cache_set_json function with timeout.
        """
        # Call the function
        result = cache_set_json('test_key', {'key': 'value'}, timeout=60)
        
        # Assertions
        self.assertTrue(result)
        mock_cache.set.assert_called_once_with('test_key', json.dumps({'key': 'value'}), timeout=60)
    
    @patch('common.utils.redis_utils.cache')
    def test_cache_set_json_exception(self, mock_cache):
        """
        Test cache_set_json function with exception.
        """
        # Mock the cache to raise an exception
        mock_cache.set.side_effect = Exception('Cache error')
        
        # Call the function
        result = cache_set_json('test_key', {'key': 'value'})
        
        # Assertions
        self.assertFalse(result)
        mock_cache.set.assert_called_once()