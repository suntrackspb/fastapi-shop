from typing import Optional, List
from pydantic import BaseModel, confloat, conint
from app.models.order import OrderStatus, PaymentMethod, DeliveryMethod
from app.schemas.base import BaseResponseSchema, TimestampSchema
from app.schemas.product import ProductVariationResponse


class OrderItemBase(BaseModel):
    product_id: int
    variation_id: int
    quantity: conint(gt=0)
    price: confloat(gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase, BaseResponseSchema):
    product_name: str
    variation: ProductVariationResponse


class OrderBase(BaseModel):
    full_name: str
    email: str
    phone: str
    delivery_method: DeliveryMethod
    delivery_address: Optional[str] = None
    payment_method: PaymentMethod


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None


class OrderResponse(OrderBase, BaseResponseSchema, TimestampSchema):
    user_id: int
    status: OrderStatus
    total_amount: float
    items: List[OrderItemResponse] 