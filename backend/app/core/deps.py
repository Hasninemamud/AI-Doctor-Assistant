# Authentication dependencies for FastAPI

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import verify_token, get_current_user_id
from app.models.models import User
from app.schemas.schemas import TokenData

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Verify and decode token
        user_id = get_current_user_id(credentials.credentials)
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
            
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user"
            )
            
        return user
        
    except Exception:
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (already handled in get_current_user)
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        User: Current active user
    """
    return current_user


def verify_refresh_token(refresh_token: str, db: Session) -> Optional[User]:
    """
    Verify refresh token and return user
    
    Args:
        refresh_token: JWT refresh token
        db: Database session
        
    Returns:
        Optional[User]: User if token is valid, None otherwise
    """
    payload = verify_token(refresh_token, "refresh")
    if payload is None:
        return None
    
    user_id = payload.get("sub")
    if user_id is None:
        return None
    
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    return user