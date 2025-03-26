from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reporting_service.common'
    
    def ready(self):
        import reporting_service.common.signals
