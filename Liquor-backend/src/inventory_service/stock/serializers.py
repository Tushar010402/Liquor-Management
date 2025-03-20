from rest_framework import serializers
from django.utils import timezone
from .models import (
    StockLevel, StockTransaction, StockTransfer, StockTransferItem,
    StockAdjustment, StockAdjustmentItem
)
from products.models import Product, ProductVariant


class StockLevelSerializer(serializers.ModelSerializer):
    """
    Serializer for stock levels.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True, allow_null=True)
    variant_code = serializers.CharField(source='variant.code', read_only=True, allow_null=True)
    
    class Meta:
        model = StockLevel
        fields = [
            'id', 'tenant_id', 'shop_id', 'product', 'product_name', 'product_code',
            'variant', 'variant_name', 'variant_code', 'current_stock', 'minimum_stock',
            'maximum_stock', 'is_low_stock', 'is_out_of_stock', 'last_stock_update',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'shop_id', 'is_low_stock', 'is_out_of_stock',
            'last_stock_update', 'created_at', 'updated_at'
        ]


class StockLevelCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock levels.
    """
    class Meta:
        model = StockLevel
        fields = [
            'product', 'variant', 'current_stock', 'minimum_stock', 'maximum_stock'
        ]
    
    def create(self, validated_data):
        # Add tenant_id and shop_id from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        validated_data['shop_id'] = self.context['shop_id']
        
        # Create stock level
        return StockLevel.objects.create(**validated_data)


class StockLevelUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating stock levels.
    """
    class Meta:
        model = StockLevel
        fields = ['minimum_stock', 'maximum_stock']


class StockTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for stock transactions.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True, allow_null=True)
    variant_code = serializers.CharField(source='variant.code', read_only=True, allow_null=True)
    
    class Meta:
        model = StockTransaction
        fields = [
            'id', 'tenant_id', 'shop_id', 'product', 'product_name', 'product_code',
            'variant', 'variant_name', 'variant_code', 'transaction_type', 'quantity',
            'reference_id', 'reference_type', 'performed_by', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'shop_id', 'created_at', 'updated_at'
        ]


class StockTransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock transactions.
    """
    class Meta:
        model = StockTransaction
        fields = [
            'product', 'variant', 'transaction_type', 'quantity',
            'reference_id', 'reference_type', 'notes'
        ]
    
    def validate(self, data):
        """
        Validate that the product and variant exist and belong to the same tenant.
        """
        product = data.get('product')
        variant = data.get('variant')
        
        # Check if product exists and belongs to the tenant
        if product.tenant_id != self.context['request'].user.tenant_id:
            raise serializers.ValidationError("Product does not exist or does not belong to your tenant.")
        
        # Check if variant exists and belongs to the product
        if variant and (variant.product != product or variant.tenant_id != self.context['request'].user.tenant_id):
            raise serializers.ValidationError("Variant does not exist or does not belong to the specified product.")
        
        return data
    
    def create(self, validated_data):
        # Add tenant_id, shop_id, and performed_by from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        validated_data['shop_id'] = self.context['shop_id']
        validated_data['performed_by'] = self.context['request'].user.id
        
        # Get product and variant
        product = validated_data['product']
        variant = validated_data.get('variant')
        
        # Get or create stock level
        stock_level, created = StockLevel.objects.get_or_create(
            tenant_id=validated_data['tenant_id'],
            shop_id=validated_data['shop_id'],
            product=product,
            variant=variant,
            defaults={
                'current_stock': 0,
                'minimum_stock': 10,
                'maximum_stock': 100
            }
        )
        
        # Update stock level based on transaction type
        transaction_type = validated_data['transaction_type']
        quantity = validated_data['quantity']
        
        if transaction_type in ['purchase', 'return', 'transfer_in', 'opening_stock']:
            # Increase stock
            stock_level.current_stock += quantity
        elif transaction_type in ['sale', 'transfer_out', 'wastage', 'adjustment']:
            # Decrease stock
            if stock_level.current_stock < quantity:
                raise serializers.ValidationError(f"Insufficient stock. Current stock: {stock_level.current_stock}, Requested: {quantity}")
            stock_level.current_stock -= quantity
        
        # Save stock level
        stock_level.save()
        
        # Create stock transaction
        return StockTransaction.objects.create(**validated_data)


class StockTransferItemSerializer(serializers.ModelSerializer):
    """
    Serializer for stock transfer items.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True, allow_null=True)
    variant_code = serializers.CharField(source='variant.code', read_only=True, allow_null=True)
    
    class Meta:
        model = StockTransferItem
        fields = [
            'id', 'product', 'product_name', 'product_code', 'variant',
            'variant_name', 'variant_code', 'quantity', 'received_quantity',
            'is_received', 'notes'
        ]
        read_only_fields = ['id', 'received_quantity', 'is_received']


class StockTransferItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock transfer items.
    """
    class Meta:
        model = StockTransferItem
        fields = ['product', 'variant', 'quantity', 'notes']
    
    def validate(self, data):
        """
        Validate that the product and variant exist and belong to the same tenant.
        """
        product = data.get('product')
        variant = data.get('variant')
        
        # Check if product exists and belongs to the tenant
        if product.tenant_id != self.context['request'].user.tenant_id:
            raise serializers.ValidationError("Product does not exist or does not belong to your tenant.")
        
        # Check if variant exists and belongs to the product
        if variant and (variant.product != product or variant.tenant_id != self.context['request'].user.tenant_id):
            raise serializers.ValidationError("Variant does not exist or does not belong to the specified product.")
        
        # Check if there is sufficient stock
        try:
            stock_level = StockLevel.objects.get(
                tenant_id=self.context['request'].user.tenant_id,
                shop_id=self.context['source_shop_id'],
                product=product,
                variant=variant
            )
            
            if stock_level.current_stock < data['quantity']:
                raise serializers.ValidationError(f"Insufficient stock for {product.name}. Current stock: {stock_level.current_stock}, Requested: {data['quantity']}")
        except StockLevel.DoesNotExist:
            raise serializers.ValidationError(f"No stock found for {product.name} in the source shop.")
        
        return data


class StockTransferSerializer(serializers.ModelSerializer):
    """
    Serializer for stock transfers.
    """
    items = StockTransferItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StockTransfer
        fields = [
            'id', 'tenant_id', 'shop_id', 'source_shop_id', 'destination_shop_id',
            'transfer_date', 'status', 'reference_number', 'initiated_by',
            'notes', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'shop_id', 'initiated_by', 'created_at', 'updated_at', 'items'
        ]


class StockTransferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock transfers.
    """
    items = StockTransferItemCreateSerializer(many=True)
    
    class Meta:
        model = StockTransfer
        fields = [
            'source_shop_id', 'destination_shop_id', 'transfer_date',
            'reference_number', 'notes', 'items'
        ]
    
    def validate(self, data):
        """
        Validate that the source and destination shops are different.
        """
        if data['source_shop_id'] == data['destination_shop_id']:
            raise serializers.ValidationError("Source and destination shops cannot be the same.")
        
        return data
    
    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items')
        
        # Add tenant_id, shop_id, and initiated_by from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        validated_data['shop_id'] = validated_data['source_shop_id']  # Use source shop as the primary shop
        validated_data['initiated_by'] = self.context['request'].user.id
        
        # Create stock transfer
        transfer = StockTransfer.objects.create(**validated_data)
        
        # Create stock transfer items
        for item_data in items_data:
            StockTransferItem.objects.create(
                transfer=transfer,
                tenant_id=transfer.tenant_id,
                shop_id=transfer.shop_id,
                **item_data
            )
        
        return transfer


class StockTransferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating stock transfers.
    """
    class Meta:
        model = StockTransfer
        fields = ['status', 'notes']
    
    def validate(self, data):
        """
        Validate the status transition.
        """
        instance = self.instance
        new_status = data.get('status', instance.status)
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['in_transit', 'cancelled'],
            'in_transit': ['completed', 'cancelled'],
            'completed': [],
            'cancelled': []
        }
        
        if new_status != instance.status and new_status not in valid_transitions[instance.status]:
            raise serializers.ValidationError(f"Invalid status transition from '{instance.status}' to '{new_status}'.")
        
        return data
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # Update transfer
        transfer = super().update(instance, validated_data)
        
        # Handle status change
        if old_status != new_status:
            if new_status == 'in_transit':
                # Create stock transactions for transfer_out
                self._create_transfer_out_transactions(transfer)
            elif new_status == 'completed':
                # Create stock transactions for transfer_in
                self._create_transfer_in_transactions(transfer)
            elif new_status == 'cancelled' and old_status == 'in_transit':
                # Revert transfer_out transactions
                self._revert_transfer_out_transactions(transfer)
        
        return transfer
    
    def _create_transfer_out_transactions(self, transfer):
        """
        Create stock transactions for transfer_out.
        """
        for item in transfer.items.all():
            # Create stock transaction
            StockTransaction.objects.create(
                tenant_id=transfer.tenant_id,
                shop_id=transfer.source_shop_id,
                product=item.product,
                variant=item.variant,
                transaction_type='transfer_out',
                quantity=item.quantity,
                reference_id=transfer.id,
                reference_type='stock_transfer',
                performed_by=self.context['request'].user.id,
                notes=f"Transfer to {transfer.destination_shop_id}"
            )
            
            # Update stock level
            try:
                stock_level = StockLevel.objects.get(
                    tenant_id=transfer.tenant_id,
                    shop_id=transfer.source_shop_id,
                    product=item.product,
                    variant=item.variant
                )
                
                stock_level.current_stock -= item.quantity
                stock_level.save()
            except StockLevel.DoesNotExist:
                pass
    
    def _create_transfer_in_transactions(self, transfer):
        """
        Create stock transactions for transfer_in.
        """
        for item in transfer.items.all():
            # Update item
            item.is_received = True
            item.received_quantity = item.quantity
            item.save()
            
            # Create stock transaction
            StockTransaction.objects.create(
                tenant_id=transfer.tenant_id,
                shop_id=transfer.destination_shop_id,
                product=item.product,
                variant=item.variant,
                transaction_type='transfer_in',
                quantity=item.received_quantity,
                reference_id=transfer.id,
                reference_type='stock_transfer',
                performed_by=self.context['request'].user.id,
                notes=f"Transfer from {transfer.source_shop_id}"
            )
            
            # Update or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                tenant_id=transfer.tenant_id,
                shop_id=transfer.destination_shop_id,
                product=item.product,
                variant=item.variant,
                defaults={
                    'current_stock': 0,
                    'minimum_stock': 10,
                    'maximum_stock': 100
                }
            )
            
            stock_level.current_stock += item.received_quantity
            stock_level.save()
    
    def _revert_transfer_out_transactions(self, transfer):
        """
        Revert transfer_out transactions.
        """
        for item in transfer.items.all():
            # Create stock transaction to revert transfer_out
            StockTransaction.objects.create(
                tenant_id=transfer.tenant_id,
                shop_id=transfer.source_shop_id,
                product=item.product,
                variant=item.variant,
                transaction_type='transfer_in',
                quantity=item.quantity,
                reference_id=transfer.id,
                reference_type='stock_transfer_cancelled',
                performed_by=self.context['request'].user.id,
                notes=f"Cancelled transfer to {transfer.destination_shop_id}"
            )
            
            # Update stock level
            try:
                stock_level = StockLevel.objects.get(
                    tenant_id=transfer.tenant_id,
                    shop_id=transfer.source_shop_id,
                    product=item.product,
                    variant=item.variant
                )
                
                stock_level.current_stock += item.quantity
                stock_level.save()
            except StockLevel.DoesNotExist:
                pass


class StockAdjustmentItemSerializer(serializers.ModelSerializer):
    """
    Serializer for stock adjustment items.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True, allow_null=True)
    variant_code = serializers.CharField(source='variant.code', read_only=True, allow_null=True)
    
    class Meta:
        model = StockAdjustmentItem
        fields = [
            'id', 'product', 'product_name', 'product_code', 'variant',
            'variant_name', 'variant_code', 'previous_quantity', 'new_quantity',
            'difference', 'notes'
        ]
        read_only_fields = ['id', 'previous_quantity', 'difference']


class StockAdjustmentItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock adjustment items.
    """
    class Meta:
        model = StockAdjustmentItem
        fields = ['product', 'variant', 'new_quantity', 'notes']
    
    def validate(self, data):
        """
        Validate that the product and variant exist and belong to the same tenant.
        """
        product = data.get('product')
        variant = data.get('variant')
        
        # Check if product exists and belongs to the tenant
        if product.tenant_id != self.context['request'].user.tenant_id:
            raise serializers.ValidationError("Product does not exist or does not belong to your tenant.")
        
        # Check if variant exists and belongs to the product
        if variant and (variant.product != product or variant.tenant_id != self.context['request'].user.tenant_id):
            raise serializers.ValidationError("Variant does not exist or does not belong to the specified product.")
        
        return data


class StockAdjustmentSerializer(serializers.ModelSerializer):
    """
    Serializer for stock adjustments.
    """
    items = StockAdjustmentItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = [
            'id', 'tenant_id', 'shop_id', 'adjustment_date', 'adjustment_type',
            'reference_number', 'performed_by', 'notes', 'created_at', 'updated_at',
            'items'
        ]
        read_only_fields = [
            'id', 'tenant_id', 'shop_id', 'performed_by', 'created_at', 'updated_at', 'items'
        ]


class StockAdjustmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating stock adjustments.
    """
    items = StockAdjustmentItemCreateSerializer(many=True)
    
    class Meta:
        model = StockAdjustment
        fields = [
            'adjustment_date', 'adjustment_type', 'reference_number', 'notes', 'items'
        ]
    
    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items')
        
        # Add tenant_id, shop_id, and performed_by from the request
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        validated_data['shop_id'] = self.context['shop_id']
        validated_data['performed_by'] = self.context['request'].user.id
        
        # Create stock adjustment
        adjustment = StockAdjustment.objects.create(**validated_data)
        
        # Create stock adjustment items and update stock levels
        for item_data in items_data:
            product = item_data['product']
            variant = item_data.get('variant')
            new_quantity = item_data['new_quantity']
            
            # Get or create stock level
            stock_level, created = StockLevel.objects.get_or_create(
                tenant_id=adjustment.tenant_id,
                shop_id=adjustment.shop_id,
                product=product,
                variant=variant,
                defaults={
                    'current_stock': 0,
                    'minimum_stock': 10,
                    'maximum_stock': 100
                }
            )
            
            # Create adjustment item
            StockAdjustmentItem.objects.create(
                adjustment=adjustment,
                tenant_id=adjustment.tenant_id,
                shop_id=adjustment.shop_id,
                product=product,
                variant=variant,
                previous_quantity=stock_level.current_stock,
                new_quantity=new_quantity,
                notes=item_data.get('notes', '')
            )
            
            # Calculate difference
            difference = new_quantity - stock_level.current_stock
            
            # Create stock transaction
            StockTransaction.objects.create(
                tenant_id=adjustment.tenant_id,
                shop_id=adjustment.shop_id,
                product=product,
                variant=variant,
                transaction_type='adjustment',
                quantity=abs(difference),
                reference_id=adjustment.id,
                reference_type='stock_adjustment',
                performed_by=adjustment.performed_by,
                notes=f"Stock adjustment: {adjustment.adjustment_type}"
            )
            
            # Update stock level
            stock_level.current_stock = new_quantity
            stock_level.save()
        
        return adjustment