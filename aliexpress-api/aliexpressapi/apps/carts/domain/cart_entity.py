from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID
from typing import List
from .cart_item_entity import CartItemEntity

@dataclass
class CartEntity:
    id: UUID
    items: List[CartItemEntity] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def total_price(self) -> Decimal:
        return sum(item.subtotal for item in self.items)
