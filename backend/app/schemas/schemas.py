# Pydantic schemas for request/response validation

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from uuid import UUID
import enum

from app.models.models import (
    GenderEnum, ConsultationStatusEnum, ProcessingStatusEnum,
    RiskLevelEnum, SenderTypeEnum, AnalysisTypeEnum, MedicalSpecialtyEnum
)


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        # Allow model_version field names
        protected_namespaces = ()


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    name: str
    date_of_birth: Optional[Union[date, str]] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @validator('date_of_birth', pre=True, allow_reuse=True)
    def parse_date_of_birth(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseSchema):
    name: Optional[str] = None
    date_of_birth: Optional[Union[date, str]] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None
    
    @validator('date_of_birth', pre=True, allow_reuse=True)
    def parse_date_of_birth(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v


class User(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLogin(BaseSchema):
    email: EmailStr
    password: str


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseSchema):
    user_id: Optional[str] = None


class RefreshTokenRequest(BaseSchema):
    refresh_token: str


# Medical History schemas
class MedicalHistoryBase(BaseSchema):
    allergies: Optional[List[str]] = None
    medications: Optional[List[Dict[str, Any]]] = None
    conditions: Optional[List[str]] = None
    surgeries: Optional[List[Dict[str, Any]]] = None
    family_history: Optional[List[str]] = None


class MedicalHistoryCreate(MedicalHistoryBase):
    pass


class MedicalHistoryUpdate(MedicalHistoryBase):
    pass


class MedicalHistory(MedicalHistoryBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


# Consultation schemas
class ConsultationBase(BaseSchema):
    chief_complaint: Optional[str] = None
    symptoms: Optional[Dict[str, Any]] = None


class ConsultationCreate(ConsultationBase):
    pass


class ConsultationUpdate(BaseSchema):
    chief_complaint: Optional[str] = None
    symptoms: Optional[Dict[str, Any]] = None
    status: Optional[ConsultationStatusEnum] = None


class Consultation(ConsultationBase):
    id: UUID
    user_id: UUID
    status: ConsultationStatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None


class ConsultationDetail(Consultation):
    test_reports: List["TestReport"] = []
    analyses: List["Analysis"] = []
    chat_messages: List["ChatMessage"] = []


# Test Report schemas
class TestReportBase(BaseSchema):
    file_name: str
    file_type: str


class TestReportCreate(TestReportBase):
    pass


class TestReport(TestReportBase):
    id: UUID
    consultation_id: UUID
    file_path: str
    file_size: int
    processing_status: ProcessingStatusEnum
    extracted_text: Optional[str] = None
    processed_data: Optional[Dict[str, Any]] = None
    uploaded_at: datetime
    processed_at: Optional[datetime] = None


# Analysis schemas
class AnalysisBase(BaseSchema):
    ai_analysis: Dict[str, Any]
    risk_level: RiskLevelEnum
    summary: Optional[str] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    emergency_actions: Optional[List[Dict[str, Any]]] = None
    follow_up_suggestions: Optional[List[str]] = None


class AnalysisCreate(AnalysisBase):
    consultation_id: UUID
    model_version: Optional[str] = None
    confidence_score: Optional[int] = None


class Analysis(AnalysisBase):
    id: UUID
    consultation_id: UUID
    model_version: Optional[str] = None
    confidence_score: Optional[int] = None
    created_at: datetime


# Chat Message schemas
class ChatMessageBase(BaseSchema):
    sender_type: SenderTypeEnum
    message_content: str
    message_metadata: Optional[Dict[str, Any]] = None


class ChatMessageCreate(ChatMessageBase):
    consultation_id: UUID


class ChatMessage(ChatMessageBase):
    id: UUID
    consultation_id: UUID
    timestamp: datetime


# File Upload schemas
class FileUploadResponse(BaseSchema):
    file_id: UUID
    file_name: str
    file_size: int
    upload_url: str
    processing_status: ProcessingStatusEnum


# Symptom schemas
class SymptomData(BaseSchema):
    location: Optional[str] = None
    severity: Optional[int] = None  # 1-10 scale
    duration: Optional[str] = None
    onset: Optional[str] = None
    quality: Optional[str] = None
    associated_symptoms: Optional[List[str]] = None
    aggravating_factors: Optional[List[str]] = None
    relieving_factors: Optional[List[str]] = None


class SymptomSubmission(BaseSchema):
    chief_complaint: str
    symptoms: List[SymptomData]
    medical_history: Optional[Dict[str, Any]] = None


# AI Analysis Request/Response schemas
class AnalysisRequest(BaseSchema):
    consultation_id: UUID
    include_test_reports: bool = True
    include_symptoms: bool = True
    include_medical_history: bool = True
    user_location: Optional[str] = None  # Add location for enhanced recommendations


class EmergencyAlert(BaseSchema):
    is_emergency: bool
    severity_level: RiskLevelEnum
    immediate_actions: List[str]
    emergency_contacts: List[str]
    message: str


class AnalysisResponse(BaseSchema):
    analysis_id: UUID
    consultation_id: UUID
    summary: str
    risk_level: RiskLevelEnum
    key_findings: List[str]
    recommendations: List[Dict[str, Any]]
    emergency_alert: Optional[EmergencyAlert] = None
    follow_up_suggestions: List[str]
    confidence_score: int
    disclaimer: str


# Error schemas
class ErrorResponse(BaseSchema):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ValidationError(BaseSchema):
    field: str
    message: str


class ValidationErrorResponse(BaseSchema):
    error: str = "Validation Error"
    details: List[ValidationError]


# Health check schema
class HealthResponse(BaseSchema):
    status: str
    service: str
    timestamp: datetime
    version: str = "1.0.0"


# Symptom Timeline schemas
class SymptomTimelineEntry(BaseSchema):
    symptom: str
    severity: Optional[int] = None  # 1-10 scale
    location: Optional[str] = None
    quality: Optional[str] = None
    duration: Optional[str] = None
    notes: Optional[str] = None
    recorded_at: datetime


class SymptomTimelineCreate(SymptomTimelineEntry):
    consultation_id: UUID


class SymptomTimeline(SymptomTimelineEntry):
    id: UUID
    consultation_id: UUID
    entered_at: datetime


# Specialized Analysis schemas
class TimelinePattern(BaseSchema):
    pattern_type: str
    description: str
    significance: str
    start_time: datetime
    end_time: Optional[datetime] = None
    severity_trend: Optional[str] = None  # improving, worsening, stable
    confidence: float = 0.0


class ProgressionAnalysis(BaseSchema):
    progression: str  # worsening, improving, stable, unknown
    severity_range: Optional[List[int]] = None
    symptom_count_trend: int = 0
    average_interval_hours: float = 0.0
    total_duration_hours: float = 0.0


class RiskTrajectory(BaseSchema):
    current_risk: str
    risk_trend: str  # increasing, stable, decreasing
    rapid_changes_count: int = 0
    average_recent_severity: float = 0.0


class EmergencyScreeningResult(BaseSchema):
    is_emergency: bool
    emergency_level: str  # none, low, moderate, high, critical
    red_flags: List[str]
    immediate_actions: List[str]
    time_to_care: str  # immediate, within_1_hour, within_4_hours, within_24_hours
    emergency_specialty: Optional[str] = None
    confidence: int
    reasoning: str


class TimelineAnalysisResult(BaseSchema):
    timeline_summary: str
    identified_patterns: List[TimelinePattern]
    progression_analysis: ProgressionAnalysis
    risk_trajectory: RiskTrajectory
    recommendations: List[Dict[str, Any]]
    ai_insights: Dict[str, Any]


class SpecializedAnalysisBase(BaseSchema):
    analysis_type: AnalysisTypeEnum
    medical_specialty: Optional[MedicalSpecialtyEnum] = None
    model_used: Optional[str] = None
    analysis_results: Dict[str, Any]
    summary: Optional[str] = None
    confidence_score: Optional[int] = None


class SpecializedAnalysisCreate(SpecializedAnalysisBase):
    consultation_id: UUID
    is_emergency: Optional[bool] = None
    emergency_level: Optional[str] = None
    red_flags: Optional[List[str]] = None
    identified_patterns: Optional[List[Dict[str, Any]]] = None
    progression_analysis: Optional[Dict[str, Any]] = None
    risk_trajectory: Optional[Dict[str, Any]] = None


class SpecializedAnalysis(SpecializedAnalysisBase):
    id: UUID
    consultation_id: UUID
    is_emergency: Optional[bool] = None
    emergency_level: Optional[str] = None
    red_flags: Optional[List[str]] = None
    identified_patterns: Optional[List[Dict[str, Any]]] = None
    progression_analysis: Optional[Dict[str, Any]] = None
    risk_trajectory: Optional[Dict[str, Any]] = None
    created_at: datetime


# Enhanced Analysis Request schemas
class EnhancedAnalysisRequest(BaseSchema):
    consultation_id: UUID
    analysis_types: List[AnalysisTypeEnum] = [AnalysisTypeEnum.GENERAL]
    include_emergency_screening: bool = True
    include_timeline_analysis: bool = True
    include_test_reports: bool = True
    include_symptoms: bool = True
    include_medical_history: bool = True


class ComprehensiveAnalysisResponse(BaseSchema):
    consultation_id: UUID
    general_analysis: Optional[AnalysisResponse] = None
    emergency_screening: Optional[EmergencyScreeningResult] = None
    timeline_analysis: Optional[TimelineAnalysisResult] = None
    specialized_analyses: List[SpecializedAnalysis] = []
    overall_risk_level: RiskLevelEnum
    priority_recommendations: List[Dict[str, Any]]
    analysis_timestamp: datetime


# Location-based Medical Service schemas
class HospitalInfo(BaseSchema):
    name: str
    address: str
    phone: str
    type: str  # General Hospital, Medical Center, Specialty Hospital, etc.
    specialty: Optional[str] = None
    rating: Optional[float] = None
    distance_km: Optional[float] = None
    emergency_services: bool = False
    accepts_insurance: bool = True
    website: Optional[str] = None
    directions_url: Optional[str] = None
    description: Optional[str] = None
    wait_time_minutes: Optional[int] = None
    trauma_level: Optional[str] = None  # For emergency facilities
    open_24_7: Optional[bool] = None


class DoctorInfo(BaseSchema):
    name: str
    specialty: str
    practice_name: Optional[str] = None
    address: str
    phone: str
    rating: Optional[float] = None
    years_experience: Optional[int] = None
    education: Optional[str] = None
    accepts_new_patients: bool = True
    accepts_insurance: bool = True
    distance_km: Optional[float] = None
    next_available: Optional[str] = None
    website: Optional[str] = None
    directions_url: Optional[str] = None
    languages: Optional[List[str]] = None
    hospital_affiliations: Optional[List[str]] = None


class LocationSearchRequest(BaseSchema):
    location: str  # City, state, or full address
    medical_condition: Optional[str] = None
    specialty: Optional[str] = None
    radius_km: int = 25
    search_type: str = "both"  # "hospitals", "doctors", or "both"


class MedicalFacilityRecommendations(BaseSchema):
    hospitals: List[HospitalInfo] = []
    doctors: List[DoctorInfo] = []
    emergency_facilities: List[HospitalInfo] = []
    urgent_care: List[HospitalInfo] = []
    specialist_recommendations: Dict[str, Dict[str, List[Any]]] = {}
    search_location: str
    search_timestamp: datetime
    error_message: Optional[str] = None


class LocationBasedAnalysisRequest(BaseSchema):
    consultation_id: UUID
    user_location: str
    include_facility_search: bool = True
    diagnosed_conditions: Optional[List[str]] = None
    risk_level: Optional[str] = None


class EnhancedAnalysisWithLocation(BaseSchema):
    consultation_id: UUID
    analysis: AnalysisResponse
    facility_recommendations: Optional[MedicalFacilityRecommendations] = None
    location_based_recommendations: List[Dict[str, Any]] = []
    emergency_instructions: Optional[Dict[str, Any]] = None