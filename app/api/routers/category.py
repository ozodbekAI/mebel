from datetime import datetime
from typing import Sequence, List, Optional, Any, Coroutine
from fastapi import (
    APIRouter,
    Depends,
    Header,
    Query,
    status,
    HTTPException,
    Form,
    File,
    UploadFile,
)
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.controllers.category import CategoryController
from app.api.models.user import User
from app.api.schemas.product import CategoryCreate, CategoryResponse, CategoryUpdate, SubcategoryCreate, ProductCreate, CategoryListResponse

from app.core.datebases.postgres import get_general_session
from app.api.utils.auth import AuthUtils

router = APIRouter()

@router.get("/",
    response_model=CategoryListResponse, 
    status_code=status.HTTP_200_OK
)
async def get_categories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    controller: CategoryController = Depends(),
    session: AsyncSession = Depends(get_general_session),
    # current_user: User = Depends(AuthUtils.get_current_admin_user), 
    ):
    
    
    return await controller.get_categories(page, size)

@router.get("/{category_id}",
    response_model=CategoryResponse, 
    status_code=status.HTTP_200_OK
)
async def get_category_by_id(
    category_id: int,
    controller: CategoryController = Depends(),
    session: AsyncSession = Depends(get_general_session),
    # current_user: User = Depends(AuthUtils.get_current_admin_user), 
    ) -> CategoryResponse:
    
    
    return await controller.get_category_by_id(category_id)


@router.post("/",
    response_model=CategoryResponse, 
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    category: CategoryCreate,
    controller: CategoryController = Depends(),
    session: AsyncSession = Depends(get_general_session),
    current_user: User = Depends(AuthUtils.get_current_admin_user), 
    ) -> CategoryResponse:
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

    return await controller.create_category(category)


@router.put("/{category_id}",
    response_model=CategoryResponse, 
    status_code=status.HTTP_200_OK
)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    controller: CategoryController = Depends(),
    session: AsyncSession = Depends(get_general_session),
    current_user: User = Depends(AuthUtils.get_current_admin_user), 
    ) -> CategoryResponse:
    
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

    return await controller.update_category(category_id, category)