from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from components.security.webhooks.verifier import WebhookVerifier
from components.idempotency.service import IdempotencyService
from components.caching.cache_factory import get_cache
from apps.payments.tasks import process_stripe_event


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # VERY IMPORTANT

    def post(self, request, *args, **kwargs):
        verifier = WebhookVerifier(secret="STRIPE_WEBHOOK_SECRET")

        # 1️⃣ Verify signature (FAIL FAST)
        verifier.verify(
            payload=request.body,
            signature=request.headers.get("X-Signature"),
            timestamp=int(request.headers.get("X-Timestamp")),
        )

        # 2️⃣ Idempotency check
        idempotency = IdempotencyService(cache=get_cache("idempotency"))

        event_id = request.headers.get("X-Event-ID")

        if not idempotency.acquire(event_id):
            return Response(status=status.HTTP_200_OK)

        # 3️⃣ Dispatch async processing
        process_stripe_event.delay(request.data)

        # 4️⃣ ACK immediately
        return Response(status=status.HTTP_200_OK)
