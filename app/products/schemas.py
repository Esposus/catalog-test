from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    stock_quantity: int = Field(..., ge=0)
    price: int = Field(..., ge=0)
    category_id: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    stock_quantity: int
    price: Decimal
    category_id: int | None

    model_config = ConfigDict(from_attributes=True)
