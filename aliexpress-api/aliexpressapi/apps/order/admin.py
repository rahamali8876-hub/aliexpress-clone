# from django.contrib import admin

# from apps.order.models.order import Order
# from apps.order.models.order_item import OrderItem
# # from .models import Order, OrderItem, Shipment, Return


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["id", "user", "status", "created_at"]
#     search_fields = ["user__username", "status"]
#     list_filter = ["status", "created_at"]


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ["id", "order", "product", "quantity", "price"]
#     search_fields = ["order__id", "product__name"]


# # @admin.register(Shipment)
# # class ShipmentAdmin(admin.ModelAdmin):
# #     list_display = ["id", "order", "tracking_number", "status", "shipped_at",'estimated_delivery']
# #     search_fields = ["tracking_number", "order__id"]
# #     list_filter = ["status", "shipped_at"]


# # @admin.register(Return)
# # class ReturnAdmin(admin.ModelAdmin):
# #     list_display = ["id", "order_item", "reason", "status", "created_at"]
# #     search_fields = ["order_item__id", "reason"]
# #     list_filter = ["status", "created_at"]


from django.contrib import admin
from django.utils.html import format_html

from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem


@admin.action(description="Mark selected orders as CANCELLED")
def cancel_orders(modeladmin, request, queryset):
    queryset.filter(status="PENDING").update(status="CANCELLED")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = (
        "product_variant",
        "quantity",
        "unit_price",
        "subtotal",
    )

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_display",
        "status",
        "total_price",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
        "user__username",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "user",
        "total_price",
        "status",
        "created_at",
        "idempotency_key",
    )

    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Customer")
    def user_display(self, obj):
        if obj.user:
            return obj.user.email or obj.user.username
        return format_html("<i>Guest</i>")

    actions = [cancel_orders]
