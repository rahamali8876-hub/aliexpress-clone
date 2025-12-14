class CODPaymentStrategy:
    provider = "COD"

    def initiate(self, *, order, payment):
        # COD is instantly successful
        payment.status = "SUCCESS"
        payment.gateway_reference = "COD"
        payment.save(update_fields=["status", "gateway_reference"])

        order.status = "PAID"
        order.save(update_fields=["status"])

        return {
            "status": "SUCCESS",
            "message": "Cash on Delivery confirmed",
        }

    def handle_webhook(self, payload):
        # No webhook needed for COD
        pass
