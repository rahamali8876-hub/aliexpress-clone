from apps.carts.repositories.cart_repository import CartRepository
from apps.carts.context.unit_of_work import UnitOfWork


class CartService:
    def __init__(self, repo: CartRepository):
        self.repo = repo

    def get_cart(self, *, user, session_id):
        return self.repo.get_or_create_cart(
            user=user if user.is_authenticated else None,
            session_id=None if user.is_authenticated else session_id,
        )

    def add_item(self, *, cart, variant_id, quantity):
        with UnitOfWork():
            variant = self.repo.get_variant(variant_id)
            self.repo.add_item(cart=cart, variant=variant, quantity=quantity)
        return cart

    def update_item(self, *, cart, item_id, quantity):
        with UnitOfWork():
            self.repo.update_item(cart=cart, item_id=item_id, quantity=quantity)
        return cart

    def remove_item(self, *, cart, item_id):
        with UnitOfWork():
            self.repo.remove_item(cart=cart, item_id=item_id)
        return cart


# from apps.carts.repositories.cart_repository import CartRepository
# from apps.carts.context.unit_of_work import UnitOfWork

# class CartService:
#     def __init__(self, repo: CartRepository):
#         self.repo = repo

#     def get_cart(self, *, user, session_id):
#         return self.repo.get_or_create_cart(
#             user=user if user.is_authenticated else None,
#             session_id=None if user.is_authenticated else session_id,
#         )

#     def add_item(self, *, cart, variant_id, quantity):
#         with UnitOfWork():
#             variant = self.repo.get_variant(variant_id)
#             self.repo.add_item(cart=cart, variant=variant, quantity=quantity)
#         return cart
