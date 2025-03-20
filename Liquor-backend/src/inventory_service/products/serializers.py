from rest_framework import serializers
from django.utils import timezone
from .models import (
    ProductCategory, ProductType, Product, ProductVariant,
    ProductAttribute, ProductAttributeValue, ProductPriceHistory
)


class ProductCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories.
    """
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = ProductCategory
        fields = ['id', 'tenant_id', 'name', 'description', 'parent', 'parent_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at', 'parent_name']


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product categories.
    """
    class Meta:
        model = ProductCategory
        fields = ['name', 'description', 'parent']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return ProductCategory.objects.create(**validated_data)


class ProductTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for product types.
    """
    class Meta:
        model = ProductType
        fields = ['id', 'tenant_id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class ProductTypeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product types.
    """
    class Meta:
        model = ProductType
        fields = ['name', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return ProductType.objects.create(**validated_data)


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for product attributes.
    """
    class Meta:
        model = ProductAttribute
        fields = ['id', 'tenant_id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class ProductAttributeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product attributes.
    """
    class Meta:
        model = ProductAttribute
        fields = ['name', 'description']
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        return ProductAttribute.objects.create(**validated_data)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Serializer for product attribute values.
    """
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'attribute_name']


class ProductAttributeValueCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product attribute values.
    """
    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value']
    
    def create(self, validated_data):
        product = self.context['product']
        
        # Add tenant_id from the product
        validated_data['tenant_id'] = product.tenant_id
        
        # Create product attribute value
        return ProductAttributeValue.objects.create(product=product, **validated_data)


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for product variants.
    """
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'tenant_id', 'product', 'name', 'code', 'barcode',
            'mrp', 'selling_price', 'purchase_price', 'volume_ml',
            'weight_grams', 'image', 'is_available', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'tenant_id', 'created_at', 'updated_at']


class ProductVariantCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating product variants.
    """
    class Meta:
        model = ProductVariant
        fields = [
            'name', 'code', 'barcode', 'mrp', 'selling_price',
            'purchase_price', 'volume_ml', 'weight_grams', 'image',
            'is_available'
        ]
    
    def create(self, validated_data):
        product = self.context['product']
        
        # Add tenant_id from the product
        validated_data['tenant_id'] = product.tenant_id
        
        # Create product variant
        return ProductVariant.objects.create(product=product, **validated_data)


class ProductPriceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for product price history.
    """
    class Meta:
        model = ProductPriceHistory
        fields = [
            'id', 'mrp', 'selling_price', 'purchase_price',
            'effective_from', 'effective_to', 'changed_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for products.
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_name = serializers.CharField(source='product_type.name', read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'tenant_id', 'name', 'code', 'barcode', 'description',
            'brand', 'brand_name', 'category', 'category_name',
            'product_type', 'product_type_name', 'mrp', 'selling_price',
            'purchase_price', 'tax_rate', 'volume_ml', 'weight_grams',
            'alcohol_percentage', 'image', 'is_available', 'is_active',
            'created_at', 'updated_at', 'variants', 'attribute_values'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'created_at', 'updated_at',
            'brand_name', 'category_name', 'product_type_name',
            'variants', 'attribute_values'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating products.
    """
    class Meta:
        model = Product
        fields = [
            'name', 'code', 'barcode', 'description', 'brand', 'category',
            'product_type', 'mrp', 'selling_price', 'purchase_price',
            'tax_rate', 'volume_ml', 'weight_grams', 'alcohol_percentage',
            'image', 'is_available'
        ]
    
    def create(self, validated_data):
        # Add tenant_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        
        # Create product
        product = Product.objects.create(**validated_data)
        
        # Create price history
        ProductPriceHistory.objects.create(
            product=product,
            tenant_id=product.tenant_id,
            mrp=product.mrp,
            selling_price=product.selling_price,
            purchase_price=product.purchase_price,
            effective_from=timezone.now(),
            changed_by=self.context['request'].user.id
        )
        
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating products.
    """
    class Meta:
        model = Product
        fields = [
            'name', 'barcode', 'description', 'category', 'product_type',
            'mrp', 'selling_price', 'purchase_price', 'tax_rate',
            'volume_ml', 'weight_grams', 'alcohol_percentage',
            'image', 'is_available', 'is_active'
        ]
    
    def update(self, instance, validated_data):
        # Check if prices have changed
        price_changed = False
        for price_field in ['mrp', 'selling_price', 'purchase_price']:
            if price_field in validated_data and getattr(instance, price_field) != validated_data[price_field]:
                price_changed = True
                break
        
        # Update product
        product = super().update(instance, validated_data)
        
        # Create price history if prices have changed
        if price_changed:
            # Close previous price history
            ProductPriceHistory.objects.filter(
                product=product,
                effective_to__isnull=True
            ).update(effective_to=timezone.now())
            
            # Create new price history
            ProductPriceHistory.objects.create(
                product=product,
                tenant_id=product.tenant_id,
                mrp=product.mrp,
                selling_price=product.selling_price,
                purchase_price=product.purchase_price,
                effective_from=timezone.now(),
                changed_by=self.context['request'].user.id
            )
        
        return product