// Type definitions for the AI Doctor Assistant

export interface User {
  id: string;
  email: string;
  name: string;
  date_of_birth?: string;
  gender?: 'male' | 'female' | 'other';
  phone?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  date_of_birth?: string;
  gender?: 'male' | 'female' | 'other';
  phone?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Consultation {
  id: string;
  user_id: string;
  chief_complaint?: string;
  symptoms?: any;
  status: 'draft' | 'active' | 'completed' | 'cancelled';
  created_at: string;
  updated_at?: string;
}

export interface SymptomData {
  location?: string;
  severity?: number; // 1-10 scale
  duration?: string;
  onset?: string;
  quality?: string;
  associated_symptoms?: string[];
  aggravating_factors?: string[];
  relieving_factors?: string[];
}

export interface TestReport {
  id: string;
  consultation_id: string;
  file_name: string;
  file_path: string;
  file_type: string;
  file_size: number;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  processed_data?: any;
  uploaded_at: string;
  processed_at?: string;
}

export interface Analysis {
  id: string;
  consultation_id: string;
  ai_analysis: any;
  risk_level: 'low' | 'moderate' | 'high' | 'critical';
  summary?: string;
  recommendations?: any[];
  emergency_actions?: any[];
  follow_up_suggestions?: string[];
  model_version?: string;
  confidence_score?: number;
  created_at: string;
}

export interface EmergencyAlert {
  is_emergency: boolean;
  severity_level: 'low' | 'moderate' | 'high' | 'critical';
  immediate_actions: string[];
  emergency_contacts: string[];
  message: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  consultation_id: string;
  summary: string;
  risk_level: 'low' | 'moderate' | 'high' | 'critical';
  key_findings: string[];
  recommendations: any[];
  emergency_alert?: EmergencyAlert;
  follow_up_suggestions: string[];
  confidence_score: number;
  disclaimer: string;
}

export interface ApiError {
  error: string;
  message: string;
  details?: any;
}

export interface MedicalHistory {
  id: string;
  user_id: string;
  allergies?: string[];
  medications?: any[];
  conditions?: string[];
  surgeries?: any[];
  family_history?: string[];
  created_at: string;
  updated_at?: string;
}