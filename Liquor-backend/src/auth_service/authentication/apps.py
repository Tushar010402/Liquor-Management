from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service.authentication'
    
    def ready(self):
        import auth_service.authentication.signals
