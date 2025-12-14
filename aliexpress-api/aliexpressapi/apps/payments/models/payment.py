import uuid
from django.db import models
from apps.orders.models.order import Order


class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED = "INITIATED"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        REFUNDED = "REFUNDED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    provider = models.CharField(max_length=50)  # COD, STRIPE, RAZORPAY
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.INITIATED
    )

    gateway_reference = models.CharField(max_length=255, null=True, blank=True)

    idempotency_key = models.UUIDField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} | {self.amount} | {self.status}"
