from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_service.common'
    
    def ready(self):
        import core_service.common.signals
