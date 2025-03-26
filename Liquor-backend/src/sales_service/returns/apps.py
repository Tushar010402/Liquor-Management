from django.apps import AppConfig


class ReturnsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.returns'
    
    def ready(self):
        import sales_service.returns.signals
