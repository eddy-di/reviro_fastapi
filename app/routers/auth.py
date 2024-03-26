from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config.core import ALGORITHM, REGISTER_LINK, SECRET_KEY, TOKEN_LINK
from app.config.database import get_db
from app.models.user import User
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

    token = create_access_token(user.username, user.id, timedelta(days=1))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')
