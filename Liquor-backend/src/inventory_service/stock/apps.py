from django.apps import AppConfig


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_service.stock'
    
    def ready(self):
        import inventory_service.stock.signals
