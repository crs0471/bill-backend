from rest_framework import serializers
from bill.models import Bill, Bill_product


class BillProductSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Bill_product
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    products = BillProductSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Bill
        fields = '__all__'
