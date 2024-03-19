from fastapi import HTTPException

from app.services.root import DatabaseCRUD
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from app.models.company import Company
from app.services.database.company import not_found_exception as no_company



def not_found_exception() -> HTTPException:
    """Exception for unavailable/non-existent product instance."""

    raise HTTPException(status_code=404, detail='Product not found')


class ProductCRUD(DatabaseCRUD):

    def check_company_id(self, company_id: int) -> HTTPException | None:
        result = self.db.query(Company).filter(Company.id == company_id).first()

        if not result:
            return no_company()
        return None
    
    def get_products(self, company_id: int, skip: int, limit: int) -> list[Product] | HTTPException:
        
        self.check_company_id(company_id=company_id)

        products = (
            self.db.query(Product)
            .filter(Product.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return products
    
    def create_product(self, company_id: int, schema: ProductCreate) -> Product:
        
        self.check_company_id(company_id=company_id)

        new_product = Product(
            name=schema.name,
            description=schema.description,
            created_at=schema.created_at,
            updated_at=schema.updated_at,
            price=schema.price,
            discount=schema.discount,
            quantity=schema.quantity,
            company_id=company_id
        )
        
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)

        return new_product
    
    def get_product(self, company_id: int, product_id: int) -> Product | HTTPException:
        
        self.check_company_id(company_id=company_id)

        product = (
            self.db.query(Product)
            .filter(Product.company_id == company_id, Product.id == product_id)
            .first()
        )

        if not product:
            return not_found_exception()
        
        return product
    
    def put_product(self, company_id: int, product_id: int, schema: ProductUpdate) -> Product | HTTPException:
        
        self.check_company_id(company_id=company_id)

        product = (
            self.db.query(Product)
            .filter(Product.company_id == company_id, Product.id == product_id)
            .first()
        )

        if not product:
            return not_found_exception()
        
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        
        self.db.commit()
        self.db.refresh(product)

        return product
    
    def patch_product(self, company_id: int, product_id: int, schema: ProductUpdate) -> Product | HTTPException:
        
        self.check_company_id(company_id=company_id)

        product = (
            self.db.query(Product)
            .filter(Product.company_id == company_id, Product.id == product_id)
            .first()
        )

        if not product:
            return not_found_exception()
        
        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        
        self.db.commit()
        self.db.refresh(product)

        return product
    
    def delete_product(self, company_id: int, product_id: int) -> None | HTTPException:
        
        self.check_company_id(company_id=company_id)

        product = (
            self.db.query(Product)
            .filter(Product.company_id == company_id, Product.id == product_id)
            .first()
        )

        if not product:
            return not_found_exception()
        
        self.db.delete(product)
        self.db.commit()

        return None
