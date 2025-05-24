from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_product, crud_category
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductVariationCreate
)
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ProductResponse])
def get_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get list of products.
    """
    if category_id:
        products = crud_product.product.get_multi_by_category(
            db, category_id=category_id, skip=skip, limit=limit
        )
    else:
        products = crud_product.product.get_multi(db, skip=skip, limit=limit)
    return products


@router.get("/search", response_model=List[ProductResponse])
def search_products(
    *,
    db: Session = Depends(deps.get_db),
    query: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Search products by name or description.
    """
    products = crud_product.product.search(
        db, query=query, skip=skip, limit=limit
    )
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get product by ID.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate = Depends(),
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Create new product.
    """
    # Check if category exists
    category = crud_category.category.get(db, id=product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    # Check if product with same name exists
    product = crud_product.product.get_by_name(db, name=product_in.name)
    if product:
        raise HTTPException(
            status_code=400,
            detail="Product with this name already exists"
        )
    
    product = crud_product.product.create_with_variations(
        db, obj_in=product_in
    )
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: ProductUpdate = Depends(),
    variations: Optional[List[ProductVariationCreate]] = None,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Update product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if category exists if it's being updated
    if product_in.category_id:
        category = crud_category.category.get(db, id=product_in.category_id)
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
    
    product = crud_product.product.update_with_variations(
        db, db_obj=product, obj_in=product_in, variations=variations
    )
    return product


@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Delete product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = crud_product.product.remove(db, id=product_id)
    return product


@router.get("/{product_id}/variations", response_model=List[ProductVariationCreate])
def get_product_variations(
    product_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get available variations for a product.
    """
    product = crud_product.product.get(db, id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    variations = crud_product.product.get_available_variations(
        db, product_id=product_id
    )
    return variations 