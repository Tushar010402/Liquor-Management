from django.apps import AppConfig


class JournalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.journals'
    
    def ready(self):
        import accounting_service.journals.signals
