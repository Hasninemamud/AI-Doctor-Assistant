# Pydantic schemas for request/response validation

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
import enum

from app.models.models import (
    GenderEnum, ConsultationStatusEnum, ProcessingStatusEnum,
    RiskLevelEnum, SenderTypeEnum
)


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    name: str
    date_of_birth: Optional[datetime] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
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
    date_of_birth: Optional[datetime] = None
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None


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
    metadata: Optional[Dict[str, Any]] = None


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