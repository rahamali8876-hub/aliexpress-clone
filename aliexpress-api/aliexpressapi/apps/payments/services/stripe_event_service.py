class StripeEventService:
    def handle(self, payload: dict):
        event_type = payload["type"]

        if event_type == "payment_intent.succeeded":
            self._handle_payment_success(payload["data"]["object"])

        elif event_type == "payment_intent.failed":
            self._handle_payment_failure(payload["data"]["object"])

    def _handle_payment_success(self, data):
        # update order
        # mark payment as PAID
        pass

    def _handle_payment_failure(self, data):
        # mark payment as FAILED
        pass
