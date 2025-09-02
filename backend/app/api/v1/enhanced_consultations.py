# Enhanced Consultation API endpoints with specialized medical analysis

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import json
from datetime import datetime

from app.core.deps import get_db, get_current_user
from app.models.models import User, Consultation, SymptomTimeline, SpecializedAnalysis, Analysis
from app.schemas.schemas import (
    ConsultationCreate, ConsultationUpdate, Consultation as ConsultationSchema,
    ConsultationDetail, SymptomSubmission, AnalysisRequest, AnalysisResponse,
    SymptomTimelineCreate, SymptomTimeline as SymptomTimelineSchema,
    EnhancedAnalysisRequest, ComprehensiveAnalysisResponse,
    SpecializedAnalysisCreate, SpecializedAnalysis as SpecializedAnalysisSchema,
    AnalysisTypeEnum, EmergencyScreeningResult, TimelineAnalysisResult,
    ErrorResponse
)
from app.services.ai_service import ai_analysis_service
from app.services.specialized_medical_service import specialized_medical_service, SymptomTimelineEntry
from app.services.timeline_analysis_service import timeline_analyzer

router = APIRouter()


@router.post("/", response_model=ConsultationSchema)
async def create_consultation(
    consultation: ConsultationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new medical consultation"""
    db_consultation = Consultation(
        user_id=current_user.id,
        chief_complaint=consultation.chief_complaint,
        symptoms=consultation.symptoms
    )
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    return db_consultation


@router.get("/", response_model=List[ConsultationSchema])
async def get_consultations(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's consultations"""
    consultations = db.query(Consultation).filter(
        Consultation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return consultations


@router.get("/{consultation_id}", response_model=ConsultationDetail)
async def get_consultation(
    consultation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific consultation with details"""
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
    consultation_id: UUID,
    consultation_update: ConsultationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update consultation details"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Update fields
    for field, value in consultation_update.dict(exclude_unset=True).items():
        setattr(consultation, field, value)
    
    db.commit()
    db.refresh(consultation)
    return consultation


@router.post("/{consultation_id}/symptoms")
async def submit_symptoms(
    consultation_id: UUID,
    symptoms: SymptomSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit symptoms for a consultation"""
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
    consultation.chief_complaint = symptoms.chief_complaint
    consultation.symptoms = symptoms.dict()
    consultation.status = "active"
    
    db.commit()
    return {"message": "Symptoms submitted successfully"}


@router.post("/{consultation_id}/timeline", response_model=SymptomTimelineSchema)
async def add_timeline_entry(
    consultation_id: UUID,
    timeline_entry: SymptomTimelineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a symptom timeline entry"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Create timeline entry
    db_timeline_entry = SymptomTimeline(
        consultation_id=consultation_id,
        symptom=timeline_entry.symptom,
        severity=timeline_entry.severity,
        location=timeline_entry.location,
        quality=timeline_entry.quality,
        duration=timeline_entry.duration,
        notes=timeline_entry.notes,
        recorded_at=timeline_entry.recorded_at
    )
    
    db.add(db_timeline_entry)
    db.commit()
    db.refresh(db_timeline_entry)
    return db_timeline_entry


@router.get("/{consultation_id}/timeline", response_model=List[SymptomTimelineSchema])
async def get_timeline(
    consultation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get symptom timeline for a consultation"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    timeline = db.query(SymptomTimeline).filter(
        SymptomTimeline.consultation_id == consultation_id
    ).order_by(SymptomTimeline.recorded_at).all()
    
    return timeline


@router.post("/{consultation_id}/analyze", response_model=AnalysisResponse)
async def analyze_consultation_basic(
    consultation_id: UUID,
    analysis_request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Basic consultation analysis (backward compatibility)"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    try:
        # Get consultation data
        symptoms = consultation.symptoms if analysis_request.include_symptoms else None
        
        # Get test reports if requested
        test_report_text = None
        if analysis_request.include_test_reports:
            test_reports = consultation.test_reports
            if test_reports:
                test_report_text = "\n".join([
                    report.extracted_text for report in test_reports 
                    if report.extracted_text
                ])
        
        # Get medical history if requested
        medical_history = None
        if analysis_request.include_medical_history and current_user.medical_history:
            medical_history = {
                "allergies": current_user.medical_history[0].allergies,
                "medications": current_user.medical_history[0].medications,
                "conditions": current_user.medical_history[0].conditions,
                "surgeries": current_user.medical_history[0].surgeries,
                "family_history": current_user.medical_history[0].family_history
            }
        
        # Perform AI analysis
        analysis_result = await ai_analysis_service.analyze_consultation(
            symptoms=symptoms,
            test_report_text=test_report_text,
            medical_history=medical_history,
            chief_complaint=consultation.chief_complaint
        )
        
        # Save analysis to database
        db_analysis = Analysis(
            consultation_id=consultation_id,
            ai_analysis=analysis_result["ai_analysis"],
            risk_level=analysis_result["risk_level"],
            summary=analysis_result["summary"],
            recommendations=analysis_result.get("recommendations", []),
            emergency_actions=analysis_result.get("emergency_alert", {}).get("immediate_actions", []) if analysis_result.get("emergency_alert") else [],
            follow_up_suggestions=analysis_result.get("follow_up_suggestions", []),
            model_version="openai/gpt-oss-120b:free",
            confidence_score=analysis_result.get("confidence_score", 75)
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Update consultation status
        consultation.status = "completed"
        db.commit()
        
        return AnalysisResponse(
            analysis_id=db_analysis.id,
            consultation_id=consultation_id,
            summary=analysis_result["summary"],
            risk_level=analysis_result["risk_level"],
            key_findings=analysis_result.get("key_findings", []),
            recommendations=analysis_result.get("recommendations", []),
            emergency_alert=analysis_result.get("emergency_alert"),
            follow_up_suggestions=analysis_result.get("follow_up_suggestions", []),
            confidence_score=analysis_result.get("confidence_score", 75),
            disclaimer=analysis_result.get("disclaimer", "This analysis is for informational purposes only.")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/{consultation_id}/analyze/comprehensive", response_model=ComprehensiveAnalysisResponse)
async def analyze_consultation_comprehensive(
    consultation_id: UUID,
    analysis_request: EnhancedAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Comprehensive consultation analysis with specialized models and timeline analysis"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    try:
        # Prepare data for analysis
        symptoms = consultation.symptoms if analysis_request.include_symptoms else None
        
        # Get test reports
        test_report_text = None
        if analysis_request.include_test_reports:
            test_reports = consultation.test_reports
            if test_reports:
                test_report_text = "\n".join([
                    report.extracted_text for report in test_reports 
                    if report.extracted_text
                ])
        
        # Get medical history
        medical_history = None
        if analysis_request.include_medical_history and current_user.medical_history:
            medical_history = {
                "allergies": current_user.medical_history[0].allergies,
                "medications": current_user.medical_history[0].medications,
                "conditions": current_user.medical_history[0].conditions,
                "surgeries": current_user.medical_history[0].surgeries,
                "family_history": current_user.medical_history[0].family_history
            }
        
        # Get timeline data
        timeline_data = None
        timeline_entries = []
        if analysis_request.include_timeline_analysis:
            timeline_records = db.query(SymptomTimeline).filter(
                SymptomTimeline.consultation_id == consultation_id
            ).order_by(SymptomTimeline.recorded_at).all()
            
            timeline_entries = [
                SymptomTimelineEntry(
                    timestamp=record.recorded_at,
                    symptom=record.symptom,
                    severity=record.severity,
                    location=record.location,
                    quality=record.quality,
                    duration=record.duration,
                    notes=record.notes
                )
                for record in timeline_records
            ]
        
        # Perform analyses in parallel
        analysis_results = {}
        
        # Basic AI analysis (always performed)
        if AnalysisTypeEnum.GENERAL in analysis_request.analysis_types:
            general_analysis = await ai_analysis_service.analyze_consultation(
                symptoms=symptoms,
                test_report_text=test_report_text,
                medical_history=medical_history,
                chief_complaint=consultation.chief_complaint
            )
            analysis_results["general"] = general_analysis
        
        # Emergency screening
        emergency_result = None
        if analysis_request.include_emergency_screening:
            emergency_analysis = await specialized_medical_service.emergency_screening_analysis(
                symptoms=symptoms or {},
                chief_complaint=consultation.chief_complaint,
                timeline=timeline_entries
            )
            emergency_result = EmergencyScreeningResult(**emergency_analysis)
            analysis_results["emergency"] = emergency_analysis
        
        # Timeline analysis
        timeline_result = None
        if analysis_request.include_timeline_analysis and timeline_entries:
            timeline_analysis = await timeline_analyzer.analyze_comprehensive_timeline(
                timeline_entries,
                symptoms
            )
            timeline_result = TimelineAnalysisResult(
                timeline_summary=timeline_analysis["ai_analysis"].get("summary", "Timeline analysis completed"),
                identified_patterns=[],  # Simplified for response
                progression_analysis=timeline_analysis["pattern_analysis"],
                risk_trajectory=timeline_analysis["risk_assessment"],
                recommendations=timeline_analysis["clinical_recommendations"],
                ai_insights=timeline_analysis["ai_analysis"]
            )
            analysis_results["timeline"] = timeline_analysis
        
        # Additional specialized analyses
        specialized_analyses = []
        for analysis_type in analysis_request.analysis_types:
            if analysis_type != AnalysisTypeEnum.GENERAL:
                try:
                    if analysis_type == AnalysisTypeEnum.CLINICAL_ANALYSIS:
                        clinical_analysis = await specialized_medical_service.clinical_differential_analysis(
                            symptoms=symptoms or {},
                            test_results=test_report_text,
                            medical_history=medical_history,
                            timeline=timeline_entries
                        )
                        
                        # Save specialized analysis
                        db_specialized = SpecializedAnalysis(
                            consultation_id=consultation_id,
                            analysis_type=analysis_type,
                            model_used="openai/gpt-oss-120b:free",
                            analysis_results=clinical_analysis,
                            summary=clinical_analysis.get("summary", "Clinical analysis completed"),
                            confidence_score=clinical_analysis.get("confidence", 75)
                        )
                        
                        db.add(db_specialized)
                        specialized_analyses.append(db_specialized)
                        
                except Exception as e:
                    # Log error but continue with other analyses
                    print(f"Specialized analysis {analysis_type} failed: {e}")
        
        # Save main analysis
        main_analysis = analysis_results.get("general")
        if main_analysis:
            db_analysis = Analysis(
                consultation_id=consultation_id,
                ai_analysis=main_analysis["ai_analysis"],
                risk_level=main_analysis["risk_level"],
                summary=main_analysis["summary"],
                recommendations=main_analysis.get("recommendations", []),
                emergency_actions=main_analysis.get("emergency_alert", {}).get("immediate_actions", []) if main_analysis.get("emergency_alert") else [],
                follow_up_suggestions=main_analysis.get("follow_up_suggestions", []),
                model_version="openai/gpt-oss-120b:free",
                confidence_score=main_analysis.get("confidence_score", 75)
            )
            
            db.add(db_analysis)
        
        # Commit all analyses
        db.commit()
        
        # Determine overall risk level
        overall_risk = "moderate"
        if emergency_result and emergency_result.is_emergency:
            overall_risk = "critical"
        elif main_analysis and main_analysis["risk_level"] in ["high", "critical"]:
            overall_risk = main_analysis["risk_level"]
        elif timeline_result and timeline_result.risk_trajectory.get("current_risk") == "high":
            overall_risk = "high"
        
        # Generate priority recommendations
        priority_recommendations = []
        
        if emergency_result and emergency_result.is_emergency:
            priority_recommendations.extend([
                {
                    "category": "emergency",
                    "action": action,
                    "priority": "critical",
                    "timeline": "Immediately"
                }
                for action in emergency_result.immediate_actions
            ])
        
        if main_analysis and main_analysis.get("recommendations"):
            priority_recommendations.extend(main_analysis["recommendations"][:3])  # Top 3
        
        if timeline_result and timeline_result.recommendations:
            priority_recommendations.extend([
                rec for rec in timeline_result.recommendations 
                if rec.get("priority") in ["critical", "high"]
            ])
        
        # Update consultation status
        consultation.status = "completed"
        db.commit()
        
        return ComprehensiveAnalysisResponse(
            consultation_id=consultation_id,
            general_analysis=AnalysisResponse(
                analysis_id=db_analysis.id if main_analysis else None,
                consultation_id=consultation_id,
                summary=main_analysis["summary"] if main_analysis else "Analysis completed",
                risk_level=main_analysis["risk_level"] if main_analysis else "moderate",
                key_findings=main_analysis.get("key_findings", []) if main_analysis else [],
                recommendations=main_analysis.get("recommendations", []) if main_analysis else [],
                emergency_alert=main_analysis.get("emergency_alert") if main_analysis else None,
                follow_up_suggestions=main_analysis.get("follow_up_suggestions", []) if main_analysis else [],
                confidence_score=main_analysis.get("confidence_score", 75) if main_analysis else 75,
                disclaimer=main_analysis.get("disclaimer", "This analysis is for informational purposes only.") if main_analysis else "This analysis is for informational purposes only."
            ) if main_analysis else None,
            emergency_screening=emergency_result,
            timeline_analysis=timeline_result,
            specialized_analyses=[SpecializedAnalysisSchema.from_orm(sa) for sa in specialized_analyses],
            overall_risk_level=overall_risk,
            priority_recommendations=priority_recommendations[:5],  # Top 5 priority items
            analysis_timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive analysis failed: {str(e)}"
        )


@router.get("/{consultation_id}/specialized-analyses", response_model=List[SpecializedAnalysisSchema])
async def get_specialized_analyses(
    consultation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all specialized analyses for a consultation"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    analyses = db.query(SpecializedAnalysis).filter(
        SpecializedAnalysis.consultation_id == consultation_id
    ).order_by(SpecializedAnalysis.created_at.desc()).all()
    
    return analyses


@router.delete("/{consultation_id}")
async def delete_consultation(
    consultation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a consultation and all associated data"""
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Delete associated records (cascade should handle this, but explicit is better)
    db.query(SymptomTimeline).filter(SymptomTimeline.consultation_id == consultation_id).delete()
    db.query(SpecializedAnalysis).filter(SpecializedAnalysis.consultation_id == consultation_id).delete()
    db.query(Analysis).filter(Analysis.consultation_id == consultation_id).delete()
    
    # Delete consultation
    db.delete(consultation)
    db.commit()
    
    return {"message": "Consultation deleted successfully"}