from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.company import CompanyCreate, Company as CompanySchema
from app.models.company import Company
from app.config.database import get_db
from app.config.core import COMPANIES_LINK, COMPANY_LINK
from app.services.api.company import CompanyService


company_router = APIRouter()


@company_router.get(
    COMPANIES_LINK, 
    response_model=list[CompanySchema], 
    tags=['Companies']
)
def get_companies(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
) -> list[Company]:
    result = CompanyService(db).get_companies(
        skip=skip, 
        limit=limit
    )
    return result


@company_router.post(
    COMPANIES_LINK, 
    response_model=CompanySchema, 
    tags=['Companies']
)
def create_company(
    schema: CompanyCreate, 
    db: Session = Depends(get_db)
) -> Company:
    result = CompanyService(db).create_company(schema=schema)
    return result


@company_router.get(
    COMPANY_LINK, 
    response_model=CompanySchema, 
    tags=['Companies']
)
def get_company(
    company_id: int, 
    db: Session = Depends(get_db)
) -> Company | HTTPException:
    result = CompanyService(db).get_company(company_id=company_id)
    return result


@company_router.put(
    COMPANY_LINK, 
    response_model=CompanySchema, 
    tags=['Companies']
)
def update_company(
    company_id: int, 
    schema: CompanyCreate, 
    db: Session = Depends(get_db)
) -> Company | HTTPException:
    result = CompanyService(db).put_company(
        company_id=company_id, 
        schema=schema
    )
    return result


@company_router.patch(
    COMPANY_LINK, 
    response_model=CompanySchema, 
    tags=['Companies']
)
def patch_company(
    company_id: int, 
    schema: CompanyCreate, 
    db: Session = Depends(get_db)
) -> Company | HTTPException:
    result = CompanyService(db).patch_company(
        company_id=company_id, 
        schema=schema
    )
    return result


@company_router.delete(
    COMPANY_LINK, 
    response_model=CompanySchema, 
    tags=['Companies']
)
def delete_company(
    company_id: int, 
    db: Session = Depends(get_db)
) -> JSONResponse | HTTPException:
    result = CompanyService(db).delete_company(company_id=company_id)
    return result
