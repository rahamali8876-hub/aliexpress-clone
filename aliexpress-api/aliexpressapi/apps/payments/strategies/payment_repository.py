import uuid
from apps.payments.models.payment import Payment


class PaymentRepository:
    def get_or_create_payment(self, *, order, provider, idempotency_key):
        payment = Payment.objects.filter(idempotency_key=idempotency_key).first()

        if payment:
            return payment, False

        payment = Payment.objects.create(
            order=order,
            provider=provider,
            amount=order.total_price,
            idempotency_key=idempotency_key,
        )

        return payment, True
