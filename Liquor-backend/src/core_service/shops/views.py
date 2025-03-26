from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from tenants.permissions import IsSaasAdmin, IsTenantAdmin, IsTenantUser
from .models import Shop, ShopOperatingHours, ShopHoliday, ShopSettings
from .serializers import (
    ShopSerializer, ShopCreateSerializer, ShopUpdateSerializer,
    ShopOperatingHoursSerializer, ShopOperatingHoursCreateSerializer,
    ShopHolidaySerializer, ShopHolidayCreateSerializer,
    ShopSettingsSerializer, ShopSettingsUpdateSerializer
)


class ShopViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing shops.
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_open', 'city', 'state', 'country']
    search_fields = ['name', 'code', 'address', 'city', 'manager_name']
    ordering_fields = ['name', 'created_at', 'city']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'destroy']:
            permission_classes = [IsSaasAdmin | IsTenantAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsSaasAdmin | IsTenantAdmin]
        else:
            permission_classes = [IsTenantUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return ShopCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ShopUpdateSerializer
        return ShopSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user role and tenant.
        """
        user = self.request.user
        queryset = Shop.objects.all()
        
        # SaaS Admin can see all shops
        if user.role == 'saas_admin':
            return queryset
        
        # Other users can only see shops in their tenant
        return queryset.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new shop and publish event to Kafka.
        """
        shop = serializer.save()
        
        # Publish shop created event
        event_data = {
            'event_type': 'shop_created',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'code': shop.code,
            'created_by': str(self.request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return shop
    
    def perform_update(self, serializer):
        """
        Update a shop and publish event to Kafka.
        """
        shop = serializer.save()
        
        # Publish shop updated event
        event_data = {
            'event_type': 'shop_updated',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'code': shop.code,
            'updated_by': str(self.request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return shop
    
    def perform_destroy(self, instance):
        """
        Soft delete a shop by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish shop deactivated event
        event_data = {
            'event_type': 'shop_deactivated',
            'shop_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('shop-events', f'shop:{instance.id}', event_data)
    
    @action(detail=True, methods=['get'])
    def operating_hours(self, request, pk=None):
        """
        Get operating hours for a shop.
        """
        shop = self.get_object()
        hours = ShopOperatingHours.objects.filter(shop=shop)
        serializer = ShopOperatingHoursSerializer(hours, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_operating_hours(self, request, pk=None):
        """
        Add operating hours to a shop.
        """
        shop = self.get_object()
        serializer = ShopOperatingHoursCreateSerializer(
            data=request.data,
            context={'shop': shop}
        )
        
        if serializer.is_valid():
            hours = serializer.save()
            
            # Publish operating hours added event
            event_data = {
                'event_type': 'shop_operating_hours_added',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'day_of_week': hours.day_of_week,
                'added_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(
                ShopOperatingHoursSerializer(hours).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='update-operating-hours/(?P<hours_id>[^/.]+)')
    def update_operating_hours(self, request, pk=None, hours_id=None):
        """
        Update operating hours for a shop.
        """
        shop = self.get_object()
        try:
            hours = ShopOperatingHours.objects.get(id=hours_id, shop=shop)
        except ShopOperatingHours.DoesNotExist:
            return Response(
                {'detail': 'Operating hours not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ShopOperatingHoursSerializer(hours, data=request.data, partial=True)
        if serializer.is_valid():
            updated_hours = serializer.save()
            
            # Publish operating hours updated event
            event_data = {
                'event_type': 'shop_operating_hours_updated',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'day_of_week': updated_hours.day_of_week,
                'updated_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='delete-operating-hours/(?P<hours_id>[^/.]+)')
    def delete_operating_hours(self, request, pk=None, hours_id=None):
        """
        Delete operating hours for a shop.
        """
        shop = self.get_object()
        try:
            hours = ShopOperatingHours.objects.get(id=hours_id, shop=shop)
            day_of_week = hours.day_of_week
            hours.delete()
            
            # Publish operating hours deleted event
            event_data = {
                'event_type': 'shop_operating_hours_deleted',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'day_of_week': day_of_week,
                'deleted_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShopOperatingHours.DoesNotExist:
            return Response(
                {'detail': 'Operating hours not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def holidays(self, request, pk=None):
        """
        Get holidays for a shop.
        """
        shop = self.get_object()
        holidays = ShopHoliday.objects.filter(shop=shop)
        serializer = ShopHolidaySerializer(holidays, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_holiday(self, request, pk=None):
        """
        Add a holiday to a shop.
        """
        shop = self.get_object()
        serializer = ShopHolidayCreateSerializer(
            data=request.data,
            context={'shop': shop}
        )
        
        if serializer.is_valid():
            holiday = serializer.save()
            
            # Publish holiday added event
            event_data = {
                'event_type': 'shop_holiday_added',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'holiday_id': str(holiday.id),
                'name': holiday.name,
                'date': holiday.date.isoformat(),
                'added_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(
                ShopHolidaySerializer(holiday).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='delete-holiday/(?P<holiday_id>[^/.]+)')
    def delete_holiday(self, request, pk=None, holiday_id=None):
        """
        Delete a holiday from a shop.
        """
        shop = self.get_object()
        try:
            holiday = ShopHoliday.objects.get(id=holiday_id, shop=shop)
            holiday_name = holiday.name
            holiday_date = holiday.date
            holiday.delete()
            
            # Publish holiday deleted event
            event_data = {
                'event_type': 'shop_holiday_deleted',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'holiday_name': holiday_name,
                'holiday_date': holiday_date.isoformat(),
                'deleted_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShopHoliday.DoesNotExist:
            return Response(
                {'detail': 'Holiday not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def settings(self, request, pk=None):
        """
        Get settings for a shop.
        """
        shop = self.get_object()
        settings = shop.settings
        serializer = ShopSettingsSerializer(settings)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put', 'patch'])
    def update_settings(self, request, pk=None):
        """
        Update settings for a shop.
        """
        shop = self.get_object()
        settings = shop.settings
        
        serializer = ShopSettingsUpdateSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Publish shop settings updated event
            event_data = {
                'event_type': 'shop_settings_updated',
                'shop_id': str(shop.id),
                'tenant_id': str(shop.tenant_id),
                'updated_by': str(request.user.id)
            }
            publish_event('shop-events', f'shop:{shop.id}', event_data)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def open(self, request, pk=None):
        """
        Open a shop.
        """
        shop = self.get_object()
        shop.is_open = True
        shop.save()
        
        # Publish shop opened event
        event_data = {
            'event_type': 'shop_opened',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'opened_by': str(request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return Response({'message': 'Shop opened successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Close a shop.
        """
        shop = self.get_object()
        shop.is_open = False
        shop.save()
        
        # Publish shop closed event
        event_data = {
            'event_type': 'shop_closed',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'closed_by': str(request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return Response({'message': 'Shop closed successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a shop.
        """
        shop = self.get_object()
        shop.is_active = True
        shop.save()
        
        # Publish shop activated event
        event_data = {
            'event_type': 'shop_activated',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'activated_by': str(request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return Response({'message': 'Shop activated successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a shop.
        """
        shop = self.get_object()
        shop.is_active = False
        shop.save()
        
        # Publish shop deactivated event
        event_data = {
            'event_type': 'shop_deactivated',
            'shop_id': str(shop.id),
            'tenant_id': str(shop.tenant_id),
            'name': shop.name,
            'deactivated_by': str(request.user.id)
        }
        publish_event('shop-events', f'shop:{shop.id}', event_data)
        
        return Response({'message': 'Shop deactivated successfully.'}, status=status.HTTP_200_OK)