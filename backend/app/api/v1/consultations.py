# Consultation API endpoints

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.models import (
    User, Consultation, Analysis, TestReport, MedicalHistory,
    ConsultationStatusEnum, RiskLevelEnum
)
from app.schemas.schemas import (
    ConsultationCreate, ConsultationUpdate, Consultation as ConsultationSchema,
    ConsultationDetail, SymptomSubmission, AnalysisRequest,
    AnalysisResponse, Analysis as AnalysisSchema
)
from app.services.ai_service import ai_analysis_service

router = APIRouter()


@router.post("/", response_model=ConsultationSchema, status_code=status.HTTP_201_CREATED)
async def create_consultation(
    consultation_data: ConsultationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new consultation
    
    Args:
        consultation_data: Consultation creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ConsultationSchema: Created consultation
    """
    consultation = Consultation(
        user_id=current_user.id,
        chief_complaint=consultation_data.chief_complaint,
        symptoms=consultation_data.symptoms,
        status=ConsultationStatusEnum.DRAFT
    )
    
    db.add(consultation)
    db.commit()
    db.refresh(consultation)
    
    return consultation


@router.get("/", response_model=List[ConsultationSchema])
async def get_user_consultations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20
):
    """
    Get user's consultations
    
    Args:
        current_user: Current authenticated user
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List[ConsultationSchema]: User's consultations
    """
    consultations = db.query(Consultation).filter(
        Consultation.user_id == current_user.id
    ).order_by(Consultation.created_at.desc()).offset(skip).limit(limit).all()
    
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationDetail)
async def get_consultation(
    consultation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed consultation information
    
    Args:
        consultation_id: Consultation ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ConsultationDetail: Detailed consultation information
        
    Raises:
        HTTPException: If consultation not found
    """
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    return consultation


@router.put("/{consultation_id}", response_model=ConsultationSchema)
async def update_consultation(
    consultation_id: str,
    consultation_update: ConsultationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update consultation
    
    Args:
        consultation_id: Consultation ID
        consultation_update: Consultation update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ConsultationSchema: Updated consultation
        
    Raises:
        HTTPException: If consultation not found
    """
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Update consultation fields
    update_data = consultation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(consultation, field, value)
    
    db.commit()
    db.refresh(consultation)
    
    return consultation


@router.post("/{consultation_id}/symptoms", response_model=ConsultationSchema)
async def submit_symptoms(
    consultation_id: str,
    symptom_data: SymptomSubmission,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit symptoms for a consultation
    
    Args:
        consultation_id: Consultation ID
        symptom_data: Symptom submission data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ConsultationSchema: Updated consultation
        
    Raises:
        HTTPException: If consultation not found
    """
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Update consultation with symptoms
    consultation.chief_complaint = symptom_data.chief_complaint
    consultation.symptoms = {
        "symptoms": [symptom.dict() for symptom in symptom_data.symptoms],
        "submitted_at": datetime.utcnow().isoformat()
    }
    consultation.status = ConsultationStatusEnum.ACTIVE
    
    db.commit()
    db.refresh(consultation)
    
    return consultation


@router.post("/{consultation_id}/analyze", response_model=AnalysisResponse)
async def analyze_consultation(
    consultation_id: str,
    analysis_request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Analyze consultation using AI
    
    Args:
        consultation_id: Consultation ID
        analysis_request: Analysis request parameters
        background_tasks: Background tasks for async processing
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        AnalysisResponse: AI analysis results
        
    Raises:
        HTTPException: If consultation not found
    """
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Gather data for analysis
    analysis_data = {}
    
    if analysis_request.include_symptoms:
        analysis_data["symptoms"] = consultation.symptoms
        analysis_data["chief_complaint"] = consultation.chief_complaint
    
    if analysis_request.include_test_reports:
        test_reports = db.query(TestReport).filter(
            TestReport.consultation_id == consultation_id
        ).all()
        
        # Combine all test report texts
        test_texts = []
        for report in test_reports:
            if report.extracted_text:
                test_texts.append(f"File: {report.file_name}\n{report.extracted_text}")
        
        if test_texts:
            analysis_data["test_report_text"] = "\n\n".join(test_texts)
    
    if analysis_request.include_medical_history:
        medical_history = db.query(MedicalHistory).filter(
            MedicalHistory.user_id == current_user.id
        ).first()
        
        if medical_history:
            analysis_data["medical_history"] = {
                "allergies": medical_history.allergies,
                "medications": medical_history.medications,
                "conditions": medical_history.conditions,
                "surgeries": medical_history.surgeries,
                "family_history": medical_history.family_history
            }
    
    # Perform AI analysis
    try:
        ai_result = await ai_analysis_service.analyze_consultation(**analysis_data)
        
        # Save analysis to database
        analysis = Analysis(
            consultation_id=consultation_id,
            ai_analysis=ai_result["ai_analysis"],
            risk_level=RiskLevelEnum(ai_result["risk_level"]),
            summary=ai_result["summary"],
            recommendations=ai_result.get("recommendations"),
            emergency_actions=ai_result.get("emergency_alert", {}).get("immediate_actions") if ai_result.get("emergency_alert") else None,
            follow_up_suggestions=ai_result.get("follow_up_suggestions"),
            confidence_score=ai_result.get("confidence_score"),
            model_version="gpt-4"
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Update consultation status
        consultation.status = ConsultationStatusEnum.COMPLETED
        db.commit()
        
        # Prepare response
        response = AnalysisResponse(
            analysis_id=analysis.id,
            consultation_id=consultation_id,
            summary=ai_result["summary"],
            risk_level=RiskLevelEnum(ai_result["risk_level"]),
            key_findings=ai_result.get("key_findings", []),
            recommendations=ai_result.get("recommendations", []),
            emergency_alert=ai_result.get("emergency_alert"),
            follow_up_suggestions=ai_result.get("follow_up_suggestions", []),
            confidence_score=ai_result.get("confidence_score", 75),
            disclaimer=ai_result.get("disclaimer", "This is for informational purposes only.")
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/{consultation_id}/analyses", response_model=List[AnalysisSchema])
async def get_consultation_analyses(
    consultation_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all analyses for a consultation
    
    Args:
        consultation_id: Consultation ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[AnalysisSchema]: Consultation analyses
        
    Raises:
        HTTPException: If consultation not found
    """
    # Verify consultation exists and belongs to user
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Get analyses
    analyses = db.query(Analysis).filter(
        Analysis.consultation_id == consultation_id
    ).order_by(Analysis.created_at.desc()).all()
    
    return analyses