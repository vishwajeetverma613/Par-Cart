from rest_framework import serializers
from order.models import Order, OrderItem
from common.enums import OrderStatus

class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "customer", "total_amount", "status", "created_at", "items"]

    def get_items(self, obj):
        return OrderItem.objects.filter(order=obj).values("product__name", "quantity", "price")
    
   