from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import app.schemas.user as user_schemas
import app.crud.crud_user as crud_user
from app.db.session import get_db
from app.core.security import create_access_token, verify_password
from app.schemas.token import Token
from app.deps import get_current_active_user # We'll create this next

router = APIRouter()

@router.post("/register", response_model=user_schemas.User)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: user_schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud_user.create_user(db=db, user=user_in)
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud_user.get_user_by_email(db, email=form_data.username) # Using email as username
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(subject=user.email) # Use email as subject for JWT
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=user_schemas.User)
def read_users_me(
    current_user: user_schemas.User = Depends(get_current_active_user),
):
    """
    Get current user.
    """
    return current_user

# TODO: Add other user endpoints (get by id, update, list users for admin etc.)