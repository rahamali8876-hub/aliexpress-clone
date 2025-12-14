import uuid
from apps.payments.repositories.payment_repository import PaymentRepository
from apps.payments.strategies.factory import PaymentStrategyFactory
from apps.carts.context.unit_of_work import UnitOfWork


class PaymentService:
    def __init__(self, repo: PaymentRepository):
        self.repo = repo

    def initiate_payment(self, *, order, provider, idempotency_key=None):
        idempotency_key = idempotency_key or uuid.uuid4()

        with UnitOfWork():
            payment, _ = self.repo.get_or_create_payment(
                order=order,
                provider=provider,
                idempotency_key=idempotency_key,
            )

            strategy = PaymentStrategyFactory.get(provider)
            response = strategy.initiate(
                order=order,
                payment=payment,
            )

        return response
