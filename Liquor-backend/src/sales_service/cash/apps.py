from django.apps import AppConfig


class CashConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.cash'
    
    def ready(self):
        import sales_service.cash.signals
