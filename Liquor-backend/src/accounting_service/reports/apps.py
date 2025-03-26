from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.reports'
    
    def ready(self):
        import accounting_service.reports.signals
