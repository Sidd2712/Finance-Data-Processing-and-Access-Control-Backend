from fastapi import Header, HTTPException, Depends
from sqlmodel import Session
from uuid import UUID
from app.database import get_session
from app.models.user import User, UserRole

def get_current_user(
    x_user_id: UUID = Header(...), 
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to fetch the user from the database based on a Header ID.
    In a real app, this would decode a JWT token.
    """
    user = session.get(User, x_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

class RoleChecker:
    """
    A reusable class to check if a user has the required permissions.
    """
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Role '{user.role}' does not have permission to perform this action"
            )
        return user