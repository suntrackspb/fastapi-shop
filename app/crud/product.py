from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.product import Product, ProductVariation, ProductImage
from app.schemas.product import ProductCreate, ProductUpdate, ProductVariationCreate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == name).first()

    def get_multi_by_category(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(Product)
            .filter(Product.category_id == category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_variations(
        self, db: Session, *, obj_in: ProductCreate
    ) -> Product:
        # Create product
        obj_in_data = obj_in.model_dump(exclude={"variations", "images"})
        db_obj = Product(**obj_in_data)
        db.add(db_obj)
        db.flush()  # Flush to get the product ID

        # Create variations
        for variation_in in obj_in.variations:
            variation = ProductVariation(
                product_id=db_obj.id,
                **variation_in.model_dump()
            )
            db.add(variation)
        db.flush()

        # Create images
        for image_in in obj_in.images:
            image = ProductImage(
                product_id=db_obj.id,
                variation_id=image_in.variation_id,
                **image_in.model_dump(exclude={"variation_id"})
            )
            db.add(image)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_variations(
        self,
        db: Session,
        *,
        db_obj: Product,
        obj_in: ProductUpdate,
        variations: Optional[List[ProductVariationCreate]] = None
    ) -> Product:
        # Update product
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update variations if provided
        if variations:
            # Delete existing variations
            db.query(ProductVariation).filter(
                ProductVariation.product_id == db_obj.id
            ).delete()

            # Create new variations
            for variation_in in variations:
                variation = ProductVariation(
                    product_id=db_obj.id,
                    **variation_in.model_dump()
                )
                db.add(variation)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        search_query = f"%{query}%"
        return (
            db.query(Product)
            .filter(
                (Product.name.ilike(search_query)) |
                (Product.description.ilike(search_query))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_available_variations(
        self, db: Session, *, product_id: int
    ) -> List[ProductVariation]:
        return (
            db.query(ProductVariation)
            .filter(
                ProductVariation.product_id == product_id,
                ProductVariation.is_available == True
            )
            .all()
        )


product = CRUDProduct(Product) 