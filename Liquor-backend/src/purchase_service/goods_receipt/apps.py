from django.apps import AppConfig


class GoodsReceiptConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods_receipt'
    
    def ready(self):
        import goods_receipt.signals