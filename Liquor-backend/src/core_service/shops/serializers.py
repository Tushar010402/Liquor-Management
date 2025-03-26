from rest_framework import serializers
from .models import Shop, ShopOperatingHours, ShopHoliday, ShopSettings


class ShopOperatingHoursSerializer(serializers.ModelSerializer):
    """
    Serializer for shop operating hours.
    """
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = ShopOperatingHours
        fields = ['id', 'day_of_week', 'day_name', 'opening_time', 'closing_time', 'is_closed']
        read_only_fields = ['id']


class ShopHolidaySerializer(serializers.ModelSerializer):
    """
    Serializer for shop holidays.
    """
    class Meta:
        model = ShopHoliday
        fields = ['id', 'name', 'date', 'description']
        read_only_fields = ['id']


class ShopSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for shop settings.
    """
    class Meta:
        model = ShopSettings
        exclude = ['id', 'shop', 'tenant_id', 'created_at', 'updated_at', 'is_active']


class ShopSerializer(serializers.ModelSerializer):
    """
    Serializer for shops.
    """
    operating_hours = ShopOperatingHoursSerializer(many=True, read_only=True)
    holidays = ShopHolidaySerializer(many=True, read_only=True)
    settings = ShopSettingsSerializer(read_only=True)
    
    class Meta:
        model = Shop
        fields = [
            'id', 'tenant_id', 'name', 'code', 'address', 'city', 'state', 'country',
            'postal_code', 'phone', 'email', 'latitude', 'longitude', 'license_number',
            'license_expiry', 'tax_id', 'manager_id', 'manager_name', 'manager_phone',
            'manager_email', 'is_open', 'is_active', 'created_at', 'updated_at',
            'operating_hours', 'holidays', 'settings'
        ]
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class ShopCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new shop.
    """
    operating_hours = ShopOperatingHoursSerializer(many=True, required=False)
    settings = ShopSettingsSerializer(required=False)
    
    class Meta:
        model = Shop
        fields = [
            'name', 'code', 'address', 'city', 'state', 'country', 'postal_code',
            'phone', 'email', 'latitude', 'longitude', 'license_number',
            'license_expiry', 'tax_id', 'manager_id', 'manager_name', 'manager_phone',
            'manager_email', 'is_open', 'operating_hours', 'settings'
        ]
    
    def create(self, validated_data):
        operating_hours_data = validated_data.pop('operating_hours', [])
        settings_data = validated_data.pop('settings', None)
        
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        
        # Create shop
        shop = Shop.objects.create(**validated_data)
        
        # Create operating hours
        for hours_data in operating_hours_data:
            ShopOperatingHours.objects.create(
                shop=shop,
                tenant_id=shop.tenant_id,
                **hours_data
            )
        
        # Create settings
        if settings_data:
            ShopSettings.objects.create(
                shop=shop,
                tenant_id=shop.tenant_id,
                **settings_data
            )
        else:
            ShopSettings.objects.create(
                shop=shop,
                tenant_id=shop.tenant_id
            )
        
        return shop


class ShopUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing shop.
    """
    class Meta:
        model = Shop
        fields = [
            'name', 'address', 'city', 'state', 'country', 'postal_code',
            'phone', 'email', 'latitude', 'longitude', 'license_number',
            'license_expiry', 'tax_id', 'manager_id', 'manager_name', 'manager_phone',
            'manager_email', 'is_open', 'is_active'
        ]


class ShopOperatingHoursCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating shop operating hours.
    """
    class Meta:
        model = ShopOperatingHours
        fields = ['day_of_week', 'opening_time', 'closing_time', 'is_closed']
    
    def create(self, validated_data):
        shop = self.context['shop']
        return ShopOperatingHours.objects.create(
            shop=shop,
            tenant_id=shop.tenant_id,
            **validated_data
        )


class ShopHolidayCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating shop holidays.
    """
    class Meta:
        model = ShopHoliday
        fields = ['name', 'date', 'description']
    
    def create(self, validated_data):
        shop = self.context['shop']
        return ShopHoliday.objects.create(
            shop=shop,
            tenant_id=shop.tenant_id,
            **validated_data
        )


class ShopSettingsUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating shop settings.
    """
    class Meta:
        model = ShopSettings
        exclude = ['id', 'shop', 'tenant_id', 'created_at', 'updated_at', 'is_active']