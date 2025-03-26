from django.apps import AppConfig


class ShopsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service.shops'
    label = 'auth_shops'
    
    def ready(self):
        import auth_service.shops.signals
