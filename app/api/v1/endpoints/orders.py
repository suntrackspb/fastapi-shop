from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_order, crud_product
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get list of orders for current user.
    """
    if deps.get_current_active_admin(current_user):
        # Admin can see all orders
        orders = crud_order.order.get_multi(db, skip=skip, limit=limit)
    else:
        # Regular users can only see their own orders
        orders = crud_order.order.get_by_user(
            db, user_id=current_user.id, skip=skip, limit=limit
        )
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get order by ID.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user has permission to view this order
    if not deps.get_current_active_admin(current_user) and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to view this order"
        )
    
    return order


@router.post("/", response_model=OrderResponse)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Create new order.
    """
    # Validate product variations
    for item in order_in.items:
        variation = crud_product.product.get_available_variations(
            db, product_id=item.product_id
        )
        if not variation:
            raise HTTPException(
                status_code=400,
                detail=f"Product variation not available for product ID {item.product_id}"
            )
    
    # Set user ID from current user
    order_data = order_in.model_dump()
    order_data["user_id"] = current_user.id
    
    order = crud_order.order.create_with_items(
        db, obj_in=order_in
    )
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: User = Depends(deps.get_current_active_admin)
):
    """
    Update order (admin only).
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = crud_order.order.update(
        db, db_obj=order, obj_in=order_in
    )
    return order


@router.get("/{order_id}/total", response_model=float)
def get_order_total(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get total amount for an order.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user has permission to view this order
    if not deps.get_current_active_admin(current_user) and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to view this order"
        )
    
    return crud_order.order.get_total_amount(db, id=order_id)


@router.get("/{order_id}/status", response_model=str)
def get_order_status(
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get status of an order.
    """
    order = crud_order.order.get(db, id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if user has permission to view this order
    if not deps.get_current_active_admin(current_user) and order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions to view this order"
        )
    
    return crud_order.order.get_order_status(db, id=order_id) 