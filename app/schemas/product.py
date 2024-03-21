from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str | None
    description: str | None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    price: Decimal | None
    discount: int | None = Field(default=0, ge=0, lt=100)
    quantity: int | None = Field(default=0, ge=0)
    company_id: int | None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    updated_at: datetime = datetime.now()
    price: Decimal | None = None
    discount: int | None = Field(default=0, ge=0, lt=100)
    quantity: int | None = Field(default=0, ge=0)
    company_id: int | None = None


class ProductPutUpdate(ProductBase):
    name: str
    description: str
    updated_at: datetime = datetime.now()
    price: Decimal
    discount: int = Field(default=0, ge=0, lt=100)
    quantity: int = Field(default=0, ge=0)
    company_id: int | None = None


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
