from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shop, ShopSettings, ShopActivity
from .serializers import (
    ShopSerializer, ShopCreateSerializer, ShopUpdateSerializer,
    ShopSettingsSerializer, ShopActivitySerializer
)
from users.permissions import IsTenantAdmin, IsTenantUser


class ShopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing shops.
    """
    queryset = Shop.objects.all()
    permission_classes = [IsAuthenticated, IsTenantUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tenant_id', 'status', 'shop_type', 'is_active']
    search_fields = ['name', 'code', 'city', 'state']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ShopCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ShopUpdateSerializer
        return ShopSerializer
    
    def get_queryset(self):
        """
        Filter shops by tenant_id from the authenticated user.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # SaaS admin can see all shops
        if hasattr(user, 'is_saas_admin') and user.is_saas_admin():
            return queryset
        
        # Tenant users can only see shops in their tenant
        if hasattr(user, 'tenant_id') and user.tenant_id:
            return queryset.filter(tenant_id=user.tenant_id)
        
        return Shop.objects.none()
    
    def perform_create(self, serializer):
        """
        Set tenant_id from the authenticated user if not provided.
        """
        tenant_id = serializer.validated_data.get('tenant_id')
        if not tenant_id and hasattr(self.request.user, 'tenant_id'):
            serializer.validated_data['tenant_id'] = self.request.user.tenant_id
        
        serializer.validated_data['created_by'] = self.request.user.id
        shop = serializer.save()
        
        # Log activity
        ShopActivity.objects.create(
            shop=shop,
            user_id=self.request.user.id,
            activity_type='shop_created',
            description=f"Shop {shop.name} created by {self.request.user.email}",
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
    
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """
        Get shop performance metrics.
        """
        shop = self.get_object()
        
        # This would typically fetch performance data from other services
        # For now, we'll return a placeholder response
        return Response({
            'shop_id': str(shop.id),
            'shop_name': shop.name,
            'metrics': {
                'sales': {
                    'today': 0,
                    'this_week': 0,
                    'this_month': 0
                },
                'inventory': {
                    'total_items': 0,
                    'low_stock_items': 0
                },
                'staff': {
                    'total': 0,
                    'active_today': 0
                }
            }
        })
    
    @action(detail=True, methods=['get'])
    def activity(self, request, pk=None):
        """
        Get shop activity logs.
        """
        shop = self.get_object()
        activities = ShopActivity.objects.filter(shop=shop)
        
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = ShopActivitySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ShopActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ShopSettingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing shop settings.
    """
    queryset = ShopSettings.objects.all()
    serializer_class = ShopSettingsSerializer
    permission_classes = [IsAuthenticated, IsTenantAdmin]
    
    def get_queryset(self):
        """
        Filter shop settings by tenant_id from the authenticated user.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # SaaS admin can see all shop settings
        if hasattr(user, 'is_saas_admin') and user.is_saas_admin():
            return queryset
        
        # Tenant users can only see shop settings in their tenant
        if hasattr(user, 'tenant_id') and user.tenant_id:
            return queryset.filter(shop__tenant_id=user.tenant_id)
        
        return ShopSettings.objects.none()