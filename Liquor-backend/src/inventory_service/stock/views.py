from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from common.permissions import IsTenantUser, CanManageInventory
from .models import (
    StockLevel, StockTransaction, StockTransfer, StockTransferItem,
    StockAdjustment, StockAdjustmentItem
)
from .serializers import (
    StockLevelSerializer, StockLevelCreateSerializer, StockLevelUpdateSerializer,
    StockTransactionSerializer, StockTransactionCreateSerializer,
    StockTransferSerializer, StockTransferCreateSerializer, StockTransferUpdateSerializer,
    StockAdjustmentSerializer, StockAdjustmentCreateSerializer
)


class StockLevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stock levels.
    """
    queryset = StockLevel.objects.all()
    serializer_class = StockLevelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_low_stock', 'is_out_of_stock', 'shop_id', 'product']
    search_fields = ['product__name', 'product__code', 'variant__name', 'variant__code']
    ordering_fields = ['product__name', 'current_stock', 'last_stock_update']
    ordering = ['product__name']
    
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
            return StockLevelCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StockLevelUpdateSerializer
        return StockLevelSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        queryset = StockLevel.objects.filter(tenant_id=user.tenant_id)
        
        # Filter by shop_id if provided
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new stock level and publish event to Kafka.
        """
        # Get shop_id from query params
        shop_id = self.request.query_params.get('shop_id')
        if not shop_id:
            return Response(
                {'detail': 'shop_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stock_level = serializer.save(context={'request': self.request, 'shop_id': shop_id})
        
        # Publish stock level created event
        event_data = {
            'event_type': 'stock_level_created',
            'stock_level_id': str(stock_level.id),
            'tenant_id': str(stock_level.tenant_id),
            'shop_id': str(stock_level.shop_id),
            'product_id': str(stock_level.product.id),
            'variant_id': str(stock_level.variant.id) if stock_level.variant else None,
            'current_stock': stock_level.current_stock,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-level:{stock_level.id}', event_data)
        
        return stock_level
    
    def perform_update(self, serializer):
        """
        Update a stock level and publish event to Kafka.
        """
        stock_level = serializer.save()
        
        # Publish stock level updated event
        event_data = {
            'event_type': 'stock_level_updated',
            'stock_level_id': str(stock_level.id),
            'tenant_id': str(stock_level.tenant_id),
            'shop_id': str(stock_level.shop_id),
            'product_id': str(stock_level.product.id),
            'variant_id': str(stock_level.variant.id) if stock_level.variant else None,
            'current_stock': stock_level.current_stock,
            'minimum_stock': stock_level.minimum_stock,
            'maximum_stock': stock_level.maximum_stock,
            'is_low_stock': stock_level.is_low_stock,
            'is_out_of_stock': stock_level.is_out_of_stock,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-level:{stock_level.id}', event_data)
        
        return stock_level
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get low stock items.
        """
        queryset = self.get_queryset().filter(is_low_stock=True, is_out_of_stock=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """
        Get out of stock items.
        """
        queryset = self.get_queryset().filter(is_out_of_stock=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StockTransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stock transactions.
    """
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'shop_id', 'product', 'reference_type']
    search_fields = ['product__name', 'product__code', 'variant__name', 'variant__code', 'notes']
    ordering_fields = ['created_at', 'product__name', 'quantity']
    ordering = ['-created_at']
    
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
            return StockTransactionCreateSerializer
        return StockTransactionSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        queryset = StockTransaction.objects.filter(tenant_id=user.tenant_id)
        
        # Filter by shop_id if provided
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new stock transaction and publish event to Kafka.
        """
        # Get shop_id from query params
        shop_id = self.request.query_params.get('shop_id')
        if not shop_id:
            return Response(
                {'detail': 'shop_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transaction = serializer.save(context={'request': self.request, 'shop_id': shop_id})
        
        # Publish stock transaction created event
        event_data = {
            'event_type': 'stock_transaction_created',
            'transaction_id': str(transaction.id),
            'tenant_id': str(transaction.tenant_id),
            'shop_id': str(transaction.shop_id),
            'product_id': str(transaction.product.id),
            'variant_id': str(transaction.variant.id) if transaction.variant else None,
            'transaction_type': transaction.transaction_type,
            'quantity': transaction.quantity,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-transaction:{transaction.id}', event_data)
        
        return transaction


class StockTransferViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stock transfers.
    """
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'source_shop_id', 'destination_shop_id', 'transfer_date']
    search_fields = ['reference_number', 'notes']
    ordering_fields = ['transfer_date', 'created_at', 'status']
    ordering = ['-transfer_date', '-created_at']
    
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
            return StockTransferCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StockTransferUpdateSerializer
        return StockTransferSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        queryset = StockTransfer.objects.filter(tenant_id=user.tenant_id)
        
        # Filter by shop_id if provided
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(
                models.Q(source_shop_id=shop_id) | models.Q(destination_shop_id=shop_id)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new stock transfer and publish event to Kafka.
        """
        transfer = serializer.save(context={'request': self.request})
        
        # Publish stock transfer created event
        event_data = {
            'event_type': 'stock_transfer_created',
            'transfer_id': str(transfer.id),
            'tenant_id': str(transfer.tenant_id),
            'source_shop_id': str(transfer.source_shop_id),
            'destination_shop_id': str(transfer.destination_shop_id),
            'status': transfer.status,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-transfer:{transfer.id}', event_data)
        
        return transfer
    
    def perform_update(self, serializer):
        """
        Update a stock transfer and publish event to Kafka.
        """
        transfer = serializer.save(context={'request': self.request})
        
        # Publish stock transfer updated event
        event_data = {
            'event_type': 'stock_transfer_updated',
            'transfer_id': str(transfer.id),
            'tenant_id': str(transfer.tenant_id),
            'source_shop_id': str(transfer.source_shop_id),
            'destination_shop_id': str(transfer.destination_shop_id),
            'status': transfer.status,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-transfer:{transfer.id}', event_data)
        
        return transfer
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a stock transfer.
        """
        transfer = self.get_object()
        
        if transfer.status in ['completed', 'cancelled']:
            return Response(
                {'detail': f"Cannot cancel a transfer with status '{transfer.status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update transfer status
        transfer.status = 'cancelled'
        transfer.save()
        
        # If transfer was in_transit, revert the stock transactions
        if transfer.status == 'in_transit':
            serializer = StockTransferUpdateSerializer(
                transfer,
                data={'status': 'cancelled'},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
        # Publish stock transfer cancelled event
        event_data = {
            'event_type': 'stock_transfer_cancelled',
            'transfer_id': str(transfer.id),
            'tenant_id': str(transfer.tenant_id),
            'source_shop_id': str(transfer.source_shop_id),
            'destination_shop_id': str(transfer.destination_shop_id),
            'cancelled_by': str(request.user.id)
        }
        publish_event('inventory-events', f'stock-transfer:{transfer.id}', event_data)
        
        return Response({'message': 'Stock transfer cancelled successfully.'}, status=status.HTTP_200_OK)


class StockAdjustmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing stock adjustments.
    """
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['adjustment_type', 'shop_id', 'adjustment_date']
    search_fields = ['reference_number', 'notes']
    ordering_fields = ['adjustment_date', 'created_at', 'adjustment_type']
    ordering = ['-adjustment_date', '-created_at']
    
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
            return StockAdjustmentCreateSerializer
        return StockAdjustmentSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        queryset = StockAdjustment.objects.filter(tenant_id=user.tenant_id)
        
        # Filter by shop_id if provided
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Create a new stock adjustment and publish event to Kafka.
        """
        # Get shop_id from query params
        shop_id = self.request.query_params.get('shop_id')
        if not shop_id:
            return Response(
                {'detail': 'shop_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        adjustment = serializer.save(context={'request': self.request, 'shop_id': shop_id})
        
        # Publish stock adjustment created event
        event_data = {
            'event_type': 'stock_adjustment_created',
            'adjustment_id': str(adjustment.id),
            'tenant_id': str(adjustment.tenant_id),
            'shop_id': str(adjustment.shop_id),
            'adjustment_type': adjustment.adjustment_type,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'stock-adjustment:{adjustment.id}', event_data)
        
        return adjustment