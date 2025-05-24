from typing import Optional, List
from pydantic import BaseModel, confloat
from app.schemas.base import BaseResponseSchema, TimestampSchema


class ProductImageBase(BaseModel):
    image_path: str
    order: Optional[int] = 0


class ProductImageCreate(ProductImageBase):
    variation_id: Optional[int] = None


class ProductImageResponse(ProductImageBase, BaseResponseSchema):
    variation_id: Optional[int] = None


class ProductVariationBase(BaseModel):
    color_name: str
    color_hex: str
    price: confloat(gt=0)
    is_available: bool = True


class ProductVariationCreate(ProductVariationBase):
    pass


class ProductVariationUpdate(BaseModel):
    color_name: Optional[str] = None
    color_hex: Optional[str] = None
    price: Optional[confloat(gt=0)] = None
    is_available: Optional[bool] = None


class ProductVariationResponse(ProductVariationBase, BaseResponseSchema, TimestampSchema):
    images: List[ProductImageResponse] = []


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    is_available: bool = True


class ProductCreate(ProductBase):
    variations: List[ProductVariationCreate]
    images: List[ProductImageCreate]


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    is_available: Optional[bool] = None


class ProductResponse(ProductBase, BaseResponseSchema, TimestampSchema):
    variations: List[ProductVariationResponse] = []
    images: List[ProductImageResponse] = []
    category_name: str 