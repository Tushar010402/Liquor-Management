from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_service.accounts'
    
    def ready(self):
        import accounting_service.accounts.signals
