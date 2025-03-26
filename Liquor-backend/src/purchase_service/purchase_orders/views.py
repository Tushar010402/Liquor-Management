from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import PurchaseOrder, PurchaseOrderItem
from .serializers import PurchaseOrderSerializer, PurchaseOrderItemSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def get_queryset(self):
        """Filter queryset based on tenant and shop"""
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        shop_id = self.request.query_params.get('shop_id')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_items(self, request, pk=None):
        """Add items to an existing purchase order"""
        purchase_order = self.get_object()
        items_data = request.data.get('items', [])
        
        try:
            with transaction.atomic():
                for item_data in items_data:
                    item_data['purchase_order'] = purchase_order.id
                    serializer = PurchaseOrderItemSerializer(data=item_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    
            return Response({'message': 'Items added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all items for a purchase order"""
        purchase_order = self.get_object()
        items = PurchaseOrderItem.objects.filter(purchase_order=purchase_order)
        serializer = PurchaseOrderItemSerializer(items, many=True)
        return Response(serializer.data) 