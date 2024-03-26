from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(pattern=r'^[\w.-]+$')
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
