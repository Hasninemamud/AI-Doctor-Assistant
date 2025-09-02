# User management API endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, MedicalHistory
from app.schemas.schemas import (
    User as UserSchema, UserUpdate,
    MedicalHistory as MedicalHistorySchema,
    MedicalHistoryCreate, MedicalHistoryUpdate
)

router = APIRouter()


@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user profile
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserSchema: User profile data
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    Args:
        user_update: User update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        UserSchema: Updated user profile
    """
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/me/medical-history", response_model=MedicalHistorySchema)
async def get_user_medical_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's medical history
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MedicalHistorySchema: User's medical history
        
    Raises:
        HTTPException: If medical history not found
    """
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.user_id == current_user.id
    ).first()
    
    if not medical_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found"
        )
    
    return medical_history


@router.post("/me/medical-history", response_model=MedicalHistorySchema, status_code=status.HTTP_201_CREATED)
async def create_user_medical_history(
    medical_history_data: MedicalHistoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create user's medical history
    
    Args:
        medical_history_data: Medical history data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MedicalHistorySchema: Created medical history
        
    Raises:
        HTTPException: If medical history already exists
    """
    # Check if medical history already exists
    existing_history = db.query(MedicalHistory).filter(
        MedicalHistory.user_id == current_user.id
    ).first()
    
    if existing_history:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical history already exists"
        )
    
    # Create medical history
    medical_history = MedicalHistory(
        user_id=current_user.id,
        **medical_history_data.dict()
    )
    
    db.add(medical_history)
    db.commit()
    db.refresh(medical_history)
    
    return medical_history


@router.put("/me/medical-history", response_model=MedicalHistorySchema)
async def update_user_medical_history(
    medical_history_update: MedicalHistoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update user's medical history
    
    Args:
        medical_history_update: Medical history update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MedicalHistorySchema: Updated medical history
        
    Raises:
        HTTPException: If medical history not found
    """
    medical_history = db.query(MedicalHistory).filter(
        MedicalHistory.user_id == current_user.id
    ).first()
    
    if not medical_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical history not found"
        )
    
    # Update medical history fields
    update_data = medical_history_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medical_history, field, value)
    
    db.commit()
    db.refresh(medical_history)
    
    return medical_history