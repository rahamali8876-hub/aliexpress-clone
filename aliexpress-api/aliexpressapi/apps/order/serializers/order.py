from rest_framework import serializers
from apps.order.models.order import Order
from apps.order.serializers.order_item import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_price",
            "created_at",
            "items",
        ]
        read_only_fields = fields
