from rest_framework import serializers
from .models import Shop, ShopSettings, ShopActivity


class ShopSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for ShopSettings model.
    """
    class Meta:
        model = ShopSettings
        fields = [
            'id', 'enable_low_stock_alerts', 'low_stock_threshold',
            'enable_expiry_alerts', 'expiry_alert_days',
            'default_tax_rate', 'enable_discounts', 'max_discount_percentage',
            'require_discount_approval', 'discount_approval_threshold',
            'require_sales_approval', 'require_stock_adjustment_approval',
            'require_return_approval',
            'receipt_header', 'receipt_footer', 'show_tax_on_receipt',
            'settings_json',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShopSerializer(serializers.ModelSerializer):
    """
    Serializer for Shop model.
    """
    settings = ShopSettingsSerializer(read_only=True)
    
    class Meta:
        model = Shop
        fields = [
            'id', 'tenant_id', 'name', 'code', 'shop_type', 'status',
            'address', 'city', 'state', 'country', 'postal_code',
            'latitude', 'longitude',
            'phone', 'email',
            'license_number', 'license_type', 'license_expiry',
            'opening_time', 'closing_time',
            'is_open_on_sunday', 'is_open_on_monday', 'is_open_on_tuesday',
            'is_open_on_wednesday', 'is_open_on_thursday', 'is_open_on_friday',
            'is_open_on_saturday',
            'description', 'image',
            'created_by', 'notes',
            'settings',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShopCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new shop.
    """
    settings = ShopSettingsSerializer(required=False)
    
    class Meta:
        model = Shop
        fields = [
            'tenant_id', 'name', 'code', 'shop_type', 'status',
            'address', 'city', 'state', 'country', 'postal_code',
            'latitude', 'longitude',
            'phone', 'email',
            'license_number', 'license_type', 'license_expiry',
            'opening_time', 'closing_time',
            'is_open_on_sunday', 'is_open_on_monday', 'is_open_on_tuesday',
            'is_open_on_wednesday', 'is_open_on_thursday', 'is_open_on_friday',
            'is_open_on_saturday',
            'description', 'image',
            'created_by', 'notes',
            'settings'
        ]
    
    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        shop = Shop.objects.create(**validated_data)
        
        if settings_data:
            ShopSettings.objects.create(shop=shop, **settings_data)
        else:
            # Create default settings
            ShopSettings.objects.create(shop=shop)
        
        return shop


class ShopUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a shop.
    """
    settings = ShopSettingsSerializer(required=False)
    
    class Meta:
        model = Shop
        fields = [
            'name', 'shop_type', 'status',
            'address', 'city', 'state', 'country', 'postal_code',
            'latitude', 'longitude',
            'phone', 'email',
            'license_number', 'license_type', 'license_expiry',
            'opening_time', 'closing_time',
            'is_open_on_sunday', 'is_open_on_monday', 'is_open_on_tuesday',
            'is_open_on_wednesday', 'is_open_on_thursday', 'is_open_on_friday',
            'is_open_on_saturday',
            'description', 'image',
            'notes', 'is_active',
            'settings'
        ]
    
    def update(self, instance, validated_data):
        settings_data = validated_data.pop('settings', None)
        
        # Update shop instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update settings if provided
        if settings_data and hasattr(instance, 'settings'):
            settings = instance.settings
            for attr, value in settings_data.items():
                setattr(settings, attr, value)
            settings.save()
        
        return instance


class ShopActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for ShopActivity model.
    """
    shop_name = serializers.CharField(source='shop.name', read_only=True)
    
    class Meta:
        model = ShopActivity
        fields = [
            'id', 'shop', 'shop_name', 'user_id', 'activity_type',
            'description', 'ip_address', 'metadata',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']