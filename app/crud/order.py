from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_items(
        self, db: Session, *, obj_in: OrderCreate
    ) -> Order:
        # Create order
        obj_in_data = obj_in.model_dump(exclude={"items"})
        db_obj = Order(**obj_in_data)
        db.add(db_obj)
        db.flush()  # Flush to get the order ID

        # Create order items
        for item_in in obj_in.items:
            item = OrderItem(
                order_id=db_obj.id,
                **item_in.model_dump()
            )
            db.add(item)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_items(
        self,
        db: Session,
        *,
        db_obj: Order,
        obj_in: OrderUpdate,
        items: Optional[List[OrderItemCreate]] = None
    ) -> Order:
        # Update order
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # Update items if provided
        if items:
            # Delete existing items
            db.query(OrderItem).filter(
                OrderItem.order_id == db_obj.id
            ).delete()

            # Create new items
            for item_in in items:
                item = OrderItem(
                    order_id=db_obj.id,
                    **item_in.model_dump()
                )
                db.add(item)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_with_items(self, db: Session, *, id: int) -> Optional[Order]:
        return (
            db.query(Order)
            .filter(Order.id == id)
            .first()
        )

    def get_total_amount(self, db: Session, *, id: int) -> float:
        result = (
            db.query(func.sum(OrderItem.price * OrderItem.quantity))
            .filter(OrderItem.order_id == id)
            .scalar()
        )
        return result or 0.0

    def get_order_status(self, db: Session, *, id: int) -> str:
        order = self.get(db, id=id)
        if not order:
            return "not_found"
        return order.status


order = CRUDOrder(Order) 