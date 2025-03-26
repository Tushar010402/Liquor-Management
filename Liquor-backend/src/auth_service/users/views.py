from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from .models import UserShopAssignment, UserPermission
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer,
    PasswordChangeSerializer, UserShopAssignmentSerializer,
    UserPermissionSerializer, UserShopAssignmentCreateSerializer,
    UserPermissionCreateSerializer
)
from .permissions import (
    IsSaasAdmin, IsTenantAdmin, IsUserManager, 
    IsSelfOrAdmin, CanManageUsers
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active', 'tenant_id']
    search_fields = ['email', 'full_name', 'phone']
    ordering_fields = ['email', 'full_name', 'date_joined', 'last_login']
    ordering = ['-date_joined']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsSaasAdmin | IsTenantAdmin]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsSaasAdmin | IsTenantAdmin | IsUserManager]
        elif self.action == 'change_password':
            permission_classes = [IsSelfOrAdmin]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [CanManageUsers]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return PasswordChangeSerializer
        return UserSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role and tenant.
        """
        user = self.request.user
        queryset = User.objects.all()
        
        # SaaS Admin can see all users
        if user.is_saas_admin():
            return queryset
        
        # Tenant Admin can see all users in their tenant
        if user.is_tenant_admin():
            return queryset.filter(tenant_id=user.tenant_id)
        
        # Managers can see users in their tenant with lower roles
        if user.is_manager():
            return queryset.filter(
                tenant_id=user.tenant_id,
                role__in=[User.ROLE_ASSISTANT_MANAGER, User.ROLE_EXECUTIVE]
            )
        
        # Assistant Managers can see executives in their tenant
        if user.is_assistant_manager():
            return queryset.filter(
                tenant_id=user.tenant_id,
                role=User.ROLE_EXECUTIVE
            )
        
        # Executives can only see themselves
        return queryset.filter(id=user.id)
    
    def perform_create(self, serializer):
        """
        Create a new user and publish event to Kafka.
        """
        user = serializer.save()
        
        # Publish user created event
        event_data = {
            'event_type': 'user_created',
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'created_by': str(self.request.user.id)
        }
        publish_event('user-events', f'user:{user.id}', event_data)
        
        return user
    
    def perform_update(self, serializer):
        """
        Update a user and publish event to Kafka.
        """
        user = serializer.save()
        
        # Publish user updated event
        event_data = {
            'event_type': 'user_updated',
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'updated_by': str(self.request.user.id)
        }
        publish_event('user-events', f'user:{user.id}', event_data)
        
        return user
    
    def perform_destroy(self, instance):
        """
        Soft delete a user by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish user deactivated event
        event_data = {
            'event_type': 'user_deactivated',
            'user_id': str(instance.id),
            'email': instance.email,
            'role': instance.role,
            'tenant_id': str(instance.tenant_id) if instance.tenant_id else None,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('user-events', f'user:{instance.id}', event_data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """
        Change a user's password.
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ['Wrong password.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Publish password changed event
            event_data = {
                'event_type': 'user_password_changed',
                'user_id': str(user.id),
                'changed_by': str(request.user.id)
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            return Response(
                {'message': 'Password updated successfully.'},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a user account.
        """
        user = self.get_object()
        user.is_active = True
        user.save()
        
        # Publish user activated event
        event_data = {
            'event_type': 'user_activated',
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'activated_by': str(request.user.id)
        }
        publish_event('user-events', f'user:{user.id}', event_data)
        
        return Response(
            {'message': 'User activated successfully.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a user account.
        """
        user = self.get_object()
        user.is_active = False
        user.save()
        
        # Publish user deactivated event
        event_data = {
            'event_type': 'user_deactivated',
            'user_id': str(user.id),
            'email': user.email,
            'role': user.role,
            'tenant_id': str(user.tenant_id) if user.tenant_id else None,
            'deactivated_by': str(request.user.id)
        }
        publish_event('user-events', f'user:{user.id}', event_data)
        
        return Response(
            {'message': 'User deactivated successfully.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def shops(self, request, pk=None):
        """
        Get shops assigned to a user.
        """
        user = self.get_object()
        assignments = UserShopAssignment.objects.filter(user=user)
        serializer = UserShopAssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_shop(self, request, pk=None):
        """
        Assign a shop to a user.
        """
        user = self.get_object()
        serializer = UserShopAssignmentCreateSerializer(
            data=request.data,
            context={'user': user}
        )
        
        if serializer.is_valid():
            assignment = serializer.save()
            
            # If this is set as primary, unset other primary assignments
            if assignment.is_primary:
                UserShopAssignment.objects.filter(
                    user=user,
                    is_primary=True
                ).exclude(id=assignment.id).update(is_primary=False)
            
            # Publish shop assignment event
            event_data = {
                'event_type': 'user_shop_assigned',
                'user_id': str(user.id),
                'shop_id': str(assignment.shop_id),
                'is_primary': assignment.is_primary,
                'assigned_by': str(request.user.id)
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            return Response(
                UserShopAssignmentSerializer(assignment).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='unassign-shop/(?P<shop_id>[^/.]+)')
    def unassign_shop(self, request, pk=None, shop_id=None):
        """
        Unassign a shop from a user.
        """
        user = self.get_object()
        try:
            assignment = UserShopAssignment.objects.get(user=user, shop_id=shop_id)
            assignment.delete()
            
            # Publish shop unassignment event
            event_data = {
                'event_type': 'user_shop_unassigned',
                'user_id': str(user.id),
                'shop_id': shop_id,
                'unassigned_by': str(request.user.id)
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserShopAssignment.DoesNotExist:
            return Response(
                {'detail': 'Shop assignment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """
        Get custom permissions assigned to a user.
        """
        user = self.get_object()
        permissions = UserPermission.objects.filter(user=user)
        serializer = UserPermissionSerializer(permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        """
        Add a custom permission to a user.
        """
        user = self.get_object()
        serializer = UserPermissionCreateSerializer(
            data=request.data,
            context={'user': user}
        )
        
        if serializer.is_valid():
            permission = serializer.save()
            
            # Publish permission added event
            event_data = {
                'event_type': 'user_permission_added',
                'user_id': str(user.id),
                'permission_key': permission.permission_key,
                'added_by': str(request.user.id)
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            return Response(
                UserPermissionSerializer(permission).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-permission/(?P<permission_key>[^/.]+)')
    def remove_permission(self, request, pk=None, permission_key=None):
        """
        Remove a custom permission from a user.
        """
        user = self.get_object()
        try:
            permission = UserPermission.objects.get(user=user, permission_key=permission_key)
            permission.delete()
            
            # Publish permission removed event
            event_data = {
                'event_type': 'user_permission_removed',
                'user_id': str(user.id),
                'permission_key': permission_key,
                'removed_by': str(request.user.id)
            }
            publish_event('user-events', f'user:{user.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserPermission.DoesNotExist:
            return Response(
                {'detail': 'Permission not found.'},
                status=status.HTTP_404_NOT_FOUND
            )