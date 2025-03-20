from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Permission, Role, RolePermission
from .serializers import (
    PermissionSerializer, RoleSerializer, RoleCreateSerializer,
    RoleUpdateSerializer, RolePermissionSerializer, RolePermissionAssignSerializer
)
from users.permissions import IsSaasAdmin, IsTenantAdmin


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'category']
    ordering = ['category', 'name']


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing roles.
    """
    queryset = Role.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tenant_id', 'is_system_role', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RoleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RoleUpdateSerializer
        elif self.action == 'permissions':
            return RolePermissionAssignSerializer
        return RoleSerializer
    
    def get_queryset(self):
        """
        Filter roles by tenant_id from the authenticated user.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # SaaS admin can see all roles
        if hasattr(user, 'is_saas_admin') and user.is_saas_admin():
            return queryset
        
        # Tenant users can only see roles in their tenant or system roles
        if hasattr(user, 'tenant_id') and user.tenant_id:
            return queryset.filter(tenant_id=user.tenant_id) | queryset.filter(is_system_role=True)
        
        return Role.objects.none()
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'permissions']:
            permission_classes = [IsAuthenticated, IsTenantAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Set tenant_id from the authenticated user if not provided.
        """
        tenant_id = serializer.validated_data.get('tenant_id')
        if not tenant_id and hasattr(self.request.user, 'tenant_id'):
            serializer.validated_data['tenant_id'] = self.request.user.tenant_id
        
        # Only SaaS admin can create system roles
        if not (hasattr(self.request.user, 'is_saas_admin') and self.request.user.is_saas_admin()):
            serializer.validated_data['is_system_role'] = False
        
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def permissions(self, request, pk=None):
        """
        Assign permissions to a role.
        """
        role = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            permission_ids = serializer.validated_data['permission_ids']
            
            # Remove existing permissions
            RolePermission.objects.filter(role=role).delete()
            
            # Add new permissions
            for permission_id in permission_ids:
                try:
                    permission = Permission.objects.get(id=permission_id)
                    RolePermission.objects.create(role=role, permission=permission)
                except Permission.DoesNotExist:
                    pass
            
            return Response({'status': 'permissions assigned'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)