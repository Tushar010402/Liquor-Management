from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from common.utils.kafka_utils import publish_event
from common.permissions import IsTenantUser, CanManageInventory
from .models import (
    SupplierCategory, Supplier, SupplierContact,
    SupplierBankAccount, SupplierDocument
)
from .serializers import (
    SupplierCategorySerializer, SupplierCategoryCreateSerializer,
    SupplierSerializer, SupplierCreateSerializer, SupplierUpdateSerializer,
    SupplierContactSerializer, SupplierContactCreateSerializer,
    SupplierBankAccountSerializer, SupplierBankAccountCreateSerializer,
    SupplierDocumentSerializer, SupplierDocumentCreateSerializer
)


class SupplierCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing supplier categories.
    """
    queryset = SupplierCategory.objects.all()
    serializer_class = SupplierCategorySerializer
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
            return SupplierCategoryCreateSerializer
        return SupplierCategorySerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return SupplierCategory.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new supplier category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish supplier category created event
        event_data = {
            'event_type': 'supplier_category_created',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier-category:{category.id}', event_data)
        
        return category
    
    def perform_update(self, serializer):
        """
        Update a supplier category and publish event to Kafka.
        """
        category = serializer.save()
        
        # Publish supplier category updated event
        event_data = {
            'event_type': 'supplier_category_updated',
            'category_id': str(category.id),
            'tenant_id': str(category.tenant_id),
            'name': category.name,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier-category:{category.id}', event_data)
        
        return category
    
    def perform_destroy(self, instance):
        """
        Soft delete a supplier category by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish supplier category deactivated event
        event_data = {
            'event_type': 'supplier_category_deactivated',
            'category_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier-category:{instance.id}', event_data)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing suppliers.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_approved', 'category', 'city', 'state', 'country']
    search_fields = ['name', 'code', 'contact_person', 'phone', 'email', 'tax_id', 'license_number']
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
            return SupplierCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SupplierUpdateSerializer
        return SupplierSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user's tenant.
        """
        user = self.request.user
        return Supplier.objects.filter(tenant_id=user.tenant_id)
    
    def perform_create(self, serializer):
        """
        Create a new supplier and publish event to Kafka.
        """
        supplier = serializer.save()
        
        # Publish supplier created event
        event_data = {
            'event_type': 'supplier_created',
            'supplier_id': str(supplier.id),
            'tenant_id': str(supplier.tenant_id),
            'name': supplier.name,
            'code': supplier.code,
            'created_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
        
        return supplier
    
    def perform_update(self, serializer):
        """
        Update a supplier and publish event to Kafka.
        """
        supplier = serializer.save()
        
        # Publish supplier updated event
        event_data = {
            'event_type': 'supplier_updated',
            'supplier_id': str(supplier.id),
            'tenant_id': str(supplier.tenant_id),
            'name': supplier.name,
            'code': supplier.code,
            'updated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
        
        return supplier
    
    def perform_destroy(self, instance):
        """
        Soft delete a supplier by setting is_active to False.
        """
        instance.is_active = False
        instance.save()
        
        # Publish supplier deactivated event
        event_data = {
            'event_type': 'supplier_deactivated',
            'supplier_id': str(instance.id),
            'tenant_id': str(instance.tenant_id),
            'name': instance.name,
            'code': instance.code,
            'deactivated_by': str(self.request.user.id)
        }
        publish_event('inventory-events', f'supplier:{instance.id}', event_data)
    
    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        """
        Get contacts for a supplier.
        """
        supplier = self.get_object()
        contacts = SupplierContact.objects.filter(supplier=supplier)
        serializer = SupplierContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_contact(self, request, pk=None):
        """
        Add a contact to a supplier.
        """
        supplier = self.get_object()
        serializer = SupplierContactCreateSerializer(
            data=request.data,
            context={'supplier': supplier}
        )
        
        if serializer.is_valid():
            contact = serializer.save()
            
            # Publish supplier contact added event
            event_data = {
                'event_type': 'supplier_contact_added',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'contact_id': str(contact.id),
                'name': contact.name,
                'is_primary': contact.is_primary,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(
                SupplierContactSerializer(contact).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-contact/(?P<contact_id>[^/.]+)')
    def remove_contact(self, request, pk=None, contact_id=None):
        """
        Remove a contact from a supplier.
        """
        supplier = self.get_object()
        try:
            contact = SupplierContact.objects.get(id=contact_id, supplier=supplier)
            contact_name = contact.name
            contact.delete()
            
            # Publish supplier contact removed event
            event_data = {
                'event_type': 'supplier_contact_removed',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'contact_id': contact_id,
                'name': contact_name,
                'removed_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SupplierContact.DoesNotExist:
            return Response(
                {'detail': 'Contact not found for this supplier.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def bank_accounts(self, request, pk=None):
        """
        Get bank accounts for a supplier.
        """
        supplier = self.get_object()
        bank_accounts = SupplierBankAccount.objects.filter(supplier=supplier)
        serializer = SupplierBankAccountSerializer(bank_accounts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_bank_account(self, request, pk=None):
        """
        Add a bank account to a supplier.
        """
        supplier = self.get_object()
        serializer = SupplierBankAccountCreateSerializer(
            data=request.data,
            context={'supplier': supplier}
        )
        
        if serializer.is_valid():
            bank_account = serializer.save()
            
            # Publish supplier bank account added event
            event_data = {
                'event_type': 'supplier_bank_account_added',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'bank_account_id': str(bank_account.id),
                'bank_name': bank_account.bank_name,
                'account_number': bank_account.account_number,
                'is_primary': bank_account.is_primary,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(
                SupplierBankAccountSerializer(bank_account).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-bank-account/(?P<bank_account_id>[^/.]+)')
    def remove_bank_account(self, request, pk=None, bank_account_id=None):
        """
        Remove a bank account from a supplier.
        """
        supplier = self.get_object()
        try:
            bank_account = SupplierBankAccount.objects.get(id=bank_account_id, supplier=supplier)
            bank_name = bank_account.bank_name
            account_number = bank_account.account_number
            bank_account.delete()
            
            # Publish supplier bank account removed event
            event_data = {
                'event_type': 'supplier_bank_account_removed',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'bank_account_id': bank_account_id,
                'bank_name': bank_name,
                'account_number': account_number,
                'removed_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SupplierBankAccount.DoesNotExist:
            return Response(
                {'detail': 'Bank account not found for this supplier.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        Get documents for a supplier.
        """
        supplier = self.get_object()
        documents = SupplierDocument.objects.filter(supplier=supplier)
        serializer = SupplierDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_document(self, request, pk=None):
        """
        Add a document to a supplier.
        """
        supplier = self.get_object()
        serializer = SupplierDocumentCreateSerializer(
            data=request.data,
            context={'supplier': supplier}
        )
        
        if serializer.is_valid():
            document = serializer.save()
            
            # Publish supplier document added event
            event_data = {
                'event_type': 'supplier_document_added',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'document_id': str(document.id),
                'name': document.name,
                'document_type': document.document_type,
                'added_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(
                SupplierDocumentSerializer(document).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='remove-document/(?P<document_id>[^/.]+)')
    def remove_document(self, request, pk=None, document_id=None):
        """
        Remove a document from a supplier.
        """
        supplier = self.get_object()
        try:
            document = SupplierDocument.objects.get(id=document_id, supplier=supplier)
            document_name = document.name
            document_type = document.document_type
            document.delete()
            
            # Publish supplier document removed event
            event_data = {
                'event_type': 'supplier_document_removed',
                'supplier_id': str(supplier.id),
                'tenant_id': str(supplier.tenant_id),
                'document_id': document_id,
                'name': document_name,
                'document_type': document_type,
                'removed_by': str(request.user.id)
            }
            publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except SupplierDocument.DoesNotExist:
            return Response(
                {'detail': 'Document not found for this supplier.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Approve a supplier.
        """
        supplier = self.get_object()
        supplier.is_approved = True
        supplier.save()
        
        # Publish supplier approved event
        event_data = {
            'event_type': 'supplier_approved',
            'supplier_id': str(supplier.id),
            'tenant_id': str(supplier.tenant_id),
            'name': supplier.name,
            'code': supplier.code,
            'approved_by': str(request.user.id)
        }
        publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
        
        return Response({'message': 'Supplier approved successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Reject a supplier.
        """
        supplier = self.get_object()
        supplier.is_approved = False
        supplier.save()
        
        # Publish supplier rejected event
        event_data = {
            'event_type': 'supplier_rejected',
            'supplier_id': str(supplier.id),
            'tenant_id': str(supplier.tenant_id),
            'name': supplier.name,
            'code': supplier.code,
            'rejected_by': str(request.user.id)
        }
        publish_event('inventory-events', f'supplier:{supplier.id}', event_data)
        
        return Response({'message': 'Supplier rejected successfully.'}, status=status.HTTP_200_OK)