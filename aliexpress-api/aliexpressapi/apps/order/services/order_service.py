from apps.order.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def list_orders(self, *, user):
        return self.repo.list_orders(user=user)

    def get_order(self, *, order_id, user):
        return self.repo.get_order(order_id=order_id, user=user)
