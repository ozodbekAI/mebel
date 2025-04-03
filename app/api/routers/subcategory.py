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

from app.api.controllers.subcategory import SubcategoryController
from app.api.models.user import User
from app.api.schemas.product import SubcategoryBase, SubcategoryCreate, SubcategoryListResponse, SubcategoryResponse, SubcategoryUpdate

from app.core.datebases.postgres import get_general_session
from app.api.utils.auth import AuthUtils

router = APIRouter()

@router.get("/",
    response_model=SubcategoryListResponse, 
    status_code=status.HTTP_200_OK
)
async def get_subcategories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    controller: SubcategoryController = Depends(),
    session: AsyncSession = Depends(get_general_session),
    # current_user: User = Depends(AuthUtils.get_current_admin_user), 
    ):
    
    
    return await controller.get_subcategories(page, size)
