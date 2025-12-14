from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def initiate(self, *, order, payment):
        """
        Start payment process
        """
        raise NotImplementedError

    @abstractmethod
    def handle_webhook(self, payload):
        """
        Handle gateway webhook
        """
        raise NotImplementedError
