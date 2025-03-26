from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_service.suppliers'
    
    def ready(self):
        import inventory_service.suppliers.signals
