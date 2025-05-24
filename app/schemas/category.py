from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from app.schemas.base import BaseResponseSchema, TimestampSchema


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0


class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    parent_id: Optional[int] = None


class CategoryInDB(CategoryBase, BaseResponseSchema, TimestampSchema):
    parent_id: Optional[int] = None
    image: Optional[str] = None


class CategoryResponse(CategoryInDB):
    subcategories: List['CategoryResponse'] = []
    products_count: int = 0


# Update forward reference
CategoryResponse.model_rebuild() 