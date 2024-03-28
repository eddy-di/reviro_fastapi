from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(pattern=r'^[\w.-]+$')
    password: str
    role: str | None = 'user'


class RegisterSuccess(BaseModel):
    message: str
    id: int
    username: str
    role: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
