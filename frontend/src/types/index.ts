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

export interface Recommendation {
  category: 'lifestyle' | 'medication' | 'follow_up' | 'immediate' | 'emergency' | 'urgent' | 'monitoring';
  action: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  timeline?: string;
}

export interface Analysis {
  id: string;
  consultation_id: string;
  ai_analysis: any;
  risk_level: 'low' | 'moderate' | 'high' | 'critical';
  summary?: string;
  recommendations?: (Recommendation | string)[];
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
  recommendations: (Recommendation | string)[];
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

// Enhanced types for specialized medical analysis
export interface SymptomTimelineEntry {
  id?: string;
  consultation_id?: string;
  symptom: string;
  severity?: number; // 1-10 scale
  location?: string;
  quality?: string;
  duration?: string;
  notes?: string;
  recorded_at: string;
  entered_at?: string;
}

export interface TimelinePattern {
  pattern_type: string;
  description: string;
  significance: string;
  start_time: string;
  end_time?: string;
  severity_trend?: 'improving' | 'worsening' | 'stable';
  confidence: number;
}

export interface ProgressionAnalysis {
  progression: 'worsening' | 'improving' | 'stable' | 'unknown';
  severity_range?: [number, number];
  symptom_count_trend: number;
  average_interval_hours: number;
  total_duration_hours: number;
}

export interface RiskTrajectory {
  current_risk: 'low' | 'moderate' | 'high' | 'critical';
  risk_trend: 'increasing' | 'stable' | 'decreasing';
  rapid_changes_count: number;
  average_recent_severity: number;
}

export interface EmergencyScreeningResult {
  is_emergency: boolean;
  emergency_level: 'none' | 'low' | 'moderate' | 'high' | 'critical';
  red_flags: string[];
  immediate_actions: string[];
  time_to_care: 'immediate' | 'within_1_hour' | 'within_4_hours' | 'within_24_hours';
  emergency_specialty?: string;
  confidence: number;
  reasoning: string;
}

export interface TimelineAnalysisResult {
  timeline_summary: string;
  identified_patterns: TimelinePattern[];
  progression_analysis: ProgressionAnalysis;
  risk_trajectory: RiskTrajectory;
  recommendations: Recommendation[];
  ai_insights: any;
}

export interface SpecializedAnalysis {
  id: string;
  consultation_id: string;
  analysis_type: 'general' | 'emergency_screening' | 'clinical_analysis' | 'timeline_analysis' | 'differential_diagnosis';
  medical_specialty?: string;
  model_used?: string;
  analysis_results: any;
  summary?: string;
  confidence_score?: number;
  is_emergency?: boolean;
  emergency_level?: string;
  red_flags?: string[];
  identified_patterns?: any[];
  progression_analysis?: any;
  risk_trajectory?: any;
  created_at: string;
}

export interface EnhancedAnalysisRequest {
  consultation_id: string;
  analysis_types: string[];
  include_emergency_screening: boolean;
  include_timeline_analysis: boolean;
  include_test_reports: boolean;
  include_symptoms: boolean;
  include_medical_history: boolean;
}

export interface ComprehensiveAnalysisResponse {
  consultation_id: string;
  general_analysis?: AnalysisResponse;
  emergency_screening?: EmergencyScreeningResult;
  timeline_analysis?: TimelineAnalysisResult;
  specialized_analyses: SpecializedAnalysis[];
  overall_risk_level: 'low' | 'moderate' | 'high' | 'critical';
  priority_recommendations: Recommendation[];
  analysis_timestamp: string;
}

// Location-based medical facility types
export interface HospitalInfo {
  name: string;
  address: string;
  phone: string;
  type: string;
  specialty?: string;
  rating?: number;
  distance_km?: number;
  emergency_services: boolean;
  accepts_insurance: boolean;
  website?: string;
  directions_url?: string;
  description?: string;
  wait_time_minutes?: number;
  trauma_level?: string;
  open_24_7?: boolean;
}

export interface DoctorInfo {
  name: string;
  specialty: string;
  practice_name?: string;
  address: string;
  phone: string;
  rating?: number;
  years_experience?: number;
  education?: string;
  accepts_new_patients: boolean;
  accepts_insurance: boolean;
  distance_km?: number;
  next_available?: string;
  website?: string;
  directions_url?: string;
  languages?: string[];
  hospital_affiliations?: string[];
}

export interface LocationSearchRequest {
  location: string;
  medical_condition?: string;
  specialty?: string;
  radius_km: number;
  search_type: 'hospitals' | 'doctors' | 'both';
}

export interface MedicalFacilityRecommendations {
  hospitals: HospitalInfo[];
  doctors: DoctorInfo[];
  emergency_facilities: HospitalInfo[];
  urgent_care: HospitalInfo[];
  specialist_recommendations: Record<string, any>;
  search_location: string;
  search_timestamp: string;
  error_message?: string;
}

export interface LocationBasedAnalysisRequest {
  consultation_id: string;
  user_location: string;
  include_facility_search: boolean;
  diagnosed_conditions?: string[];
  risk_level?: string;
}

export interface EnhancedAnalysisWithLocation {
  consultation_id: string;
  analysis: AnalysisResponse;
  facility_recommendations?: MedicalFacilityRecommendations;
  location_based_recommendations: any[];
  emergency_instructions?: any;
}