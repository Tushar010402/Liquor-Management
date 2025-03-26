from rest_framework import serializers
from .models import (
    SupplierCategory, Supplier, SupplierContact,
    SupplierBankAccount, SupplierDocument
)


class SupplierCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for supplier categories.
    """
    class Meta:
        model = SupplierCategory
        fields = ['id', 'tenant_id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class SupplierCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating supplier categories.
    """
    class Meta:
        model = SupplierCategory
        fields = ['name', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return SupplierCategory.objects.create(**validated_data)


class SupplierContactSerializer(serializers.ModelSerializer):
    """
    Serializer for supplier contacts.
    """
    class Meta:
        model = SupplierContact
        fields = ['id', 'name', 'designation', 'phone', 'email', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierContactCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating supplier contacts.
    """
    class Meta:
        model = SupplierContact
        fields = ['name', 'designation', 'phone', 'email', 'is_primary']
    
    def create(self, validated_data):
        supplier = self.context['supplier']
        
        # Add tenant_id from the supplier
        validated_data['tenant_id'] = supplier.tenant_id
        
        # Create supplier contact
        contact = SupplierContact.objects.create(supplier=supplier, **validated_data)
        
        # If this is set as primary, unset other primary contacts
        if contact.is_primary:
            SupplierContact.objects.filter(
                supplier=supplier,
                is_primary=True
            ).exclude(id=contact.id).update(is_primary=False)
        
        return contact


class SupplierBankAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for supplier bank accounts.
    """
    class Meta:
        model = SupplierBankAccount
        fields = ['id', 'bank_name', 'account_number', 'account_name', 'branch', 'ifsc_code', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierBankAccountCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating supplier bank accounts.
    """
    class Meta:
        model = SupplierBankAccount
        fields = ['bank_name', 'account_number', 'account_name', 'branch', 'ifsc_code', 'is_primary']
    
    def create(self, validated_data):
        supplier = self.context['supplier']
        
        # Add tenant_id from the supplier
        validated_data['tenant_id'] = supplier.tenant_id
        
        # Create supplier bank account
        bank_account = SupplierBankAccount.objects.create(supplier=supplier, **validated_data)
        
        # If this is set as primary, unset other primary bank accounts
        if bank_account.is_primary:
            SupplierBankAccount.objects.filter(
                supplier=supplier,
                is_primary=True
            ).exclude(id=bank_account.id).update(is_primary=False)
        
        return bank_account


class SupplierDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for supplier documents.
    """
    class Meta:
        model = SupplierDocument
        fields = ['id', 'name', 'document_type', 'document', 'expiry_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupplierDocumentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating supplier documents.
    """
    class Meta:
        model = SupplierDocument
        fields = ['name', 'document_type', 'document', 'expiry_date', 'notes']
    
    def create(self, validated_data):
        supplier = self.context['supplier']
        
        # Add tenant_id from the supplier
        validated_data['tenant_id'] = supplier.tenant_id
        
        # Create supplier document
        return SupplierDocument.objects.create(supplier=supplier, **validated_data)


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for suppliers.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    contacts = SupplierContactSerializer(many=True, read_only=True)
    bank_accounts = SupplierBankAccountSerializer(many=True, read_only=True)
    documents = SupplierDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'tenant_id', 'name', 'code', 'category', 'category_name',
            'contact_person', 'phone', 'email', 'website', 'address', 'city',
            'state', 'country', 'postal_code', 'tax_id', 'license_number',
            'license_expiry', 'payment_terms', 'credit_limit', 'credit_days',
            'is_approved', 'notes', 'is_active', 'created_at', 'updated_at',
            'contacts', 'bank_accounts', 'documents'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'created_at', 'updated_at',
            'category_name', 'contacts', 'bank_accounts', 'documents'
        ]


class SupplierCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating suppliers.
    """
    class Meta:
        model = Supplier
        fields = [
            'name', 'code', 'category', 'contact_person', 'phone', 'email',
            'website', 'address', 'city', 'state', 'country', 'postal_code',
            'tax_id', 'license_number', 'license_expiry', 'payment_terms',
            'credit_limit', 'credit_days', 'is_approved', 'notes'
        ]
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return Supplier.objects.create(**validated_data)


class SupplierUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating suppliers.
    """
    class Meta:
        model = Supplier
        fields = [
            'name', 'category', 'contact_person', 'phone', 'email',
            'website', 'address', 'city', 'state', 'country', 'postal_code',
            'tax_id', 'license_number', 'license_expiry', 'payment_terms',
            'credit_limit', 'credit_days', 'is_approved', 'notes', 'is_active'
        ]