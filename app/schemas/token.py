from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class Token(BaseModel):
    """
    The schema for the successful login response.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    The schema for the internal data stored inside the JWT 'sub' field.
    This helps the 'get_current_user' dependency validate the token.
    """
    user_id: Optional[UUID] = None