from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tenant, BillingPlan, TenantBillingHistory, TenantActivity
from .serializers import (
    TenantSerializer, TenantCreateSerializer, TenantUpdateSerializer,
    BillingPlanSerializer, TenantBillingHistorySerializer, TenantActivitySerializer
)
from users.permissions import IsSaasAdmin


class BillingPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing billing plans.
    """
    queryset = BillingPlan.objects.all()
    serializer_class = BillingPlanSerializer
    permission_classes = [IsAuthenticated, IsSaasAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price_monthly', 'price_yearly', 'created_at']
    ordering = ['price_monthly']


class TenantViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tenants.
    """
    queryset = Tenant.objects.all()
    permission_classes = [IsAuthenticated, IsSaasAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_active', 'is_trial']
    search_fields = ['name', 'business_name', 'contact_name', 'contact_email']
    ordering_fields = ['name', 'created_at', 'subscription_end_date']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TenantCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TenantUpdateSerializer
        return TenantSerializer
    
    @action(detail=True, methods=['patch'])
    def activate(self, request, pk=None):
        """
        Activate a tenant.
        """
        tenant = self.get_object()
        tenant.status = Tenant.STATUS_ACTIVE
        tenant.save()
        
        # Log activity
        TenantActivity.objects.create(
            tenant=tenant,
            user_id=request.user.id,
            activity_type='tenant_activated',
            description=f"Tenant {tenant.name} activated by {request.user.email}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'status': 'tenant activated'})
    
    @action(detail=True, methods=['patch'])
    def suspend(self, request, pk=None):
        """
        Suspend a tenant.
        """
        tenant = self.get_object()
        tenant.status = Tenant.STATUS_SUSPENDED
        tenant.save()
        
        # Log activity
        TenantActivity.objects.create(
            tenant=tenant,
            user_id=request.user.id,
            activity_type='tenant_suspended',
            description=f"Tenant {tenant.name} suspended by {request.user.email}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'status': 'tenant suspended'})
    
    @action(detail=True, methods=['get'])
    def activity(self, request, pk=None):
        """
        Get tenant activity logs.
        """
        tenant = self.get_object()
        activities = TenantActivity.objects.filter(tenant=tenant)
        
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = TenantActivitySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = TenantActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        """
        Get tenant users.
        """
        tenant = self.get_object()
        
        # This would typically use a User model query
        # For now, we'll return a placeholder response
        return Response({'message': 'User listing not implemented yet'})
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """
        Review tenant registration.
        """
        tenant = self.get_object()
        approved = request.data.get('approved', False)
        notes = request.data.get('notes', '')
        
        if approved:
            tenant.status = Tenant.STATUS_ACTIVE
        else:
            tenant.status = Tenant.STATUS_CANCELLED
        
        tenant.notes = notes
        tenant.save()
        
        # Log activity
        activity_type = 'tenant_approved' if approved else 'tenant_rejected'
        description = f"Tenant {tenant.name} {'approved' if approved else 'rejected'} by {request.user.email}"
        
        TenantActivity.objects.create(
            tenant=tenant,
            user_id=request.user.id,
            activity_type=activity_type,
            description=description,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({'status': 'tenant reviewed'})


class TenantBillingHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing tenant billing history.
    """
    queryset = TenantBillingHistory.objects.all()
    serializer_class = TenantBillingHistorySerializer
    permission_classes = [IsAuthenticated, IsSaasAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tenant', 'status']
    ordering_fields = ['invoice_date', 'due_date', 'amount']
    ordering = ['-invoice_date']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset