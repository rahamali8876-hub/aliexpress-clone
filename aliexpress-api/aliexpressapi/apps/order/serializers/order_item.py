from rest_framework import serializers
from apps.order.models.order_item import OrderItem
from apps.products.serializers.product_variants import ProductVariantSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_variant",
            "quantity",
            "unit_price",
            "subtotal",
        ]
        read_only_fields = fields
