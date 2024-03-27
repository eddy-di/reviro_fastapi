from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.config.core import (  # REFRESH_LINK,
    ALGORITHM,
    REGISTER_LINK,
    SECRET_KEY,
    TOKEN_LINK,
)
from app.config.database import get_db
from app.models.user import RefreshTokens, User
from app.schemas.auth import CreateUserRequest, Token

auth = APIRouter(
    tags=['Auth']
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

db_dependency = Annotated[Session, Depends(get_db)]


@auth.post(
    REGISTER_LINK,
    status_code=201
)
def register(
    db: db_dependency,
    schema: CreateUserRequest
):
    create_user = User(
        username=schema.username,
        hashed_password=bcrypt_context.hash(schema.password)
    )
    db.add(create_user)
    db.commit()


@auth.post(
    TOKEN_LINK,
    response_model=Token
)
def obtain_token(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail='Could not validate user.')

    access_token = create_token(user.username, user.id, user.role, timedelta(hours=1))
    refresh_token = create_token(user.username, user.id, user.role, timedelta(days=1))

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


def store_refresh_token(db: Session, token: str, expires_at: datetime):
    refresh_token = RefreshTokens(token=token, expires_at=expires_at)
    db.add(refresh_token)
    db.commit()


def delete_expired_refresh_tokens(db: Session):
    # Delete expired refresh tokens from the database
    now = datetime.now(timezone.utc)
    db.query(RefreshTokens).filter(RefreshTokens.expires_at < now).delete()
    db.commit()


def validate_refresh_token(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials.'
    )
    try:
        db_token = db.query(RefreshTokens).filter(RefreshTokens.token == token).first()
        if db_token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get('sub')
            role: str = payload('role')
            if username is None or role is None:
                raise credentials_exception
            user = db.query(User).filter(User.username == username).first()
            return user
        else:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate user.')
        user = db.query(User).filter(User.username == username).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_user)]):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=401,
            detail='You don\'t have enough permission.'
        )
