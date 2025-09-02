# Database models for the AI Doctor Assistant

from sqlalchemy import Column, String, DateTime, Text, JSON, Enum, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ConsultationStatusEnum(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProcessingStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class RiskLevelEnum(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class SenderTypeEnum(str, enum.Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    consultations = relationship("Consultation", back_populates="user")
    medical_history = relationship("MedicalHistory", back_populates="user")


class MedicalHistory(Base):
    """Medical history for users"""
    __tablename__ = "medical_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Medical information
    allergies = Column(JSON, nullable=True)  # List of allergies
    medications = Column(JSON, nullable=True)  # Current medications
    conditions = Column(JSON, nullable=True)  # Chronic conditions
    surgeries = Column(JSON, nullable=True)  # Past surgeries
    family_history = Column(JSON, nullable=True)  # Family medical history
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="medical_history")


class Consultation(Base):
    """Consultation model for medical consultations"""
    __tablename__ = "consultations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Consultation data
    chief_complaint = Column(Text, nullable=True)
    symptoms = Column(JSON, nullable=True)  # Structured symptom data
    status = Column(Enum(ConsultationStatusEnum), default=ConsultationStatusEnum.DRAFT)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="consultations")
    test_reports = relationship("TestReport", back_populates="consultation")
    analyses = relationship("Analysis", back_populates="consultation")
    chat_messages = relationship("ChatMessage", back_populates="consultation")


class TestReport(Base):
    """Test report model for uploaded medical reports"""
    __tablename__ = "test_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id"), nullable=False)
    
    # File information
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Processing status
    processing_status = Column(Enum(ProcessingStatusEnum), default=ProcessingStatusEnum.PENDING)
    extracted_text = Column(Text, nullable=True)
    processed_data = Column(JSON, nullable=True)  # Structured medical data
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    consultation = relationship("Consultation", back_populates="test_reports")


class Analysis(Base):
    """Analysis model for AI-generated medical analysis"""
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id"), nullable=False)
    
    # Analysis data
    ai_analysis = Column(JSON, nullable=False)  # Complete AI analysis
    risk_level = Column(Enum(RiskLevelEnum), nullable=False)
    summary = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)  # Treatment recommendations
    emergency_actions = Column(JSON, nullable=True)  # Emergency protocols
    follow_up_suggestions = Column(JSON, nullable=True)  # Follow-up care
    
    # AI model information
    model_version = Column(String(50), nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    consultation = relationship("Consultation", back_populates="analyses")


class ChatMessage(Base):
    """Chat message model for real-time communication"""
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id = Column(UUID(as_uuid=True), ForeignKey("consultations.id"), nullable=False)
    
    # Message data
    sender_type = Column(Enum(SenderTypeEnum), nullable=False)
    message_content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)  # Additional message metadata
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    consultation = relationship("Consultation", back_populates="chat_messages")