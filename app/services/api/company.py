from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.database.company import CompanyCRUD
from app.services.root import AppService


class CompanyService(AppService):
    def get_companies(self, skip: int, limit: int) -> list[Company]:
        result = CompanyCRUD(self.db).get_companies(skip=skip, limit=limit)
        return result

    def get_total_count(self) -> int:
        return CompanyCRUD(self.db).get_total_count()

    def create_company(self, schema: CompanyCreate) -> Company:
        result = CompanyCRUD(self.db).create_company(schema=schema)
        return result

    def get_company(self, company_id: int) -> Company | HTTPException:
        result = CompanyCRUD(self.db).get_company(company_id=company_id)
        return result

    def put_company(self, company_id: int, schema: CompanyUpdate) -> Company | HTTPException:
        result = CompanyCRUD(self.db).put_company(company_id=company_id, schema=schema)
        return result

    def patch_company(self, company_id: int, schema: CompanyUpdate) -> Company | HTTPException:
        result = CompanyCRUD(self.db).patch_company(company_id=company_id, schema=schema)
        return result

    def delete_company(self, company_id: int) -> JSONResponse | HTTPException:
        CompanyCRUD(self.db).delete_company(company_id=company_id)
        return JSONResponse(status_code=200, content='Company deleted.')
