from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_service.common'
    
    def ready(self):
        import purchase_service.common.signals
