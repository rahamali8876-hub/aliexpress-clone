# apps/checkout/repositories/checkout_repository.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
import uuid


class CheckoutRepository:
    def lock_cart(self, cart):
        if cart.is_locked:
            raise ValueError("Cart already checked out")

        cart.is_locked = True
        cart.save(update_fields=["is_locked"])

    def create_order(self, *, cart, user, idempotency_key):
        existing = Order.objects.filter(idempotency_key=idempotency_key).first()

        if existing:
            return existing, False

        order = Order.objects.create(
            user=user if user.is_authenticated else None,
            total_price=cart.total_price,
            idempotency_key=idempotency_key,
        )

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                    unit_price=item.discount_price or item.price,
                    subtotal=item.subtotal,
                )
                for item in cart.items.all()
            ]
        )

        return order, True

    def deactivate_cart(self, cart):
        cart.is_active = False
        cart.save(update_fields=["is_active"])
