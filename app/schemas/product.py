from pydantic import BaseModel, Field
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal


class ProductBase(BaseModel):
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    price: Decimal | None
    discount: int = Field(default=0, ge=0, lt=100)
    quantity: int = Field(default=0, ge=0)
    company_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
