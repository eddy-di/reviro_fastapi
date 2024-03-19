from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str | None
    description: str | None
    created_at: datetime
    updated_at: datetime
    price: Decimal | None
    discount: int = Field(default=0, ge=0, lt=100)
    quantity: int = Field(default=0, ge=0)
    company_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    discount: int = Field(default=0, ge=0, lt=100)
    quantity: int = Field(default=0, ge=0)


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
