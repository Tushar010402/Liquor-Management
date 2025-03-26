from rest_framework import serializers
from .models import GoodsReceipt, GoodsReceiptItem, QualityCheck

class GoodsReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceiptItem
        fields = '__all__'
        read_only_fields = ('line_number',)

class GoodsReceiptSerializer(serializers.ModelSerializer):
    items = GoodsReceiptItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = GoodsReceipt
        fields = '__all__'
        read_only_fields = ('receipt_number',)

class QualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityCheck
        fields = '__all__' 