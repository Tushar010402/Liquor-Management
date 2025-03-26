from django.apps import AppConfig


class ApprovalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_service.approvals'
    
    def ready(self):
        import sales_service.approvals.signals
