from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_service.products'
    
    def ready(self):
        import inventory_service.products.signals
