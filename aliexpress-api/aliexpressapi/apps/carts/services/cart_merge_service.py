from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from apps.carts.context.unit_of_work import UnitOfWork


class CartMergeService:
    def merge(self, *, user, session_id: str):
        if not session_id:
            return

        guest_cart = Cart.objects.filter(
            session_id=session_id,
            is_active=True,
        ).first()

        if not guest_cart:
            return

        user_cart = Cart.objects.filter(
            user=user,
            is_active=True,
        ).first()

        with UnitOfWork():
            # Case 1: User has no cart → attach guest cart
            if not user_cart:
                guest_cart.user = user
                guest_cart.session_id = None
                guest_cart.save(update_fields=["user", "session_id"])
                return

            # Case 2: Merge carts
            for item in guest_cart.items.all():
                existing = CartItem.objects.filter(
                    cart=user_cart,
                    product_variant=item.product_variant,
                ).first()

                if existing:
                    existing.quantity += item.quantity
                    existing.save(update_fields=["quantity"])
                else:
                    item.cart = user_cart
                    item.save(update_fields=["cart"])

            guest_cart.is_active = False
            guest_cart.save(update_fields=["is_active"])
