from typing import List
from fastapi import Depends, HTTPException, status


from app.api.repositories.category import CategoryRepository
from app.api.schemas.product import CategoryListResponse, CategoryResponse, CategoryCreate, CategoryDetailResponse, CategoryUpdate


class CategoryController:
    def __init__(
            self, 
            category_repository: CategoryRepository = Depends()
        ):
        self.__category_repository = category_repository

    
    async def get_categories(self, page, size):
        categories = await self.__category_repository.get_categories(page, size)
        return categories
    
    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.__category_repository.get_category_by_id(category_id)
        return category
    
    async def create_category(self, category: CategoryCreate) -> CategoryResponse:
        category = await self.__category_repository.create_category(category)
        return category
    
    async def update_category(self, category_id: int, category: CategoryUpdate) -> CategoryResponse:
        category = await self.__category_repository.update_category(category_id, category)
        return category