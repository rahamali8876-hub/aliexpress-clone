from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class CartItemEntity:
    id: UUID
    product_variant_id: UUID
    quantity: int
    price: Decimal
    discount_price: Decimal | None

    @property
    def unit_price(self) -> Decimal:
        return self.discount_price or self.price

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity
