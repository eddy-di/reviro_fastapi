from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config.core import COMPANIES_LINK, COMPANY_LINK
from app.config.database import get_db
from app.models.company import Company
from app.schemas.company import Company as CompanySchema
from app.schemas.company import CompanyCreate, CompanyPaginated, CompanyUpdate
from app.services.api.company import CompanyService

company_router = APIRouter()


@company_router.get(
    COMPANIES_LINK,
    response_model=CompanyPaginated,
    tags=['Companies']
)
def get_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    count = CompanyService(db).get_total_count()
    result = CompanyService(db).get_companies(
        skip=skip,
        limit=limit
    )
    next_skip = skip + limit
    prev_skip = skip - limit if skip >= limit else None
    next_link = f'{COMPANIES_LINK[4:]}?skip={next_skip}&limit={limit}' if next_skip < count else None
    prev_link = f'{COMPANIES_LINK[4:]}?skip={prev_skip}&limit={limit}' if prev_skip is not None else None
    # [4:] is necessary to go through the postman automatic addition when the link is generated
    # for production maybe it has to be changed
    return {
        'count': count,
        'results': result,
        'next_page': next_link,
        'prev_page': prev_link
    }


@company_router.post(
    COMPANIES_LINK,
    response_model=CompanySchema,
    status_code=201,
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
def put_company(
    company_id: int,
    schema: CompanyUpdate,
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
    schema: CompanyUpdate,
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
