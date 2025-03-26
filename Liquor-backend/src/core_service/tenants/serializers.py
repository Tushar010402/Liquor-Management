from rest_framework import serializers
from django.utils.text import slugify
from .models import Tenant, TenantSettings


class TenantSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for tenant settings.
    """
    class Meta:
        model = TenantSettings
        exclude = ['tenant', 'id', 'created_at', 'updated_at']


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for tenants.
    """
    settings = TenantSettingsSerializer(read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'slug', 'address', 'city', 'state', 'country', 'postal_code',
            'phone', 'email', 'website', 'business_type', 'tax_id', 'license_number',
            'license_expiry', 'subscription_plan', 'subscription_start_date',
            'subscription_end_date', 'max_shops', 'max_users', 'contact_person_name',
            'contact_person_email', 'contact_person_phone', 'logo', 'primary_color',
            'secondary_color', 'is_active', 'created_at', 'updated_at', 'settings'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class TenantCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new tenant.
    """
    settings = TenantSettingsSerializer(required=False)
    
    class Meta:
        model = Tenant
        fields = [
            'name', 'address', 'city', 'state', 'country', 'postal_code',
            'phone', 'email', 'website', 'business_type', 'tax_id', 'license_number',
            'license_expiry', 'subscription_plan', 'subscription_start_date',
            'subscription_end_date', 'max_shops', 'max_users', 'contact_person_name',
            'contact_person_email', 'contact_person_phone', 'logo', 'primary_color',
            'secondary_color', 'settings'
        ]
    
    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        
        # Generate slug from name
        validated_data['slug'] = slugify(validated_data['name'])
        
        # Create tenant
        tenant = Tenant.objects.create(**validated_data)
        
        # Create settings if provided, otherwise use defaults
        if settings_data:
            TenantSettings.objects.create(tenant=tenant, **settings_data)
        else:
            TenantSettings.objects.create(tenant=tenant)
        
        return tenant


class TenantUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing tenant.
    """
    class Meta:
        model = Tenant
        fields = [
            'name', 'address', 'city', 'state', 'country', 'postal_code',
            'phone', 'email', 'website', 'business_type', 'tax_id', 'license_number',
            'license_expiry', 'subscription_plan', 'subscription_start_date',
            'subscription_end_date', 'max_shops', 'max_users', 'contact_person_name',
            'contact_person_email', 'contact_person_phone', 'logo', 'primary_color',
            'secondary_color', 'is_active'
        ]
    
    def update(self, instance, validated_data):
        # Update slug if name is changed
        if 'name' in validated_data and validated_data['name'] != instance.name:
            validated_data['slug'] = slugify(validated_data['name'])
        
        return super().update(instance, validated_data)


class TenantSettingsUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating tenant settings.
    """
    class Meta:
        model = TenantSettings
        exclude = ['tenant', 'id', 'created_at', 'updated_at']