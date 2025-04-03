from typing import List
from fastapi import Depends, HTTPException, status


from app.api.repositories.subcategory import SubcategoryRepository
from app.api.schemas.product import SubcategoryListResponse, SubcategoryResponse, SubcategoryCreate, SubcategoryDetailResponse, SubcategoryUpdate


class SubcategoryController:
    def __init__(
            self, 
            category_repository: SubcategoryRepository = Depends()
        ):
        self.__category_repository = category_repository

    async def get_subcategories(self, page: int, size: int) -> SubcategoryListResponse:
        return await self.__category_repository.get_subcategories(page, size)
        
