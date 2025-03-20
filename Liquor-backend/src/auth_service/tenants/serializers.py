from rest_framework import serializers
from .models import Tenant, BillingPlan, TenantBillingHistory, TenantActivity


class BillingPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for BillingPlan model.
    """
    class Meta:
        model = BillingPlan
        fields = [
            'id', 'name', 'description', 'price_monthly', 'price_yearly',
            'max_shops', 'max_users', 'features', 'is_active',
            'created_at', 'updated_at'
        ]


class TenantSerializer(serializers.ModelSerializer):
    """
    Serializer for Tenant model.
    """
    billing_plan_details = BillingPlanSerializer(source='billing_plan', read_only=True)
    
    class Meta:
        model = Tenant
        fields = [
            'id', 'name', 'slug', 'domain', 'status',
            'business_name', 'business_address', 'business_phone', 'business_email',
            'tax_id', 'registration_number',
            'contact_name', 'contact_email', 'contact_phone',
            'billing_plan', 'billing_plan_details', 'billing_cycle',
            'billing_address', 'billing_email',
            'subscription_start_date', 'subscription_end_date',
            'is_trial', 'trial_end_date',
            'logo', 'primary_color', 'secondary_color',
            'created_by', 'notes',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TenantCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new tenant.
    """
    class Meta:
        model = Tenant
        fields = [
            'name', 'slug', 'domain', 'status',
            'business_name', 'business_address', 'business_phone', 'business_email',
            'tax_id', 'registration_number',
            'contact_name', 'contact_email', 'contact_phone',
            'billing_plan', 'billing_cycle',
            'billing_address', 'billing_email',
            'is_trial', 'trial_end_date',
            'logo', 'primary_color', 'secondary_color',
            'created_by', 'notes'
        ]
    
    def create(self, validated_data):
        # Set subscription dates based on billing plan
        # This would be implemented based on your business logic
        return super().create(validated_data)


class TenantUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a tenant.
    """
    class Meta:
        model = Tenant
        fields = [
            'name', 'domain', 'status',
            'business_name', 'business_address', 'business_phone', 'business_email',
            'tax_id', 'registration_number',
            'contact_name', 'contact_email', 'contact_phone',
            'billing_plan', 'billing_cycle',
            'billing_address', 'billing_email',
            'subscription_start_date', 'subscription_end_date',
            'is_trial', 'trial_end_date',
            'logo', 'primary_color', 'secondary_color',
            'notes', 'is_active'
        ]


class TenantBillingHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for TenantBillingHistory model.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    billing_plan_name = serializers.CharField(source='billing_plan.name', read_only=True)
    
    class Meta:
        model = TenantBillingHistory
        fields = [
            'id', 'tenant', 'tenant_name', 'billing_plan', 'billing_plan_name',
            'amount', 'status', 'invoice_number', 'invoice_date', 'due_date',
            'payment_date', 'payment_method', 'payment_reference',
            'billing_period_start', 'billing_period_end', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TenantActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for TenantActivity model.
    """
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = TenantActivity
        fields = [
            'id', 'tenant', 'tenant_name', 'user_id', 'activity_type',
            'description', 'ip_address', 'user_agent', 'metadata',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']