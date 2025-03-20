from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from common.permissions import IsTenantUser, CanManageInventory
from .models import BrandCategory, Brand, BrandSupplier
from .serializers import (
    BrandCategorySerializer, BrandCategoryCreateSerializer,
    BrandSerializer, BrandCreateSerializer, BrandUpdateSerializer,
    BrandSupplierSerializer, BrandSupplierCreateSerializer
)


class BrandCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing brand categories.
    """
    queryset = BrandCategory.objects.all()
    serializer_class = BrandCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTenantUser]
        else:
            permission_classes = [CanManageInventory]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return BrandCategoryCreateSerializer
        return BrandCategorySerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return BrandCategory.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new brand category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish brand category created event
        event_data = {
            'event_type': 'brand_category_created',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand-category:{category.id}', event_data)
        
        return category
    
    def perform_update(self, serializer):
        """
        Update a brand category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish brand category updated event
        event_data = {
            'event_type': 'brand_category_updated',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand-category:{category.id}', event_data)
        
        return category
    
    def perform_destroy(self, instance):
        """
        Soft delete a brand category by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish brand category deactivated event
        event_data = {
            'event_type': 'brand_category_deactivated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand-category:{instance.id}', event_data)


class BrandViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing brands.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'category', 'country_of_origin']
    search_fields = ['name', 'code', 'description', 'manufacturer']
    ordering_fields = ['name', 'code', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsTenantUser]
        else:
            permission_classes = [CanManageInventory]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return BrandCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BrandUpdateSerializer
        return BrandSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return Brand.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new brand and publish event to Kafka.
        """
        brand = serializer.save()
        
        # Publish brand created event
        event_data = {
            'event_type': 'brand_created',
            'brand_id': str(brand.id),
            'tenant_id': str(brand.tenant_id),
            'name': brand.name,
            'code': brand.code,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand:{brand.id}', event_data)
        
        return brand
    
    def perform_update(self, serializer):
        """
        Update a brand and publish event to Kafka.
        """
        brand = serializer.save()
        
        # Publish brand updated event
        event_data = {
            'event_type': 'brand_updated',
            'brand_id': str(brand.id),
            'tenant_id': str(brand.tenant_id),
            'name': brand.name,
            'code': brand.code,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand:{brand.id}', event_data)
        
        return brand
    
    def perform_destroy(self, instance):
        """
        Soft delete a brand by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish brand deactivated event
        event_data = {
            'event_type': 'brand_deactivated',
            'brand_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'brand:{instance.id}', event_data)
    
    @action(detail=True, methods=['get'])
    def suppliers(self, request, pk=None):
        """
        Get suppliers for a brand.
        """
        brand = self.get_object()
        suppliers = BrandSupplier.objects.filter(brand=brand)
        serializer = BrandSupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_supplier(self, request, pk=None):
        """
        Add a supplier to a brand.
        """
        brand = self.get_object()
        serializer = BrandSupplierCreateSerializer(
            data=request.data,
            context={'brand': brand}
        )
        
        if serializer.is_valid():
            supplier = serializer.save()
            
            # Publish brand supplier added event
            event_data = {
                'event_type': 'brand_supplier_added',
                'brand_id': str(brand.id),
                'tenant_id': str(brand.tenant_id),
                'supplier_id': str(supplier.supplier_id),
                'supplier_name': supplier.supplier_name,
                'is_primary': supplier.is_primary,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'brand:{brand.id}', event_data)
            
            return Response(
                BrandSupplierSerializer(supplier).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-supplier/(?P<supplier_id>[^/.]+)')
    def remove_supplier(self, request, pk=None, supplier_id=None):
        """
        Remove a supplier from a brand.
        """
        brand = self.get_object()
        try:
            supplier = BrandSupplier.objects.get(brand=brand, supplier_id=supplier_id)
            supplier_name = supplier.supplier_name
            supplier.delete()
            
            # Publish brand supplier removed event
            event_data = {
                'event_type': 'brand_supplier_removed',
                'brand_id': str(brand.id),
                'tenant_id': str(brand.tenant_id),
                'supplier_id': supplier_id,
                'supplier_name': supplier_name,
                'removed_by': str(request.user.id)
            }
            publish_event('inventory-events', f'brand:{brand.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BrandSupplier.DoesNotExist:
            return Response(
                {'detail': 'Supplier not found for this brand.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='set-primary-supplier/(?P<supplier_id>[^/.]+)')
    def set_primary_supplier(self, request, pk=None, supplier_id=None):
        """
        Set a supplier as the primary supplier for a brand.
        """
        brand = self.get_object()
        try:
            supplier = BrandSupplier.objects.get(brand=brand, supplier_id=supplier_id)
            
            # Set this supplier as primary
            supplier.is_primary = True
            supplier.save()
            
            # Unset other primary suppliers
            BrandSupplier.objects.filter(
                brand=brand,
                is_primary=True
            ).exclude(id=supplier.id).update(is_primary=False)
            
            # Publish brand primary supplier set event
            event_data = {
                'event_type': 'brand_primary_supplier_set',
                'brand_id': str(brand.id),
                'tenant_id': str(brand.tenant_id),
                'supplier_id': supplier_id,
                'supplier_name': supplier.supplier_name,
                'set_by': str(request.user.id)
            }
            publish_event('inventory-events', f'brand:{brand.id}', event_data)
            
            return Response(
                BrandSupplierSerializer(supplier).data,
                status=status.HTTP_200_OK
            )
        except BrandSupplier.DoesNotExist:
            return Response(
                {'detail': 'Supplier not found for this brand.'},
                status=status.HTTP_404_NOT_FOUND
            )