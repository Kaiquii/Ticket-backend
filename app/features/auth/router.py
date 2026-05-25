from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.features.auth.model import User
from app.features.auth.schema import TokenResponse, UserCreate, UserLogin, UserResponse
from app.features.auth.service import authenticate_user, create_access_token, create_user, list_users


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, str(data.email), data.password)
    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


@router.get("/users", response_model=list[UserResponse])
def users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_users(db)
