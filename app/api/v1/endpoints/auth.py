from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Refresh access token
    """
    access_token = security.create_access_token(current_user.id)
    refresh_token = security.create_refresh_token(current_user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.UserResponse)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user 