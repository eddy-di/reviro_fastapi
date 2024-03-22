from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config.core import PRODUCT_LINK, PRODUCTS_LINK
from app.config.database import get_db
from app.models.product import Product
from app.schemas.product import Product as ProductSchema
from app.schemas.product import (
    ProductCreate,
    ProductPaginated,
    ProductPutUpdate,
    ProductUpdate,
)
from app.services.api.product import ProductService

product_router = APIRouter()


@product_router.get(
    PRODUCTS_LINK,
    response_model=ProductPaginated,
    tags=['Products']
)
def get_products(
    company_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    count = ProductService(db).get_total_count(company_id=company_id)
    result = ProductService(db).get_products(
        company_id=company_id,
        skip=skip,
        limit=limit
    )
    next_skip = skip + limit
    prev_skip = skip - limit if skip >= limit else None
    next_link = f'/v1/companies/{company_id}/products?skip={next_skip}&limit={limit}' if next_skip < count else None
    prev_link = f'/v1/companies/{company_id}/products?skip={prev_skip}&limit={limit}' if prev_skip is not None else None
    # [4:] is necessary to go through the postman automatic addition when the link is generated
    # for production maybe it has to be changed
    return {
        'count': count,
        'results': result,
        'next_page': next_link,
        'prev_page': prev_link
    }


@product_router.post(
    PRODUCTS_LINK,
    response_model=ProductSchema,
    status_code=201,
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
def put_product(
    company_id: int,
    product_id: int,
    schema: ProductPutUpdate,
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
    schema: ProductUpdate,
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
