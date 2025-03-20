from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from .models import Tenant, TenantSettings
from .serializers import (
    TenantSerializer, TenantCreateSerializer, TenantUpdateSerializer,
    TenantSettingsSerializer, TenantSettingsUpdateSerializer
)
from .permissions import IsSaasAdmin, IsTenantAdmin


class TenantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tenants.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'subscription_plan']
    search_fields = ['name', 'email', 'contact_person_name', 'contact_person_email']
    ordering_fields = ['name', 'created_at', 'subscription_end_date']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [IsSaasAdmin]
        elif self.action in ['retrieve', 'update', 'partial_update', 'settings']:
            permission_classes = [IsSaasAdmin | IsTenantAdmin]
        else:
            permission_classes = [IsSaasAdmin]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return TenantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TenantUpdateSerializer
        return TenantSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role and tenant.
        """
        user = self.request.user
        queryset = Tenant.objects.all()
        
        # SaaS Admin can see all tenants
        if user.role == 'saas_admin':
            return queryset
        
        # Tenant Admin can only see their own tenant
        if user.role == 'tenant_admin':
            return queryset.filter(id=user.tenant_id)
        
        # Other users can't see any tenants
        return Tenant.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a new tenant and publish event to Kafka.
        """
        tenant = serializer.save()
        
        # Publish tenant created event
        event_data = {
            'event_type': 'tenant_created',
            'tenant_id': str(tenant.id),
            'name': tenant.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('tenant-events', f'tenant:{tenant.id}', event_data)
        
        return tenant
    
    def perform_update(self, serializer):
        """
        Update a tenant and publish event to Kafka.
        """
        tenant = serializer.save()
        
        # Publish tenant updated event
        event_data = {
            'event_type': 'tenant_updated',
            'tenant_id': str(tenant.id),
            'name': tenant.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('tenant-events', f'tenant:{tenant.id}', event_data)
        
        return tenant
    
    def perform_destroy(self, instance):
        """
        Soft delete a tenant by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish tenant deactivated event
        event_data = {
            'event_type': 'tenant_deactivated',
            'tenant_id': str(instance.id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('tenant-events', f'tenant:{instance.id}', event_data)
    
    @action(detail=True, methods=['get'])
    def settings(self, request, pk=None):
        """
        Get settings for a tenant.
        """
        tenant = self.get_object()
        settings = tenant.settings
        serializer = TenantSettingsSerializer(settings)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_settings(self, request, pk=None):
        """
        Update settings for a tenant.
        """
        tenant = self.get_object()
        settings = tenant.settings
        
        serializer = TenantSettingsUpdateSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Publish tenant settings updated event
            event_data = {
                'event_type': 'tenant_settings_updated',
                'tenant_id': str(tenant.id),
                'updated_by': str(request.user.id)
            }
            publish_event('tenant-events', f'tenant:{tenant.id}', event_data)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a tenant.
        """
        tenant = self.get_object()
        tenant.is_active = True
        tenant.save()
        
        # Publish tenant activated event
        event_data = {
            'event_type': 'tenant_activated',
            'tenant_id': str(tenant.id),
            'name': tenant.name,
            'activated_by': str(request.user.id)
        }
        publish_event('tenant-events', f'tenant:{tenant.id}', event_data)
        
        return Response({'message': 'Tenant activated successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a tenant.
        """
        tenant = self.get_object()
        tenant.is_active = False
        tenant.save()
        
        # Publish tenant deactivated event
        event_data = {
            'event_type': 'tenant_deactivated',
            'tenant_id': str(tenant.id),
            'name': tenant.name,
            'deactivated_by': str(request.user.id)
        }
        publish_event('tenant-events', f'tenant:{tenant.id}', event_data)
        
        return Response({'message': 'Tenant deactivated successfully.'}, status=status.HTTP_200_OK)