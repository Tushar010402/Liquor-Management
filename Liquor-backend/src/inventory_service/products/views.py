from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from common.permissions import IsTenantUser, CanManageInventory
from .models import (
    ProductCategory, ProductType, Product, ProductVariant,
    ProductAttribute, ProductAttributeValue, ProductPriceHistory
)
from .serializers import (
    ProductCategorySerializer, ProductCategoryCreateSerializer,
    ProductTypeSerializer, ProductTypeCreateSerializer,
    ProductAttributeSerializer, ProductAttributeCreateSerializer,
    ProductAttributeValueSerializer, ProductAttributeValueCreateSerializer,
    ProductVariantSerializer, ProductVariantCreateSerializer,
    ProductPriceHistorySerializer,
    ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer
)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product categories.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
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
            return ProductCategoryCreateSerializer
        return ProductCategorySerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return ProductCategory.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new product category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish product category created event
        event_data = {
            'event_type': 'product_category_created',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-category:{category.id}', event_data)
        
        return category
    
    def perform_update(self, serializer):
        """
        Update a product category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish product category updated event
        event_data = {
            'event_type': 'product_category_updated',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-category:{category.id}', event_data)
        
        return category
    
    def perform_destroy(self, instance):
        """
        Soft delete a product category by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish product category deactivated event
        event_data = {
            'event_type': 'product_category_deactivated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-category:{instance.id}', event_data)


class ProductTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product types.
    """
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
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
            return ProductTypeCreateSerializer
        return ProductTypeSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return ProductType.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new product type and publish event to Kafka.
        """
        product_type = serializer.save()
        
        # Publish product type created event
        event_data = {
            'event_type': 'product_type_created',
            'product_type_id': str(product_type.id),
            'tenant_id': str(product_type.tenant_id),
            'name': product_type.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-type:{product_type.id}', event_data)
        
        return product_type
    
    def perform_update(self, serializer):
        """
        Update a product type and publish event to Kafka.
        """
        product_type = serializer.save()
        
        # Publish product type updated event
        event_data = {
            'event_type': 'product_type_updated',
            'product_type_id': str(product_type.id),
            'tenant_id': str(product_type.tenant_id),
            'name': product_type.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-type:{product_type.id}', event_data)
        
        return product_type
    
    def perform_destroy(self, instance):
        """
        Soft delete a product type by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish product type deactivated event
        event_data = {
            'event_type': 'product_type_deactivated',
            'product_type_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-type:{instance.id}', event_data)


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing product attributes.
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
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
            return ProductAttributeCreateSerializer
        return ProductAttributeSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return ProductAttribute.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new product attribute and publish event to Kafka.
        """
        attribute = serializer.save()
        
        # Publish product attribute created event
        event_data = {
            'event_type': 'product_attribute_created',
            'attribute_id': str(attribute.id),
            'tenant_id': str(attribute.tenant_id),
            'name': attribute.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-attribute:{attribute.id}', event_data)
        
        return attribute
    
    def perform_update(self, serializer):
        """
        Update a product attribute and publish event to Kafka.
        """
        attribute = serializer.save()
        
        # Publish product attribute updated event
        event_data = {
            'event_type': 'product_attribute_updated',
            'attribute_id': str(attribute.id),
            'tenant_id': str(attribute.tenant_id),
            'name': attribute.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-attribute:{attribute.id}', event_data)
        
        return attribute
    
    def perform_destroy(self, instance):
        """
        Soft delete a product attribute by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish product attribute deactivated event
        event_data = {
            'event_type': 'product_attribute_deactivated',
            'attribute_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product-attribute:{instance.id}', event_data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_available', 'brand', 'category', 'product_type']
    search_fields = ['name', 'code', 'barcode', 'description']
    ordering_fields = ['name', 'code', 'created_at', 'updated_at', 'selling_price', 'mrp']
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
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return Product.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new product and publish event to Kafka.
        """
        product = serializer.save()
        
        # Publish product created event
        event_data = {
            'event_type': 'product_created',
            'product_id': str(product.id),
            'tenant_id': str(product.tenant_id),
            'name': product.name,
            'code': product.code,
            'brand_id': str(product.brand.id),
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product:{product.id}', event_data)
        
        return product
    
    def perform_update(self, serializer):
        """
        Update a product and publish event to Kafka.
        """
        product = serializer.save()
        
        # Publish product updated event
        event_data = {
            'event_type': 'product_updated',
            'product_id': str(product.id),
            'tenant_id': str(product.tenant_id),
            'name': product.name,
            'code': product.code,
            'brand_id': str(product.brand.id),
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product:{product.id}', event_data)
        
        return product
    
    def perform_destroy(self, instance):
        """
        Soft delete a product by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish product deactivated event
        event_data = {
            'event_type': 'product_deactivated',
            'product_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'product:{instance.id}', event_data)
    
    @action(detail=True, methods=['get'])
    def variants(self, request, pk=None):
        """
        Get variants for a product.
        """
        product = self.get_object()
        variants = ProductVariant.objects.filter(product=product)
        serializer = ProductVariantSerializer(variants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_variant(self, request, pk=None):
        """
        Add a variant to a product.
        """
        product = self.get_object()
        serializer = ProductVariantCreateSerializer(
            data=request.data,
            context={'product': product}
        )
        
        if serializer.is_valid():
            variant = serializer.save()
            
            # Publish product variant added event
            event_data = {
                'event_type': 'product_variant_added',
                'product_id': str(product.id),
                'tenant_id': str(product.tenant_id),
                'variant_id': str(variant.id),
                'name': variant.name,
                'code': variant.code,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'product:{product.id}', event_data)
            
            return Response(
                ProductVariantSerializer(variant).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def attributes(self, request, pk=None):
        """
        Get attribute values for a product.
        """
        product = self.get_object()
        attribute_values = ProductAttributeValue.objects.filter(product=product)
        serializer = ProductAttributeValueSerializer(attribute_values, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_attribute(self, request, pk=None):
        """
        Add an attribute value to a product.
        """
        product = self.get_object()
        serializer = ProductAttributeValueCreateSerializer(
            data=request.data,
            context={'product': product}
        )
        
        if serializer.is_valid():
            attribute_value = serializer.save()
            
            # Publish product attribute value added event
            event_data = {
                'event_type': 'product_attribute_value_added',
                'product_id': str(product.id),
                'tenant_id': str(product.tenant_id),
                'attribute_id': str(attribute_value.attribute.id),
                'attribute_name': attribute_value.attribute.name,
                'value': attribute_value.value,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'product:{product.id}', event_data)
            
            return Response(
                ProductAttributeValueSerializer(attribute_value).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        """
        Get price history for a product.
        """
        product = self.get_object()
        price_history = ProductPriceHistory.objects.filter(product=product)
        serializer = ProductPriceHistorySerializer(price_history, many=True)
        return Response(serializer.data)