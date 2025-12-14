import hmac
import hashlib
import time


class WebhookVerifier:
    MAX_DRIFT_SECONDS = 300  # 5 min

    def __init__(self, secret: str):
        self.secret = secret.encode()

    def verify(self, *, payload: bytes, signature: str, timestamp: int):
        self._verify_timestamp(timestamp)
        expected = self._sign(payload, timestamp)
        if not hmac.compare_digest(expected, signature):
            raise ValueError("Invalid webhook signature")

    def _verify_timestamp(self, timestamp: int):
        if abs(time.time() - timestamp) > self.MAX_DRIFT_SECONDS:
            raise ValueError("Webhook timestamp expired")

    def _sign(self, payload: bytes, timestamp: int) -> str:
        msg = f"{timestamp}.".encode() + payload
        return hmac.new(self.secret, msg, hashlib.sha256).hexdigest()
