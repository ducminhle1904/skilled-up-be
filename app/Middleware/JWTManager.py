import os

from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import JWTError, jwt
from typing import Optional
from app.Core.config import settings


class JWTManager:

    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encode_jwt

    @staticmethod
    def verify_token(token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            current_timestamp = datetime.utcnow().timestamp()
            if not decode_token:
                raise credentials_exception
            if decode_token["exp"] <= current_timestamp:
                raise credentials_exception
            return decode_token
        except JWTError:
            raise credentials_exception
