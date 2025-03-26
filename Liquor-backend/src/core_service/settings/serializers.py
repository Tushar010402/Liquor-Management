from rest_framework import serializers
from .models import SystemSetting, TenantSetting, EmailTemplate, NotificationTemplate


class SystemSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for system settings.
    """
    class Meta:
        model = SystemSetting
        fields = ['id', 'key', 'value', 'description', 'is_public', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemSettingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating system settings.
    """
    class Meta:
        model = SystemSetting
        fields = ['key', 'value', 'description', 'is_public']


class TenantSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for tenant settings.
    """
    class Meta:
        model = TenantSetting
        fields = ['id', 'tenant_id', 'key', 'value', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class TenantSettingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating tenant settings.
    """
    class Meta:
        model = TenantSetting
        fields = ['key', 'value', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return TenantSetting.objects.create(**validated_data)


class EmailTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for email templates.
    """
    class Meta:
        model = EmailTemplate
        fields = ['id', 'tenant_id', 'name', 'subject', 'body', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class EmailTemplateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating email templates.
    """
    class Meta:
        model = EmailTemplate
        fields = ['name', 'subject', 'body', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return EmailTemplate.objects.create(**validated_data)


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for notification templates.
    """
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'tenant_id', 'name', 'title', 'body', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class NotificationTemplateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notification templates.
    """
    class Meta:
        model = NotificationTemplate
        fields = ['name', 'title', 'body', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return NotificationTemplate.objects.create(**validated_data)