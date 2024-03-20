import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/eddy-di/Projects/reviro_fastapi/.env.test')

API_VERSION = '/api/v1/'
COMPANIES_LINK = API_VERSION + 'companies'
COMPANY_LINK = COMPANIES_LINK + '/{company_id}'
PRODUCTS_LINK = COMPANY_LINK + '/products'
PRODUCT_LINK = PRODUCTS_LINK + '/{product_id}'

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

database_url = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
    f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
