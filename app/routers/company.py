from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.schemas.company import Company, CompanyCreate
from app.models.company import Company as CompanyModel
from app.config.database import get_db

company_router = APIRouter()

# Company CRUD Endpoints
@company_router.get("/companies/", response_model=list[Company])
def get_companies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    companies = db.query(CompanyModel).offset(skip).limit(limit).all()
    return companies

@company_router.post("/companies/", response_model=Company)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = CompanyModel(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@company_router.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@company_router.put("/companies/{company_id}", response_model=Company)
def update_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

@company_router.patch("/companies/{company_id}", response_model=Company)
def patch_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for key, value in company.dict().items():
        if value is not None:
            setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

@company_router.delete("/companies/{company_id}", response_model=Company)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)
    db.commit()
    return company

