from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class AddItemRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: Annotated[int, Field(strict=True, gt=0)]

class RemoveItemRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: Annotated[int, Field(strict=True, gt=0)]

class OrderItemResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_moment: int

    model_config = ConfigDict(from_attributes = True, extra="forbid")

class OrderCreate(BaseModel):
    customer_id: int

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    created_at: datetime
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes = True)