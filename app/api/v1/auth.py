from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.core import security
from app.schemas.token import Token 

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive. Please contact an Admin."
        )    

    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }