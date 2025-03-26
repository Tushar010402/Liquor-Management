from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.common'
    
    def ready(self):
        import sales_service.common.signals
