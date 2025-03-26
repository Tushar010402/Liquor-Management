from django.apps import AppConfig


class LedgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.ledger'
    
    def ready(self):
        import accounting_service.ledger.signals
