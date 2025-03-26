from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
import datetime
import logging

logger = logging.getLogger(__name__)

class HealthCheckView(APIView):
    """
    API endpoint for health check.
    """
    permission_classes = []
    
    def get(self, request, format=None):
        """
        Perform a health check.
        """
        # Check database connection
        db_status = "ok"
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception as e:
            db_status = f"error: {str(e)}"
            logger.error(f"Database health check failed: {str(e)}")
        
        # Check cache connection
        cache_status = "ok"
        try:
            cache.set('health_check', 'ok', 10)
            cache_value = cache.get('health_check')
            if cache_value != 'ok':
                cache_status = "error: cache value mismatch"
        except Exception as e:
            cache_status = f"error: {str(e)}"
            logger.error(f"Cache health check failed: {str(e)}")
        
        # Build response
        health_data = {
            'status': 'healthy' if db_status == 'ok' and cache_status == 'ok' else 'unhealthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'service': 'purchase-service',
            'checks': {
                'database': db_status,
                'cache': cache_status
            }
        }
        
        status_code = status.HTTP_200_OK if health_data['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(health_data, status=status_code)