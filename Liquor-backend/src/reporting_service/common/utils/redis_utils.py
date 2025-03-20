import json
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

def cache_get(key, default=None):
    """
    Get a value from the cache.
    
    Args:
        key (str): Cache key.
        default: Default value to return if key is not found.
        
    Returns:
        The cached value or default.
    """
    try:
        value = cache.get(key)
        return value if value is not None else default
    except Exception as e:
        logger.error(f"Error getting value from cache: {str(e)}")
        return default

def cache_set(key, value, timeout=None):
    """
    Set a value in the cache.
    
    Args:
        key (str): Cache key.
        value: Value to cache.
        timeout (int, optional): Cache timeout in seconds.
        
    Returns:
        bool: True if successful, False otherwise.
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
        key (str): Cache key.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        cache.delete(key)
        return True
    except Exception as e:
        logger.error(f"Error deleting value from cache: {str(e)}")
        return False

def cache_get_json(key, default=None):
    """
    Get a JSON value from the cache.
    
    Args:
        key (str): Cache key.
        default: Default value to return if key is not found.
        
    Returns:
        The cached JSON value or default.
    """
    try:
        value = cache.get(key)
        if value is not None:
            return json.loads(value)
        return default
    except Exception as e:
        logger.error(f"Error getting JSON value from cache: {str(e)}")
        return default

def cache_set_json(key, value, timeout=None):
    """
    Set a JSON value in the cache.
    
    Args:
        key (str): Cache key.
        value: Value to cache.
        timeout (int, optional): Cache timeout in seconds.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        cache.set(key, json.dumps(value), timeout=timeout)
        return True
    except Exception as e:
        logger.error(f"Error setting JSON value in cache: {str(e)}")
        return False