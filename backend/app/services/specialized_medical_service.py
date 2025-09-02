# Specialized Medical Models Service for Enhanced AI Analysis

import json
import httpx
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import re
from dataclasses import dataclass

from app.core.config import settings
from app.schemas.schemas import RiskLevelEnum


class MedicalSpecialty(str, Enum):
    """Medical specialties for specialized analysis"""
    GENERAL = "general"
    EMERGENCY = "emergency"
    CARDIOLOGY = "cardiology"
    NEUROLOGY = "neurology"
    GASTROENTEROLOGY = "gastroenterology"
    RESPIRATORY = "respiratory"
    DERMATOLOGY = "dermatology"
    PSYCHIATRY = "psychiatry"
    ORTHOPEDICS = "orthopedics"
    INFECTIOUS_DISEASE = "infectious_disease"


class AnalysisType(str, Enum):
    """Types of specialized analysis"""
    EMERGENCY_SCREENING = "emergency_screening"
    CLINICAL_ANALYSIS = "clinical_analysis"
    TIMELINE_ANALYSIS = "timeline_analysis"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    SYMPTOM_PATTERN = "symptom_pattern"
    RISK_STRATIFICATION = "risk_stratification"


@dataclass
class SymptomTimelineEntry:
    """Single symptom timeline entry"""
    timestamp: datetime
    symptom: str
    severity: Optional[int] = None
    location: Optional[str] = None
    quality: Optional[str] = None
    duration: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class TimelinePattern:
    """Identified pattern in symptom timeline"""
    pattern_type: str
    description: str
    significance: str
    start_time: datetime
    end_time: Optional[datetime] = None
    severity_trend: Optional[str] = None  # improving, worsening, stable
    confidence: float = 0.0


class SpecializedMedicalService:
    """Service for specialized medical AI analysis"""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        
        # Specialized models for different medical tasks
        self.models = {
            AnalysisType.EMERGENCY_SCREENING: {
                "primary": "microsoft/wizardlm-2-8x22b:free",
                "backup": ["meta-llama/llama-3.1-8b-instruct:free", "google/gemma-2-9b-it:free"]
            },
            AnalysisType.CLINICAL_ANALYSIS: {
                "primary": "openai/gpt-oss-120b:free",
                "backup": ["microsoft/wizardlm-2-8x22b:free", "meta-llama/llama-3.1-8b-instruct:free"]
            },
            AnalysisType.TIMELINE_ANALYSIS: {
                "primary": "meta-llama/llama-3.1-8b-instruct:free",
                "backup": ["google/gemma-2-9b-it:free", "microsoft/wizardlm-2-8x22b:free"]
            },
            AnalysisType.DIFFERENTIAL_DIAGNOSIS: {
                "primary": "openai/gpt-oss-120b:free",
                "backup": ["microsoft/wizardlm-2-8x22b:free", "meta-llama/llama-3.1-8b-instruct:free"]
            }
        }
    
    async def emergency_screening_analysis(
        self,
        symptoms: Dict[str, Any],
        chief_complaint: Optional[str] = None,
        timeline: Optional[List[SymptomTimelineEntry]] = None
    ) -> Dict[str, Any]:
        """
        Rapid emergency screening using specialized emergency detection model
        
        Args:
            symptoms: Current symptoms
            chief_complaint: Primary complaint
            timeline: Symptom timeline if available
            
        Returns:
            Dict containing emergency screening results
        """
        context = self._prepare_emergency_context(symptoms, chief_complaint, timeline)
        prompt = self._create_emergency_screening_prompt(context)
        
        try:
            response = await self._call_specialized_model(
                AnalysisType.EMERGENCY_SCREENING,
                prompt,
                max_tokens=1000,
                temperature=0.1  # Very conservative for emergency detection
            )
            
            return self._parse_emergency_response(response)
            
        except Exception as e:
            return self._create_fallback_emergency_analysis(str(e), symptoms)
    
    async def clinical_differential_analysis(
        self,
        symptoms: Dict[str, Any],
        test_results: Optional[str] = None,
        medical_history: Optional[Dict[str, Any]] = None,
        timeline: Optional[List[SymptomTimelineEntry]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive clinical analysis with differential diagnosis
        
        Args:
            symptoms: Patient symptoms
            test_results: Laboratory/imaging results
            medical_history: Patient medical history
            timeline: Symptom progression timeline
            
        Returns:
            Dict containing differential diagnosis and clinical analysis
        """
        context = self._prepare_clinical_context(symptoms, test_results, medical_history, timeline)
        prompt = self._create_clinical_analysis_prompt(context)
        
        try:
            response = await self._call_specialized_model(
                AnalysisType.CLINICAL_ANALYSIS,
                prompt,
                max_tokens=2500,
                temperature=0.2
            )
            
            return self._parse_clinical_response(response)
            
        except Exception as e:
            return self._create_fallback_clinical_analysis(str(e), symptoms)
    
    async def symptom_timeline_analysis(
        self,
        timeline: List[SymptomTimelineEntry],
        current_symptoms: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze symptom timeline for patterns and progression
        
        Args:
            timeline: Chronological symptom data
            current_symptoms: Current symptom state
            
        Returns:
            Dict containing timeline analysis results
        """
        if not timeline:
            return self._create_empty_timeline_analysis()
        
        # Sort timeline by timestamp
        sorted_timeline = sorted(timeline, key=lambda x: x.timestamp)
        
        # Extract patterns
        patterns = self._analyze_timeline_patterns(sorted_timeline)
        
        # Create context for AI analysis
        context = self._prepare_timeline_context(sorted_timeline, current_symptoms)
        prompt = self._create_timeline_analysis_prompt(context, patterns)
        
        try:
            response = await self._call_specialized_model(
                AnalysisType.TIMELINE_ANALYSIS,
                prompt,
                max_tokens=2000,
                temperature=0.3
            )
            
            ai_analysis = self._parse_timeline_response(response)
            
            # Combine rule-based patterns with AI analysis
            return {
                "timeline_summary": ai_analysis.get("summary", "Timeline analysis completed"),
                "identified_patterns": patterns,
                "ai_insights": ai_analysis,
                "progression_analysis": self._analyze_symptom_progression(sorted_timeline),
                "risk_trajectory": self._calculate_risk_trajectory(sorted_timeline),
                "recommendations": ai_analysis.get("recommendations", [])
            }
            
        except Exception as e:
            return self._create_fallback_timeline_analysis(str(e), sorted_timeline, patterns)
    
    def _prepare_emergency_context(
        self,
        symptoms: Dict[str, Any],
        chief_complaint: Optional[str],
        timeline: Optional[List[SymptomTimelineEntry]]
    ) -> str:
        """Prepare context for emergency screening"""
        context_parts = []
        
        if chief_complaint:
            context_parts.append(f"CHIEF COMPLAINT: {chief_complaint}")
        
        # Emergency-relevant symptoms
        context_parts.append("CURRENT SYMPTOMS:")
        if isinstance(symptoms, dict) and "symptoms" in symptoms:
            for symptom in symptoms["symptoms"]:
                if isinstance(symptom, dict):
                    severity = symptom.get("severity", 0)
                    location = symptom.get("location", "")
                    quality = symptom.get("quality", "")
                    context_parts.append(f"- {location}: {quality}, severity {severity}/10")
        
        # Recent timeline changes for emergency detection
        if timeline:
            recent_changes = [t for t in timeline if (datetime.utcnow() - t.timestamp).total_seconds() < 86400]  # Last 24 hours
            if recent_changes:
                context_parts.append("RECENT CHANGES (Last 24 hours):")
                for change in recent_changes[-5:]:  # Last 5 changes
                    context_parts.append(f"- {change.timestamp.strftime('%H:%M')}: {change.symptom}")
        
        return "\n".join(context_parts)
    
    def _create_emergency_screening_prompt(self, context: str) -> str:
        """Create emergency screening prompt"""
        return f"""You are an emergency medicine AI specialist. Perform rapid emergency screening based on the following patient information:

{context}

EMERGENCY SCREENING CHECKLIST:
Evaluate for these critical conditions:
- Acute coronary syndrome (chest pain, dyspnea, diaphoresis)
- Stroke (FAST criteria: Face, Arms, Speech, Time)
- Respiratory distress (severe dyspnea, oxygen saturation issues)
- Shock (hypotension, altered mental status, poor perfusion)
- Severe bleeding or trauma
- Sepsis or severe infection
- Acute abdomen (severe abdominal pain with guarding)
- Severe allergic reaction (anaphylaxis)
- Acute psychotic episode or suicidal ideation

Respond with JSON format:
{{
    "is_emergency": true/false,
    "emergency_level": "none|low|moderate|high|critical",
    "red_flags": ["specific emergency indicators found"],
    "immediate_actions": ["urgent actions if emergency"],
    "time_to_care": "immediate|within_1_hour|within_4_hours|within_24_hours",
    "emergency_specialty": "emergency|cardiology|neurology|surgery|psychiatry",
    "confidence": 95,
    "reasoning": "brief explanation of emergency assessment"
}}

Focus on sensitivity over specificity - err on side of caution for emergency detection."""
    
    def _parse_emergency_response(self, response: str) -> Dict[str, Any]:
        """Parse emergency screening response"""
        try:
            # Clean JSON response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            analysis = json.loads(response)
            
            return {
                "is_emergency": analysis.get("is_emergency", False),
                "emergency_level": analysis.get("emergency_level", "none"),
                "red_flags": analysis.get("red_flags", []),
                "immediate_actions": analysis.get("immediate_actions", []),
                "time_to_care": analysis.get("time_to_care", "within_24_hours"),
                "emergency_specialty": analysis.get("emergency_specialty", "emergency"),
                "confidence": analysis.get("confidence", 50),
                "reasoning": analysis.get("reasoning", "Emergency screening completed"),
                "analysis_type": "emergency_screening"
            }
            
        except json.JSONDecodeError:
            return self._create_fallback_emergency_analysis("JSON parsing error", {})
    
    def _analyze_timeline_patterns(self, timeline: List[SymptomTimelineEntry]) -> List[TimelinePattern]:
        """Analyze timeline for patterns using rule-based approach"""
        patterns = []
        
        if len(timeline) < 2:
            return patterns
        
        # Pattern 1: Rapid onset (symptoms appearing within 1 hour)
        rapid_onset_symptoms = []
        for i in range(1, len(timeline)):
            time_diff = (timeline[i].timestamp - timeline[i-1].timestamp).total_seconds() / 3600
            if time_diff <= 1:
                rapid_onset_symptoms.append((timeline[i-1], timeline[i]))
        
        if rapid_onset_symptoms:
            patterns.append(TimelinePattern(
                pattern_type="rapid_onset",
                description="Multiple symptoms appeared within 1 hour",
                significance="May indicate acute medical condition requiring urgent evaluation",
                start_time=rapid_onset_symptoms[0][0].timestamp,
                end_time=rapid_onset_symptoms[-1][1].timestamp,
                confidence=0.8
            ))
        
        # Pattern 2: Progressive worsening
        severity_timeline = [(t.timestamp, t.severity) for t in timeline if t.severity is not None]
        if len(severity_timeline) >= 3:
            # Check for consistently increasing severity
            increasing_count = 0
            for i in range(1, len(severity_timeline)):
                if severity_timeline[i][1] > severity_timeline[i-1][1]:
                    increasing_count += 1
            
            if increasing_count >= len(severity_timeline) * 0.7:  # 70% increasing
                patterns.append(TimelinePattern(
                    pattern_type="progressive_worsening",
                    description="Symptoms progressively worsening over time",
                    significance="Indicates condition may be deteriorating, requires medical attention",
                    start_time=severity_timeline[0][0],
                    end_time=severity_timeline[-1][0],
                    severity_trend="worsening",
                    confidence=0.9
                ))
        
        # Pattern 3: Cyclical pattern
        symptom_counts = {}
        for entry in timeline:
            symptom_counts[entry.symptom] = symptom_counts.get(entry.symptom, 0) + 1
        
        recurring_symptoms = [s for s, count in symptom_counts.items() if count >= 3]
        if recurring_symptoms:
            patterns.append(TimelinePattern(
                pattern_type="cyclical_pattern",
                description=f"Recurring symptoms: {', '.join(recurring_symptoms)}",
                significance="May indicate chronic condition with flare-ups",
                start_time=timeline[0].timestamp,
                end_time=timeline[-1].timestamp,
                confidence=0.7
            ))
        
        return patterns
    
    def _prepare_timeline_context(
        self,
        timeline: List[SymptomTimelineEntry],
        current_symptoms: Optional[Dict[str, Any]]
    ) -> str:
        """Prepare context for timeline analysis"""
        context_parts = []
        
        context_parts.append("SYMPTOM TIMELINE:")
        for entry in timeline:
            time_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
            severity_str = f" (severity: {entry.severity}/10)" if entry.severity else ""
            location_str = f" at {entry.location}" if entry.location else ""
            context_parts.append(f"- {time_str}: {entry.symptom}{location_str}{severity_str}")
        
        if current_symptoms:
            context_parts.append("\nCURRENT SYMPTOM STATE:")
            context_parts.append(str(current_symptoms))
        
        # Calculate timeline duration
        if len(timeline) > 1:
            duration = timeline[-1].timestamp - timeline[0].timestamp
            context_parts.append(f"\nTIMELINE DURATION: {duration}")
        
        return "\n".join(context_parts)
    
    def _create_timeline_analysis_prompt(self, context: str, patterns: List[TimelinePattern]) -> str:
        """Create timeline analysis prompt"""
        pattern_summary = "\n".join([f"- {p.pattern_type}: {p.description}" for p in patterns])
        
        return f"""You are a medical AI specialist analyzing symptom timeline patterns. Analyze the progression and identify clinically significant patterns:

{context}

IDENTIFIED PATTERNS:
{pattern_summary}

Provide comprehensive timeline analysis in JSON format:
{{
    "summary": "Overall timeline assessment",
    "clinical_significance": "What this timeline pattern suggests",
    "progression_type": "acute|subacute|chronic|intermittent",
    "concerning_trends": ["specific worrying patterns"],
    "timeline_insights": [
        {{
            "insight": "specific observation",
            "clinical_relevance": "why this matters medically",
            "urgency": "low|moderate|high"
        }}
    ],
    "recommendations": [
        {{
            "action": "specific recommendation",
            "timing": "when to act",
            "reasoning": "why this is recommended"
        }}
    ],
    "differential_considerations": ["conditions suggested by timeline"],
    "red_flags": ["timeline patterns requiring urgent attention"],
    "confidence": 85
}}

Focus on:
1. Symptom progression patterns
2. Time relationships between symptoms
3. Severity trends over time
4. Clinical significance of timing
5. Urgency of medical evaluation needed"""
    
    async def _call_specialized_model(
        self,
        analysis_type: AnalysisType,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.3
    ) -> str:
        """Call specialized model for specific analysis type"""
        model_config = self.models.get(analysis_type, self.models[AnalysisType.CLINICAL_ANALYSIS])
        
        # Try primary model first
        try:
            return await self._make_api_call(model_config["primary"], prompt, max_tokens, temperature)
        except Exception:
            # Try backup models
            for backup_model in model_config["backup"]:
                try:
                    return await self._make_api_call(backup_model, prompt, max_tokens, temperature)
                except Exception:
                    continue
            
            raise Exception("All specialized models failed")
    
    async def _make_api_call(
        self,
        model: str,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Make API call to specific model"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "AI Doctor Assistant - Specialized Analysis"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a specialized medical AI assistant. Provide accurate, evidence-based analysis while emphasizing the need for professional medical consultation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            result = response.json()
            if "choices" not in result or not result["choices"]:
                raise Exception("No response choices returned")
                
            return result["choices"][0]["message"]["content"].strip()
    
    def _analyze_symptom_progression(self, timeline: List[SymptomTimelineEntry]) -> Dict[str, Any]:
        """Analyze symptom progression patterns"""
        if len(timeline) < 2:
            return {"progression": "insufficient_data"}
        
        # Analyze severity progression
        severities = [entry.severity for entry in timeline if entry.severity is not None]
        if len(severities) >= 2:
            if severities[-1] > severities[0]:
                trend = "worsening"
            elif severities[-1] < severities[0]:
                trend = "improving"
            else:
                trend = "stable"
        else:
            trend = "unknown"
        
        # Analyze symptom count progression
        symptom_sets = []
        for entry in timeline:
            symptoms_at_time = set([entry.symptom])
            symptom_sets.append(symptoms_at_time)
        
        # Calculate time intervals
        intervals = []
        for i in range(1, len(timeline)):
            interval = (timeline[i].timestamp - timeline[i-1].timestamp).total_seconds() / 3600
            intervals.append(interval)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 0
        
        return {
            "progression": trend,
            "severity_range": [min(severities), max(severities)] if severities else None,
            "symptom_count_trend": len(symptom_sets[-1]) - len(symptom_sets[0]) if len(symptom_sets) >= 2 else 0,
            "average_interval_hours": avg_interval,
            "total_duration_hours": (timeline[-1].timestamp - timeline[0].timestamp).total_seconds() / 3600
        }
    
    def _calculate_risk_trajectory(self, timeline: List[SymptomTimelineEntry]) -> Dict[str, Any]:
        """Calculate risk trajectory based on timeline"""
        if not timeline:
            return {"risk_trend": "unknown", "current_risk": "moderate"}
        
        # Simple risk calculation based on severity and progression
        recent_entries = timeline[-3:] if len(timeline) >= 3 else timeline
        avg_recent_severity = sum(e.severity for e in recent_entries if e.severity) / len([e for e in recent_entries if e.severity]) if any(e.severity for e in recent_entries) else 5
        
        # Check for rapid changes
        rapid_changes = len([i for i in range(1, len(timeline)) if (timeline[i].timestamp - timeline[i-1].timestamp).total_seconds() < 3600])
        
        if avg_recent_severity >= 8 or rapid_changes >= 3:
            risk_level = "high"
        elif avg_recent_severity >= 6 or rapid_changes >= 2:
            risk_level = "moderate"
        else:
            risk_level = "low"
        
        return {
            "current_risk": risk_level,
            "risk_trend": "increasing" if rapid_changes >= 2 else "stable",
            "rapid_changes_count": rapid_changes,
            "average_recent_severity": avg_recent_severity
        }
    
    def _create_fallback_emergency_analysis(self, error: str, symptoms: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback emergency analysis"""
        return {
            "is_emergency": False,
            "emergency_level": "unknown",
            "red_flags": ["Emergency screening unavailable - seek medical evaluation"],
            "immediate_actions": ["Consult healthcare provider for proper evaluation"],
            "time_to_care": "within_24_hours",
            "confidence": 25,
            "reasoning": f"Emergency screening failed: {error}. Default to cautious approach.",
            "analysis_type": "emergency_screening_fallback"
        }
    
    def _create_fallback_timeline_analysis(
        self,
        error: str,
        timeline: List[SymptomTimelineEntry],
        patterns: List[TimelinePattern]
    ) -> Dict[str, Any]:
        """Create fallback timeline analysis"""
        return {
            "timeline_summary": f"Timeline analysis partially completed. {len(timeline)} entries analyzed.",
            "identified_patterns": patterns,
            "ai_insights": {"error": error, "fallback": True},
            "progression_analysis": self._analyze_symptom_progression(timeline),
            "risk_trajectory": self._calculate_risk_trajectory(timeline),
            "recommendations": [
                {
                    "action": "Review timeline with healthcare provider",
                    "timing": "At next appointment",
                    "reasoning": "Professional review needed for timeline interpretation"
                }
            ]
        }
    
    def _create_empty_timeline_analysis(self) -> Dict[str, Any]:
        """Create empty timeline analysis when no data available"""
        return {
            "timeline_summary": "No timeline data available for analysis",
            "identified_patterns": [],
            "ai_insights": {"message": "Insufficient timeline data"},
            "progression_analysis": {"progression": "no_data"},
            "risk_trajectory": {"risk_trend": "unknown", "current_risk": "moderate"},
            "recommendations": [
                {
                    "action": "Begin symptom tracking for future analysis",
                    "timing": "Ongoing",
                    "reasoning": "Timeline tracking improves clinical assessment"
                }
            ]
        }


# Global instance
specialized_medical_service = SpecializedMedicalService()