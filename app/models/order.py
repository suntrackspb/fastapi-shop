from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum


class OrderStatus(str, enum.Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class PaymentMethod(str, enum.Enum):
    CARD = "card"
    SBP = "sbp"
    CASH = "cash"


class DeliveryMethod(str, enum.Enum):
    COURIER = "courier"
    PICKUP = "pickup"


class Order(Base):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Contact information
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    
    # Delivery information
    delivery_method = Column(Enum(DeliveryMethod), nullable=False)
    delivery_address = Column(Text, nullable=True)  # Required for courier delivery
    
    # Payment information
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    # Relationships
    user = relationship("User", backref="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    variation_id = Column(Integer, ForeignKey("productvariation.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at the time of order
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    variation = relationship("ProductVariation") 