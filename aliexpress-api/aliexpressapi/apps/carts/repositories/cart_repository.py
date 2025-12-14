from django.shortcuts import get_object_or_404
from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from apps.products.models.product_variant import ProductVariant


class CartRepository:
    def get_or_create_cart(self, *, user=None, session_id=None):
        if user and user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                user=user,
                is_active=True,
                defaults={"session_id": None},
            )
            return cart

        if session_id:
            cart, _ = Cart.objects.get_or_create(
                session_id=session_id,
                is_active=True,
                defaults={"user": None},
            )
            return cart

        raise ValueError("Cart must have either user or session_id")

    def get_variant(self, variant_id):
        return get_object_or_404(ProductVariant, id=variant_id)

    def add_item(self, *, cart, variant, quantity):
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={
                "price": variant.price,
                "discount_price": variant.discount_price,
                "quantity": quantity,
            },
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item

    def update_item(self, *, cart, item_id, quantity):
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.quantity = quantity
        item.save()
        return item

    def remove_item(self, *, cart, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()


# class CartRepository:

#     def get_or_create_cart(self, *, user=None, session_id=None):
#         if user and user.is_authenticated:
#             cart, _ = Cart.objects.get_or_create(
#                 user=user,
#                 is_active=True,
#                 defaults={"session_id": None},
#             )
#             return cart

#         if session_id:
#             cart, _ = Cart.objects.get_or_create(
#                 session_id=session_id,
#                 is_active=True,
#                 defaults={"user": None},
#             )
#             return cart

#         raise ValueError("Cart must have either user or session_id")
