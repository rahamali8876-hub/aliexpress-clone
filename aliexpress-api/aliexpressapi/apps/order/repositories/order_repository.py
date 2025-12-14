from django.shortcuts import get_object_or_404
from apps.order.models.order import Order


class OrderRepository:
    def list_orders(self, *, user):
        if user.is_authenticated:
            return Order.objects.filter(user=user).order_by("-created_at")

        return Order.objects.none()

    def get_order(self, *, order_id, user):
        if user.is_authenticated:
            return get_object_or_404(Order, id=order_id, user=user)

        raise PermissionError("Authentication required")
