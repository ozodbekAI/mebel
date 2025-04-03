from datetime import datetime
from typing import Sequence, List, Optional, Any, Coroutine
from fastapi import (
    APIRouter,
    Depends,
    Header,
    Query,
    Response,
    status,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession


from app.api.controllers.auth import AuthController
from app.core.datebases.postgres import get_general_session
from app.api.schemas.user import Login, ResponseUser, CreateUser

router = APIRouter()


@router.post(
    "/register",
    response_model=ResponseUser,
)
async def create_user(
    data: CreateUser,
    session: AsyncSession = Depends(get_general_session),
) -> ResponseUser:
    
    controller = AuthController(session)

    user = await controller.create_user(data)
    return user

@router.get(
    "/users",
    response_model=List[ResponseUser],
)
async def get_users(
    session: AsyncSession = Depends(get_general_session),
) -> List[ResponseUser]:
    
    controller = AuthController(session)

    users = await controller.get_users()

    return users


@router.post(
    "/login",
    response_model=dict,
)    
async def login(
    data: Login,
    response: Response,
    session: AsyncSession = Depends(get_general_session),
) -> dict:
    controller = AuthController(session)

    user = await controller.login(data, response)

    return user
