from django.apps import AppConfig


class GoodsReceiptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchase_service.goods_receipt'
    
    def ready(self):
        import purchase_service.goods_receipt.signals
