from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy import Enum, and_, or_, DECIMAL
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.api.models.user import User
from app.api.schemas.user import CreateUser, ResponseUser
from app.api.utils.auth import AuthUtils


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, data: CreateUser) -> User:
        hashed_password = await AuthUtils.get_password_hash(data.password)
        user = User(
            email=data.email,
            password=hashed_password,
            full_name=data.full_name,
            )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_users(self) -> List[ResponseUser]:
        users = await self.session.execute(select(User))
        result =  users.scalars().all()
        return result
    

    async def get_user_by_email(self, email: str) -> User:
        user = await self.session.execute(select(User).filter(User.email == email))
        return user.scalar_one_or_none()