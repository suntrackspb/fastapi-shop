from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Table
from sqlalchemy.orm import relationship
from app.models.base import Base


class Product(Base):
    name = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    category = relationship("Category", back_populates="products")
    variations = relationship("ProductVariation", back_populates="product")
    images = relationship("ProductImage", back_populates="product")


class ProductVariation(Base):
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    color_name = Column(String, nullable=False)
    color_hex = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Relationships
    product = relationship("Product", back_populates="variations")
    images = relationship("ProductImage", back_populates="variation")


class ProductImage(Base):
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    variation_id = Column(Integer, ForeignKey("productvariation.id"), nullable=True)
    image_path = Column(String, nullable=False)
    order = Column(Integer, default=0)
    
    # Relationships
    product = relationship("Product", back_populates="images")
    variation = relationship("ProductVariation", back_populates="images") 