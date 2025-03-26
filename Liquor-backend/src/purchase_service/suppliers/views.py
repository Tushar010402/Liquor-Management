from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from .models import Supplier, SupplierProduct, SupplierPayment, SupplierInvoice
from .serializers import (
    SupplierSerializer, SupplierProductSerializer,
    SupplierPaymentSerializer, SupplierInvoiceSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    
    def get_queryset(self):
        """Filter queryset based on tenant"""
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products for a supplier"""
        supplier = self.get_object()
        products = SupplierProduct.objects.filter(supplier=supplier)
        serializer = SupplierProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        """Get all payments for a supplier"""
        supplier = self.get_object()
        payments = SupplierPayment.objects.filter(supplier=supplier)
        serializer = SupplierPaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def invoices(self, request, pk=None):
        """Get all invoices for a supplier"""
        supplier = self.get_object()
        invoices = SupplierInvoice.objects.filter(supplier=supplier)
        serializer = SupplierInvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

class SupplierProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierProduct.objects.all()
    serializer_class = SupplierProductSerializer
    
    def get_queryset(self):
        """Filter queryset based on tenant and supplier"""
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        supplier_id = self.request.query_params.get('supplier_id')
        
        if tenant_id:
            queryset = queryset.filter(supplier__tenant_id=tenant_id)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
            
        return queryset

class SupplierPaymentViewSet(viewsets.ModelViewSet):
    queryset = SupplierPayment.objects.all()
    serializer_class = SupplierPaymentSerializer
    
    def get_queryset(self):
        """Filter queryset based on tenant and supplier"""
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        supplier_id = self.request.query_params.get('supplier_id')
        
        if tenant_id:
            queryset = queryset.filter(supplier__tenant_id=tenant_id)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
            
        return queryset

class SupplierInvoiceViewSet(viewsets.ModelViewSet):
    queryset = SupplierInvoice.objects.all()
    serializer_class = SupplierInvoiceSerializer
    
    def get_queryset(self):
        """Filter queryset based on tenant and supplier"""
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        supplier_id = self.request.query_params.get('supplier_id')
        
        if tenant_id:
            queryset = queryset.filter(supplier__tenant_id=tenant_id)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
            
        return queryset 