# from django.contrib import admin

# # # Register your models here.
# # from .models import Cart, CartItem, Wishlist, WishlistItem
# from apps.carts.models.cart import Cart
# from apps.carts.models.cartItem import CartItem


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "created_at", "updated_at")
#     search_fields = ("user__username",)
#     list_filter = ("created_at", "updated_at")


# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ("id", "cart", "quantity", "added_at")
#     # list_display = ("cart", "product", "quantity", "added_at")
#     search_fields = ("cart__user__username", "product__name")
#     list_filter = ("added_at",)


# # @admin.register(Wishlist)
# # class WishlistAdmin(admin.ModelAdmin):
# #     list_display = ("user", "created_at")
# #     search_fields = ("user__username",)
# #     list_filter = ("created_at",)


# # @admin.register(WishlistItem)
# # class WishlistItemAdmin(admin.ModelAdmin):
# #     list_display = ("wishlist", "product", "added_at")
# #     search_fields = ("wishlist__user__username", "product__name")
# #     list_filter = ("added_at",)


from django.contrib import admin
from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = (
        "product_variant",
        "quantity",
        "price",
        "discount_price",
        "subtotal",
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
# list_display = (
#     "id",
#     "owner",
#     "total_items",
#     "total_price",
#     "is_active",
#     "is_locked",
#     "created_at",
# )

# def total_items(self, obj):
#     return obj.items.count()

# def total_price(self, obj):
#     return obj.total_price


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # list_display = (
    #     "id",
    #     "owner",
    #     "is_active",
    #     "is_locked",
    #     "created_at",
    # )

    list_display = (
        "id",
        "owner",
        "total_items",
        "total_price",
        "is_active",
        "is_locked",
        "created_at",
    )

    def total_items(self, obj):
        return obj.items.count()

    def total_price(self, obj):
        return obj.total_price

    list_filter = (
        "is_active",
        "is_locked",
        "created_at",
    )

    readonly_fields = (
        "id",
        "user",
        "session_id",
        "is_active",
        "is_locked",
        "created_at",
        "updated_at",
    )

    inlines = [CartItemInline]

    ordering = ("-created_at",)

    def owner(self, obj):
        return obj.user or f"Session: {obj.session_id}"

    owner.short_description = "Owner"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


def is_locked(self, obj):
    return "🔒" if obj.is_locked else "🔓"
