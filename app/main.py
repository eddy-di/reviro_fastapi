from fastapi import FastAPI

from .routers.company import company_router

description = '''
# Companies and products management app
This API documentation is made solely to fulfill the requirements to pass for the internship program to Reviro.io company.
'''

app = FastAPI()


app.include_router(company_router)
