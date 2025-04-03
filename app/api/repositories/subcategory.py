from typing import Optional, Sequence, Any, Coroutine, List
from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.datebases.postgres import get_general_session

from app.api.schemas.product import SubcategoryBase, SubcategoryCreate, SubcategoryDetailResponse, SubcategoryListResponse, SubcategoryResponse, SubcategoryUpdate
from app.api.models.product.product import Category, Subcategory

from slugify import slugify



class SubcategoryRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_subcategories(self, page, size):
        count_query = select(func.count()).select_from(Subcategory)
        total = await self.__session.scalar(count_query)
        
        if total is None:
            total = 0
        
        query = select(Subcategory).offset((page - 1) * size).limit(size)

        result = await self.__session.execute(query)
        subcategories = result.scalars().all()
        
        pages = (total + size - 1) // size if total > 0 else 0
        
        subcategory_responses = []
        for sub in subcategories:
            subcategory_responses.append(
                SubcategoryResponse(
                    id=sub.id,
                    category_id=sub.category_id,
                    name=sub.name,
                    description=sub.description,
                    is_active=sub.is_active,
                    slug=sub.slug,
                    created_at=sub.created_at,
                    updated_at=sub.updated_at
                )
            )
        
        list_response = SubcategoryListResponse(
            items=subcategory_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
        return list_response