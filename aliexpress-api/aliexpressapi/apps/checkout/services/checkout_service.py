# apps/checkout/services/checkout_service.py
import uuid
from apps.carts.context.unit_of_work import UnitOfWork
from apps.checkout.repositories.checkout_repository import CheckoutRepository


class CheckoutService:
    def __init__(self, repo: CheckoutRepository):
        self.repo = repo

    def checkout(self, *, cart, user, idempotency_key=None):
        if not cart.items.exists():
            raise ValueError("Cart is empty")

        idempotency_key = idempotency_key or uuid.uuid4()

        with UnitOfWork():
            self.repo.lock_cart(cart)

            order, created = self.repo.create_order(
                cart=cart,
                user=user,
                idempotency_key=idempotency_key,
            )

            if created:
                self.repo.deactivate_cart(cart)

        return order
