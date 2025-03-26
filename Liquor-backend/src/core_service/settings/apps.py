from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_service.settings'
    
    def ready(self):
        import core_service.settings.signals
