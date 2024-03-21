from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.core import database_url
from app.config.database import Base, get_db
from app.main import app
from app.models.company import Company
from app.models.product import Product

engine = create_engine(database_url)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


current_datetime = datetime.now()
current_microseconds = current_datetime.microsecond


@pytest.fixture
def api_client():
    try:
        Base.metadata.create_all(bind=engine)
        client = TestClient(app)
        yield client
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_company():
    session = TestingSessionLocal()
    db_company_item = Company(
        name='testName',
        description='testDescription',
        schedule_start='08:00:00',
        schedule_end='23:00:00',
        phone_number='+999999999999',
        email='test.example@email.com',
        map_link='https://2gis.kg/bishkek',
        social_media1='https://www.instagram.com',
        social_media2='https://twitter.com',
        social_media3=None,
    )
    session.add(db_company_item)
    session.commit()
    session.refresh(db_company_item)
    session.close()
    return db_company_item


@pytest.fixture
def create_product():
    def make_product(company_id: int):
        session = TestingSessionLocal()
        db_product_item = Product(
            name='testProductName',
            description='testProductDescription',
            price='123.12',
            discount=10,
            quantity=20,
            company_id=company_id
        )
        session.add(db_product_item)
        session.commit()
        session.refresh(db_product_item)
        session.close()
        return db_product_item
    return make_product


@pytest.fixture
def create_num_of_companies():
    def make_companies(num: int) -> list:
        companies = []
        for _ in range(num):
            session = TestingSessionLocal()
            company = Company(
                name='testName' + str(current_microseconds),
                description='testDescription',
                schedule_start='08:00:00',
                schedule_end='23:00:00',
                phone_number='+999999999999',
                email='test.example@email.com',
                map_link='https://2gis.kg/bishkek',
                social_media1='https://www.instagram.com',
                social_media2='https://twitter.com',
                social_media3=None,
            )
            session.add(company)
            session.commit()
            session.refresh(company)
            session.close()
            companies.append(company)
        return companies
    return make_companies


@pytest.fixture
def create_num_of_products_for_one_company(create_company):
    company = create_company

    def make_num_of_products(num: int) -> list:
        products = []
        for _ in range(num):
            session = TestingSessionLocal()
            db_product_item = Product(
                name='testProductName',
                description='testProductDescription',
                price='123.12',
                discount=10,
                quantity=20,
                company_id=company.id
            )
            session.add(db_product_item)
            session.commit()
            session.refresh(db_product_item)
            session.close()
            products.append(db_product_item)
        return products
    return make_num_of_products


@pytest.fixture
def company_create_data_dict() -> dict:
    company = {
        'name': 'capito',
        'description': 'coffee house',
        'schedule_start': '08:00:00',
        'schedule_end': '00:00:00',
        'schedule_weekdays': None,
        'phone_number': '+996558398456',
        'email': 'capito.kg@gmail.com',
        'map_link': 'https://2gis.kg/bishkek/inside/15763234351147898/firm/70000001068507268?m=74.60815%2C42.830919%2F16.57',
        'social_media1': 'https://www.instagram.com/capito.bishkek/',
        'social_media2': 'https://twitter.com/capitobishkek',
        'social_media3': None
    }
    return company


@pytest.fixture
def product_create_data_dict():
    def make_data_dict(company_id: int) -> dict:
        data_dict = {
            'name': 'testProductNameFromDict',
            'description': 'testProductDescriptionFromDict',
            'price': '123.12',
            'discount': 10,
            'quantity': 20,
            'company_id': company_id
        }
        return data_dict
    return make_data_dict
