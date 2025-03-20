from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from tenants.permissions import IsSaasAdmin, IsTenantAdmin, IsTenantUser
from .models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate
from .serializers import (
    SystemSettingSerializer, SystemSettingCreateSerializer,
    TenantSettingSerializer, TenantSettingCreateSerializer,
    EmailTemplateSerializer, EmailTemplateCreateSerializer,
    NotificationTemplateSerializer, NotificationTemplateCreateSerializer
)


class SystemSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing system settings.
    """
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_public']
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at', 'updated_at']
    ordering = ['key']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsSaasAdmin | IsTenantAdmin]
        else:
            permission_classes = [IsSaasAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return SystemSettingCreateSerializer
        return SystemSettingSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        """
        user = self.request.user
        queryset = SystemSetting.objects.all()
        
        # SaaS Admin can see all system settings
        if user.role == 'saas_admin':
            return queryset
        
        # Tenant Admin can only see public system settings
        return queryset.filter(is_public=True)
    
    def perform_create(self, serializer):
        """
        Create a new system setting and publish event to Kafka.
        """
        setting = serializer.save()
        
        # Publish system setting created event
        event_data = {
            'event_type': 'system_setting_created',
            'setting_id': str(setting.id),
            'key': setting.key,
            'created_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'system-setting:{setting.id}', event_data)
        
        return setting
    
    def perform_update(self, serializer):
        """
        Update a system setting and publish event to Kafka.
        """
        setting = serializer.save()
        
        # Publish system setting updated event
        event_data = {
            'event_type': 'system_setting_updated',
            'setting_id': str(setting.id),
            'key': setting.key,
            'updated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'system-setting:{setting.id}', event_data)
        
        return setting
    
    def perform_destroy(self, instance):
        """
        Soft delete a system setting by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish system setting deactivated event
        event_data = {
            'event_type': 'system_setting_deactivated',
            'setting_id': str(instance.id),
            'key': instance.key,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'system-setting:{instance.id}', event_data)


class TenantSettingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tenant settings.
    """
    queryset = TenantSetting.objects.all()
    serializer_class = TenantSettingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['key', 'description']
    ordering_fields = ['key', 'created_at', 'updated_at']
    ordering = ['key']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsTenantUser]
        else:
            permission_classes = [IsTenantAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return TenantSettingCreateSerializer
        return TenantSettingSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return TenantSetting.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new tenant setting and publish event to Kafka.
        """
        setting = serializer.save()
        
        # Publish tenant setting created event
        event_data = {
            'event_type': 'tenant_setting_created',
            'setting_id': str(setting.id),
            'tenant_id': str(setting.tenant_id),
            'key': setting.key,
            'created_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'tenant-setting:{setting.id}', event_data)
        
        return setting
    
    def perform_update(self, serializer):
        """
        Update a tenant setting and publish event to Kafka.
        """
        setting = serializer.save()
        
        # Publish tenant setting updated event
        event_data = {
            'event_type': 'tenant_setting_updated',
            'setting_id': str(setting.id),
            'tenant_id': str(setting.tenant_id),
            'key': setting.key,
            'updated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'tenant-setting:{setting.id}', event_data)
        
        return setting
    
    def perform_destroy(self, instance):
        """
        Soft delete a tenant setting by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish tenant setting deactivated event
        event_data = {
            'event_type': 'tenant_setting_deactivated',
            'setting_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'key': instance.key,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'tenant-setting:{instance.id}', event_data)


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing email templates.
    """
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'subject', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsTenantAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return EmailTemplateCreateSerializer
        return EmailTemplateSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return EmailTemplate.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new email template and publish event to Kafka.
        """
        template = serializer.save()
        
        # Publish email template created event
        event_data = {
            'event_type': 'email_template_created',
            'template_id': str(template.id),
            'tenant_id': str(template.tenant_id),
            'name': template.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'email-template:{template.id}', event_data)
        
        return template
    
    def perform_update(self, serializer):
        """
        Update an email template and publish event to Kafka.
        """
        template = serializer.save()
        
        # Publish email template updated event
        event_data = {
            'event_type': 'email_template_updated',
            'template_id': str(template.id),
            'tenant_id': str(template.tenant_id),
            'name': template.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'email-template:{template.id}', event_data)
        
        return template
    
    def perform_destroy(self, instance):
        """
        Soft delete an email template by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish email template deactivated event
        event_data = {
            'event_type': 'email_template_deactivated',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'email-template:{instance.id}', event_data)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing notification templates.
    """
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'title', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsTenantAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return NotificationTemplateCreateSerializer
        return NotificationTemplateSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return NotificationTemplate.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new notification template and publish event to Kafka.
        """
        template = serializer.save()
        
        # Publish notification template created event
        event_data = {
            'event_type': 'notification_template_created',
            'template_id': str(template.id),
            'tenant_id': str(template.tenant_id),
            'name': template.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'notification-template:{template.id}', event_data)
        
        return template
    
    def perform_update(self, serializer):
        """
        Update a notification template and publish event to Kafka.
        """
        template = serializer.save()
        
        # Publish notification template updated event
        event_data = {
            'event_type': 'notification_template_updated',
            'template_id': str(template.id),
            'tenant_id': str(template.tenant_id),
            'name': template.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'notification-template:{template.id}', event_data)
        
        return template
    
    def perform_destroy(self, instance):
        """
        Soft delete a notification template by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish notification template deactivated event
        event_data = {
            'event_type': 'notification_template_deactivated',
            'template_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('setting-events', f'notification-template:{instance.id}', event_data)