from django.apps import AppConfig


class TenantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_service.tenants'
    
    def ready(self):
        import core_service.tenants.signals
