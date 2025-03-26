from django.apps import AppConfig


class TenantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service.tenants'
    label = 'auth_tenants'
    
    def ready(self):
        import auth_service.tenants.signals
