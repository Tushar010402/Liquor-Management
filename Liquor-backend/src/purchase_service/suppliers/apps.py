from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_service.suppliers'
    label = 'purchase_suppliers'
    
    def ready(self):
        import purchase_service.suppliers.signals
