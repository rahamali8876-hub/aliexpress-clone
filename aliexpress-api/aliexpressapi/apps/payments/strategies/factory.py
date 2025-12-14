from apps.payments.strategies.cod import CODPaymentStrategy
from apps.payments.strategies.razorpay import RazorpayPaymentStrategy


class PaymentStrategyFactory:
    _strategies = {
        "COD": CODPaymentStrategy(),
        "RAZORPAY": RazorpayPaymentStrategy(),
    }

    @classmethod
    def get(cls, provider: str):
        strategy = cls._strategies.get(provider)
        if not strategy:
            raise ValueError("Unsupported payment provider")
        return strategy
