import json
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

def cache_get(key, default=None):
    """
    Get a value from the cache.
    
    Args:
        key (str): Cache key
        default: Default value if key not found
        
    Returns:
        The cached value or default
    """
    try:
        value = cache.get(key, default)
        return value
    except Exception as e:
        logger.error(f"Error getting value from cache: {str(e)}")
        return default

def cache_set(key, value, timeout=None):
    """
    Set a value in the cache.
    
    Args:
        key (str): Cache key
        value: Value to cache
        timeout (int): Cache timeout in seconds (None for default)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cache.set(key, value, timeout=timeout)
        return True
    except Exception as e:
        logger.error(f"Error setting value in cache: {str(e)}")
        return False

def cache_delete(key):
    """
    Delete a value from the cache.
    
    Args:
        key (str): Cache key
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cache.delete(key)
        return True
    except Exception as e:
        logger.error(f"Error deleting value from cache: {str(e)}")
        return False

def cache_get_json(key, default=None):
    """
    Get a JSON value from the cache and deserialize it.
    
    Args:
        key (str): Cache key
        default: Default value if key not found
        
    Returns:
        The deserialized JSON value or default
    """
    try:
        value = cache.get(key)
        if value is None:
            return default
        return json.loads(value)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in cache for key: {key}")
        return default
    except Exception as e:
        logger.error(f"Error getting JSON value from cache: {str(e)}")
        return default

def cache_set_json(key, value, timeout=None):
    """
    Serialize a value to JSON and set it in the cache.
    
    Args:
        key (str): Cache key
        value: Value to serialize and cache
        timeout (int): Cache timeout in seconds (None for default)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        json_value = json.dumps(value)
        cache.set(key, json_value, timeout=timeout)
        return True
    except Exception as e:
        logger.error(f"Error setting JSON value in cache: {str(e)}")
        return False