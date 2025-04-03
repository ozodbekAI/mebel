from typing import Optional, Sequence, Any, Coroutine, List
from fastapi import Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.datebases.postgres import get_general_session

from app.api.schemas.product import CategoryCreate, CategoryListResponse, CategoryResponse, CategoryDetailResponse, CategoryUpdate
from app.api.models.product.product import Category, Subcategory

from slugify import slugify

class CategoryRepository:
    def __init__(
            self,
            session: AsyncSession = Depends(get_general_session)
        ):
        self.__session = session

    async def get_categories(self, page: int = 1, size: int = 10):
        count_query = select(func.count()).select_from(Category)
        total = await self.__session.scalar(count_query)
        
        if total is None:
            total = 0
        
        query = select(Category).offset((page - 1) * size).limit(size)

        result = await self.__session.execute(query)
        categories = result.scalars().all()\
        
        
        
        pages = (total + size - 1) // size if total > 0 else 0
        
        category_responses = []
        for cat in categories:
            category_responses.append(
                CategoryResponse(
                    id=cat.id,
                    name=cat.name,
                    description=cat.description,
                    is_active=cat.is_active,
                    slug=cat.slug,
                    image=cat.image,
                    created_at=cat.created_at,
                    updated_at=cat.updated_at
                )
            )
        
        list_response = CategoryListResponse(
            items=category_responses,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
        return list_response
    
    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        query = select(Category).where(Category.id == category_id)
        result = await self.__session.execute(query)
        category = result.scalars().first()
        
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
        return CategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            slug=category.slug,
            image=category.image,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
    

    async def create_category(self, category: CategoryCreate) -> CategoryResponse:

        slug = slugify(category.name)

        new_category = Category(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            slug=slug,
            image=category.image
        )
        
        self.__session.add(new_category)
        await self.__session.commit()
        
        return CategoryResponse(
            id=new_category.id,
            name=new_category.name,
            description=new_category.description,
            is_active=new_category.is_active,
            slug=new_category.slug,
            image=new_category.image,
            created_at=new_category.created_at,
            updated_at=new_category.updated_at
        )
    
    async def update_category(self, category_id: int, category: CategoryUpdate) -> CategoryResponse:
        query = select(Category).where(Category.id == category_id)
        result = await self.__session.execute(query)
        category_db = result.scalars().first()
        
        if category_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        
        update_data = category.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category_db, field, value)
        
        self.__session.add(category_db)
        await self.__session.commit()
        await self.__session.refresh(category_db)
        
        return CategoryResponse(
            id=category_db.id,
            name=category_db.name,
            description=category_db.description,
            is_active=category_db.is_active,
            slug=category_db.slug,
            image=category_db.image,
            created_at=category_db.created_at,
            updated_at=category_db.updated_at
        )