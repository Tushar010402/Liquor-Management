from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.sales'
    
    def ready(self):
        import sales_service.sales.signals
