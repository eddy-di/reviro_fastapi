from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, Product as ProductSchema
from app.config.core import PRODUCTS_LINK, PRODUCT_LINK
from app.services.api.product import ProductService


product_router = APIRouter()


@product_router.get(
    PRODUCTS_LINK, 
    response_model=list[ProductSchema], 
    tags=['Products']
)
def get_products(
    company_id: int, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
) -> list[Product]:
    result = ProductService(db).get_products(
        company_id=company_id, 
        skip=skip, 
        limit=limit
    )
    return result


@product_router.post(
    PRODUCTS_LINK, 
    response_model=ProductSchema, 
    tags=['Products']
)
def create_product(
    company_id: int, 
    schema: ProductCreate, 
    db: Session = Depends(get_db)
) -> Product | HTTPException:
    result = ProductService(db).create_product(
        company_id=company_id, 
        schema=schema
    )
    return result


@product_router.get(
    PRODUCT_LINK, 
    response_model=ProductSchema, 
    tags=['Products']
)
def get_product(
    company_id: int, 
    product_id: int, 
    db: Session = Depends(get_db)
) -> Product | HTTPException:
    result = ProductService(db).get_product(
        company_id=company_id, 
        product_id=product_id
    )
    return result


@product_router.put(
    PRODUCT_LINK, 
    response_model=ProductSchema, 
    tags=['Products']
)
def update_product(
    company_id: int, 
    product_id: int, 
    schema: ProductCreate, 
    db: Session = Depends(get_db)
) -> Product | HTTPException:
    result = ProductService(db).put_product(
        company_id=company_id, 
        product_id=product_id,
        schema=schema
    )
    return result


@product_router.patch(
    PRODUCT_LINK, 
    response_model=ProductSchema, 
    tags=['Products']
)
def patch_product(
    company_id: int, 
    product_id: int, 
    schema: ProductCreate, 
    db: Session = Depends(get_db)
) -> Product | HTTPException:
    result = ProductService(db).put_product(
        company_id=company_id, 
        product_id=product_id,
        schema=schema
    )
    return result


@product_router.delete(
    PRODUCT_LINK, 
    response_model=ProductSchema, 
    tags=['Products']
)
def delete_product(
    company_id: int, 
    product_id: int, 
    db: Session = Depends(get_db)
) -> JSONResponse | HTTPException:
    result = ProductService(db).delete_product(
        company_id=company_id, 
        product_id=product_id
    )
    return result
