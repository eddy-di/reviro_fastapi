from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.database.product import ProductCRUD
from app.services.root import AppService


class ProductService(AppService):
    def get_products(self, company_id: int, skip: int, limit: int) -> list[Product]:
        result = ProductCRUD(self.db).get_products(company_id=company_id, skip=skip, limit=limit)
        return result

    def create_product(self, company_id: int, schema: ProductCreate) -> Product | HTTPException:
        result = ProductCRUD(self.db).create_product(company_id=company_id, schema=schema)
        return result

    def get_product(self, company_id: int, product_id: int) -> Product | HTTPException:
        result = ProductCRUD(self.db).get_product(company_id=company_id, product_id=product_id)
        return result

    def put_product(self, company_id: int, product_id: int, schema: ProductUpdate) -> Product | HTTPException:
        result = ProductCRUD(self.db).put_product(
            company_id=company_id,
            product_id=product_id,
            schema=schema
        )
        return result

    def patch_product(self, company_id: int, product_id: int, schema: ProductUpdate) -> Product | HTTPException:
        result = ProductCRUD(self.db).patch_product(
            company_id=company_id,
            product_id=product_id,
            schema=schema
        )
        return result

    def delete_product(self, company_id: int, product_id: int) -> JSONResponse | HTTPException:
        ProductCRUD(self.db).delete_product(company_id=company_id, product_id=product_id)
        return JSONResponse(status_code=204, content='Product deleted.')
