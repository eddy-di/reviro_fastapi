from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(pattern=r'^[\w.-]+$')
    password: str
    role: str | None = 'user'


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
