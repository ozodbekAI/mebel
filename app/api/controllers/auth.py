from fastapi import Depends, HTTPException, Request, Response, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.models.user import User
from app.api.repositories.auth import AuthRepository
from app.api.schemas.user import CreateUser, Login, ResponseUser
from app.core.settings import get_settings
from app.api.utils.auth import AuthUtils

settings = get_settings()

class AuthController:
    def __init__(
            self, 
            session: AsyncSession,
        ):
        self.session = session
        self.repository = AuthRepository(session)

    async def create_user(self, data: CreateUser) -> User:
        try:
            user = await self.repository.create_user(data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User allaqachon mavjud",
            )
        return user
    
    async def get_users(self) -> List[ResponseUser]:
        try:
            users = await self.repository.get_users()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Userlar topilmadi",
            )
        return users
    
    
    async def login(self, data: Login, response: Response) -> dict:
        user = await self.repository.get_user_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email yoki parol xato",
            )

        if not user or not AuthUtils.verify_password(plain_password=data.password, hashed_password=user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email yoki parol xato",
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Foydalanuvchi bloklangan",
            )
        
        access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        access_token = await AuthUtils.create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            }, 
            expired_minute=access_token_expires
        )

        refresh_token_expires = settings.REFRESH_TOKEN_EXPIRE_DAYS
        refresh_token = await AuthUtils.create_refresh_token(
            data={
                "sub": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
            },
            expired_days=refresh_token_expires
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=refresh_token_expires,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=access_token_expires,
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
            },
        }

        
