from fastapi import HTTPException

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services.root import DatabaseCRUD


def not_found_exception() -> HTTPException:
    raise HTTPException(status_code=404, detail='Company not found.')


class CompanyCRUD(DatabaseCRUD):
    def get_companies(self, skip: int, limit: int) -> list[Company]:
        menus = (
            self.db.query(Company)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return menus

    def create_company(self, schema: CompanyCreate) -> Company:

        new_company = Company(
            name=schema.name,
            description=schema.description,
            schedule_start=schema.schedule_start,
            schedule_end=schema.schedule_end,
            schedule_weekdays=schema.schedule_weekdays,
            phone_number=schema.phone_number,
            email=schema.email,
            map_link=schema.map_link,
            social_media1=schema.social_media1,
            social_media2=schema.social_media2,
            social_media3=schema.social_media3
        )

        self.db.add(new_company)
        self.db.commit()
        self.db.refresh(new_company)

        return new_company

    def get_company(self, company_id: int) -> Company | HTTPException:
        company = (
            self.db.query(Company)
            .filter(Company.id == company_id)
            .first()
        )

        if not company:
            return not_found_exception()

        return company

    def put_company(self, company_id: int, schema: CompanyUpdate) -> Company | HTTPException:
        company = self.db.query(Company).filter(Company.id == company_id).first()

        if not company:
            return not_found_exception()

        for key, value in schema.model_dump(exclude_unset=True).items():
            setattr(company, key, value)

        self.db.commit()
        self.db.refresh(company)

        return company

    def patch_company(self, company_id: int, schema: CompanyUpdate) -> Company | HTTPException:
        company = self.db.query(Company).filter(Company.id == company_id).first()

        if not company:
            return not_found_exception()

        patch_data = schema.model_dump(exclude_unset=True)

        for key, value in patch_data.items():
            setattr(company, key, value)

        self.db.commit()
        self.db.refresh(company)

        return company

    def delete_company(self, company_id: int) -> None | HTTPException:

        company = self.db.query(Company).filter(Company.id == company_id).first()

        if not company:
            return not_found_exception()

        self.db.delete(company)
        self.db.commit()

        return None
