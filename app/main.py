from fastapi import Depends, FastAPI

from app.config.database import Base, engine, get_db

from .routers.company import company_router
from .routers.product import product_router

description = '''
# Companies and products management app
This API documentation is made solely to fulfill the requirements to pass for the internship program to Reviro.io company.
'''

app = FastAPI(
    title='Reviro.io internship API',
    description=description,
    version='1.0.0',
    dependencies=[Depends(get_db)],
    openapi_tags=[
        {
            'name': 'Companies',
            'description': 'Operations for companies'
        },
        {
            'name': 'Products',
            'description': 'Operations for products'
        },
    ]
)


Base.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(product_router)
