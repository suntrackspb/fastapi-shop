from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    def get_multi_by_parent(
        self, db: Session, *, parent_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        query = db.query(Category)
        if parent_id is None:
            query = query.filter(Category.parent_id.is_(None))
        else:
            query = query.filter(Category.parent_id == parent_id)
        return query.order_by(Category.order).offset(skip).limit(limit).all()

    def get_tree(self, db: Session) -> List[Category]:
        """Get full category tree with subcategories"""
        def get_subcategories(category: Category) -> List[Category]:
            subcategories = db.query(Category).filter(
                Category.parent_id == category.id
            ).order_by(Category.order).all()
            for subcategory in subcategories:
                subcategory.subcategories = get_subcategories(subcategory)
            return subcategories

        root_categories = db.query(Category).filter(
            Category.parent_id.is_(None)
        ).order_by(Category.order).all()
        
        for category in root_categories:
            category.subcategories = get_subcategories(category)
        
        return root_categories

    def get_with_products_count(self, db: Session, *, id: int) -> Optional[Category]:
        """Get category with count of products"""
        return db.query(
            Category,
            func.count(Category.products).label('products_count')
        ).outerjoin(
            Category.products
        ).filter(
            Category.id == id
        ).group_by(Category.id).first()

    def create_with_image(
        self, db: Session, *, obj_in: CategoryCreate, image_path: Optional[str] = None
    ) -> Category:
        obj_in_data = obj_in.model_dump()
        if image_path:
            obj_in_data["image"] = image_path
        db_obj = Category(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_image(
        self,
        db: Session,
        *,
        db_obj: Category,
        obj_in: CategoryUpdate,
        image_path: Optional[str] = None
    ) -> Category:
        update_data = obj_in.model_dump(exclude_unset=True)
        if image_path:
            update_data["image"] = image_path
        return super().update(db, db_obj=db_obj, obj_in=update_data)


category = CRUDCategory(Category) 