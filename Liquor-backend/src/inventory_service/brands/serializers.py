from rest_framework import serializers
from .models import BrandCategory, Brand, BrandSupplier


class BrandCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for brand categories.
    """
    class Meta:
        model = BrandCategory
        fields = ['id', 'tenant_id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class BrandCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating brand categories.
    """
    class Meta:
        model = BrandCategory
        fields = ['name', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return BrandCategory.objects.create(**validated_data)


class BrandSupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for brand suppliers.
    """
    class Meta:
        model = BrandSupplier
        fields = ['id', 'supplier_id', 'supplier_name', 'is_primary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for brands.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    suppliers = BrandSupplierSerializer(many=True, read_only=True)
    
    class Meta:
        model = Brand
        fields = [
            'id', 'tenant_id', 'name', 'code', 'description', 'category', 'category_name',
            'manufacturer', 'country_of_origin', 'website', 'logo', 'is_active',
            'created_at', 'updated_at', 'suppliers'
        ]
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at', 'category_name', 'suppliers']


class BrandCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating brands.
    """
    class Meta:
        model = Brand
        fields = [
            'name', 'code', 'description', 'category', 'manufacturer',
            'country_of_origin', 'website', 'logo'
        ]
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return Brand.objects.create(**validated_data)


class BrandUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating brands.
    """
    class Meta:
        model = Brand
        fields = [
            'name', 'description', 'category', 'manufacturer',
            'country_of_origin', 'website', 'logo', 'is_active'
        ]


class BrandSupplierCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating brand suppliers.
    """
    class Meta:
        model = BrandSupplier
        fields = ['supplier_id', 'supplier_name', 'is_primary']
    
    def create(self, validated_data):
        brand = self.context['brand']
        
        # Add tenant_id from the brand
        validated_data['tenant_id'] = brand.tenant_id
        
        # Create brand supplier
        brand_supplier = BrandSupplier.objects.create(brand=brand, **validated_data)
        
        # If this is set as primary, unset other primary suppliers
        if brand_supplier.is_primary:
            BrandSupplier.objects.filter(
                brand=brand,
                is_primary=True
            ).exclude(id=brand_supplier.id).update(is_primary=False)
        
        return brand_supplier