from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.common'
    
    def ready(self):
        import accounting_service.common.signals
