from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    parent_id: Optional[int] = None,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get list of categories.
    """
    categories = crud_category.category.get_multi_by_parent(
        db, parent_id=parent_id, skip=skip, limit=limit
    )
    return categories


@router.get("/tree", response_model=List[CategoryResponse])
def get_category_tree(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get full category tree with subcategories.
    """
    return crud_category.category.get_tree(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get category by ID.
    """
    category = crud_category.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate = Depends(),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Create new category.
    """
    category = crud_category.category.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists"
        )
    
    # Handle image upload if provided
    image_path = None
    if image:
        # TODO: Implement image upload logic
        image_path = f"categories/{image.filename}"
    
    category = crud_category.category.create_with_image(
        db, obj_in=category_in, image_path=image_path
    )
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: CategoryUpdate = Depends(),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Update category.
    """
    category = crud_category.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Handle image upload if provided
    image_path = None
    if image:
        # TODO: Implement image upload logic
        image_path = f"categories/{image.filename}"
    
    category = crud_category.category.update_with_image(
        db, db_obj=category, obj_in=category_in, image_path=image_path
    )
    return category


@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Delete category.
    """
    category = crud_category.category.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has subcategories
    subcategories = crud_category.category.get_multi_by_parent(
        db, parent_id=category_id
    )
    if subcategories:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with subcategories"
        )
    
    category = crud_category.category.remove(db, id=category_id)
    return category 