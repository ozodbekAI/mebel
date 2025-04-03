from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from fastapi import Query


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    slug: Optional[str] = None


class SubcategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    category_id: int


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int = 0
    is_active: bool = True
    is_featured: bool = False
    weight: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    color: Optional[str] = None
    subcategory_id: int


class ProductImageBase(BaseModel):
    image_path: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    display_order: int = 0


class ProductVariationBase(BaseModel):
    name: str
    sku: str
    price: float
    discount_price: Optional[float] = None
    stock_quantity: int = 0
    is_active: bool = True
    size: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None



class CategoryCreate(CategoryBase):
    image: Optional[str] = None


class SubcategoryCreate(SubcategoryBase):
    pass


class ProductImageCreate(ProductImageBase):
    product_id: int


class ProductVariationCreate(ProductVariationBase):
    product_id: int


class ProductCreate(ProductBase):
    images: Optional[List[ProductImageCreate]] = []
    variations: Optional[List[ProductVariationCreate]] = []


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None


class ProductImageUpdate(BaseModel):
    image_path: Optional[str] = None
    alt_text: Optional[str] = None
    is_primary: Optional[bool] = None
    display_order: Optional[int] = None


class ProductVariationUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    size: Optional[str] = None
    color: Optional[str] = None
    material: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    weight: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    color: Optional[str] = None
    subcategory_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int
    slug: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubcategoryResponse(SubcategoryBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductImageResponse(ProductImageBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductVariationResponse(ProductVariationBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductResponse(ProductBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    images: Optional[List[ProductImageResponse]] = []
    variations: Optional[List[ProductVariationResponse]] = []

    class Config:
        from_attributes = True


class CategoryDetailResponse(CategoryResponse):
    subcategories: List[SubcategoryResponse] = []

    class Config:
        from_attributes = True


class SubcategoryDetailResponse(SubcategoryResponse):
    category: CategoryResponse
    products: List[ProductResponse] = []

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    items: List[CategoryResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True


class SubcategoryListResponse(BaseModel):
    items: List[SubcategoryResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(10, ge=1, le=100, description="Items per page")