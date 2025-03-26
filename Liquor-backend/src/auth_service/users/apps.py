from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service.users'
    
    def ready(self):
        import auth_service.users.signals
