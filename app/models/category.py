from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Category(Base):
    name = Column(String, nullable=False)
    description = Column(String)
    image = Column(String)  # Path to image
    order = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    
    # Relationships
    parent = relationship("Category", remote_side="Category.id", backref="subcategories")
    products = relationship("Product", back_populates="category") 