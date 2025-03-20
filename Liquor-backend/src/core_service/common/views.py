from django.db import connection
from django.core.cache import cache
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions


class HealthCheckView(APIView):
    """
    API endpoint for health checks.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for health checks.
        """
        # Check database connection
        db_status = self._check_database()
        
        # Check cache connection
        cache_status = self._check_cache()
        
        # Overall health status
        is_healthy = db_status and cache_status
        
        response_data = {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'timestamp': timezone.now().isoformat(),
            'components': {
                'database': 'up' if db_status else 'down',
                'cache': 'up' if cache_status else 'down'
            }
        }
        
        status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response(response_data, status=status_code)
    
    def _check_database(self):
        """
        Check database connection.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
            return True
        except Exception:
            return False
    
    def _check_cache(self):
        """
        Check cache connection.
        """
        try:
            cache.set('health_check', 'ok', 1)
            return cache.get('health_check') == 'ok'
        except Exception:
            return False