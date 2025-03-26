from rest_framework import serializers
from .models import Supplier, SupplierProduct, SupplierPayment, SupplierInvoice

class SupplierProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProduct
        fields = '__all__'

class SupplierPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierPayment
        fields = '__all__'

class SupplierInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierInvoice
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    products = SupplierProductSerializer(many=True, read_only=True)
    payments = SupplierPaymentSerializer(many=True, read_only=True)
    invoices = SupplierInvoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('supplier_code',) 