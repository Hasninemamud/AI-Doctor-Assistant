# AI Analysis Service for medical consultation

import json
import openai
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.core.config import settings
from app.schemas.schemas import (
    RiskLevelEnum, AnalysisResponse, EmergencyAlert,
    SymptomData, SymptomSubmission
)

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY


class AIAnalysisService:
    """Service for AI-powered medical analysis"""
    
    def __init__(self):
        self.model = "gpt-4"  # Use GPT-4 for better medical reasoning
        self.max_tokens = 2000
        self.temperature = 0.3  # Lower temperature for more consistent medical advice
    
    async def analyze_consultation(
        self,
        symptoms: Optional[Dict[str, Any]] = None,
        test_report_text: Optional[str] = None,
        medical_history: Optional[Dict[str, Any]] = None,
        chief_complaint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze medical consultation data using AI
        
        Args:
            symptoms: Patient symptoms data
            test_report_text: Extracted text from test reports
            medical_history: Patient medical history
            chief_complaint: Chief complaint description
            
        Returns:
            Dict[str, Any]: AI analysis results
        """
        # Prepare context for AI analysis
        context = self._prepare_medical_context(
            symptoms, test_report_text, medical_history, chief_complaint
        )
        
        # Create AI prompt
        prompt = self._create_analysis_prompt(context)
        
        try:
            # Call OpenAI API
            response = await self._call_openai_api(prompt)
            
            # Parse and structure the response
            analysis_result = self._parse_ai_response(response)
            
            return analysis_result
            
        except Exception as e:
            # Return error response
            return {
                "error": True,
                "message": f"AI analysis failed: {str(e)}",
                "risk_level": "unknown",
                "recommendations": [],
                "emergency_alert": None
            }
    
    def _prepare_medical_context(
        self,
        symptoms: Optional[Dict[str, Any]],
        test_report_text: Optional[str],
        medical_history: Optional[Dict[str, Any]],
        chief_complaint: Optional[str]
    ) -> str:
        """
        Prepare medical context for AI analysis
        
        Args:
            symptoms: Patient symptoms
            test_report_text: Test report text
            medical_history: Medical history
            chief_complaint: Chief complaint
            
        Returns:
            str: Formatted medical context
        """
        context_parts = []
        
        if chief_complaint:
            context_parts.append(f"CHIEF COMPLAINT:\n{chief_complaint}\n")
        
        if symptoms:
            context_parts.append("SYMPTOMS:")
            if isinstance(symptoms, list):
                for symptom in symptoms:
                    if isinstance(symptom, dict):
                        symptom_desc = f"- Location: {symptom.get('location', 'Not specified')}"
                        symptom_desc += f", Severity: {symptom.get('severity', 'Not specified')}/10"
                        symptom_desc += f", Duration: {symptom.get('duration', 'Not specified')}"
                        context_parts.append(symptom_desc)
            else:
                context_parts.append(f"{symptoms}")
            context_parts.append("")
        
        if test_report_text:
            context_parts.append(f"TEST RESULTS:\n{test_report_text}\n")
        
        if medical_history:
            context_parts.append("MEDICAL HISTORY:")
            if medical_history.get('allergies'):
                context_parts.append(f"- Allergies: {', '.join(medical_history['allergies'])}")
            if medical_history.get('medications'):
                context_parts.append(f"- Current medications: {medical_history['medications']}")
            if medical_history.get('conditions'):
                context_parts.append(f"- Chronic conditions: {', '.join(medical_history['conditions'])}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def _create_analysis_prompt(self, context: str) -> str:
        """
        Create AI analysis prompt
        
        Args:
            context: Medical context
            
        Returns:
            str: AI prompt
        """
        prompt = f"""You are an AI medical assistant analyzing a patient consultation. Please provide a comprehensive analysis based on the following information:

{context}

Please provide your analysis in the following JSON format:

{{
    "summary": "Brief summary of the medical situation",
    "risk_level": "low|moderate|high|critical",
    "key_findings": ["finding1", "finding2", "finding3"],
    "possible_conditions": [
        {{
            "condition": "condition name",
            "probability": "low|moderate|high",
            "reasoning": "explanation for this possibility"
        }}
    ],
    "recommendations": [
        {{
            "category": "immediate|follow_up|lifestyle|medication",
            "action": "specific recommendation",
            "priority": "high|medium|low",
            "timeline": "when to act"
        }}
    ],
    "emergency_indicators": [
        "indicator1", "indicator2"
    ],
    "is_emergency": false,
    "emergency_actions": [
        "action if emergency"
    ],
    "follow_up_suggestions": [
        "suggestion1", "suggestion2"
    ],
    "confidence_score": 85,
    "disclaimer": "Important medical disclaimer"
}}

IMPORTANT GUIDELINES:
1. Always err on the side of caution
2. Recommend professional medical consultation for serious symptoms
3. Never provide definitive diagnoses - only suggest possibilities
4. Include emergency indicators clearly
5. Provide actionable recommendations
6. Include appropriate medical disclaimers
7. Consider all provided information comprehensively

Please analyze the patient information and respond with valid JSON only."""

        return prompt
    
    async def _call_openai_api(self, prompt: str) -> str:
        """
        Call OpenAI API for medical analysis
        
        Args:
            prompt: Analysis prompt
            
        Returns:
            str: AI response
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable medical AI assistant that provides thorough analysis while always emphasizing the need for professional medical consultation. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse AI response into structured format
        
        Args:
            response: Raw AI response
            
        Returns:
            Dict[str, Any]: Parsed analysis result
        """
        try:
            # Clean the response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            # Parse JSON
            analysis = json.loads(response)
            
            # Validate and structure the response
            structured_result = {
                "analysis_id": None,  # Will be set when saving to database
                "summary": analysis.get("summary", "Analysis completed"),
                "risk_level": self._validate_risk_level(analysis.get("risk_level", "moderate")),
                "key_findings": analysis.get("key_findings", []),
                "possible_conditions": analysis.get("possible_conditions", []),
                "recommendations": analysis.get("recommendations", []),
                "emergency_alert": None,
                "follow_up_suggestions": analysis.get("follow_up_suggestions", []),
                "confidence_score": min(100, max(0, analysis.get("confidence_score", 75))),
                "disclaimer": analysis.get("disclaimer", self._get_default_disclaimer()),
                "ai_analysis": analysis,  # Store complete AI response
                "created_at": datetime.utcnow()
            }
            
            # Handle emergency situation
            if analysis.get("is_emergency", False):
                structured_result["emergency_alert"] = {
                    "is_emergency": True,
                    "severity_level": structured_result["risk_level"],
                    "immediate_actions": analysis.get("emergency_actions", []),
                    "emergency_contacts": ["911", "Local Emergency Services"],
                    "message": "This appears to be a medical emergency. Seek immediate medical attention."
                }
            
            return structured_result
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "summary": "Analysis completed with limited parsing",
                "risk_level": "moderate",
                "key_findings": ["Unable to parse detailed analysis"],
                "recommendations": [
                    {
                        "category": "follow_up",
                        "action": "Consult with a healthcare professional",
                        "priority": "high",
                        "timeline": "Within 24 hours"
                    }
                ],
                "confidence_score": 50,
                "disclaimer": self._get_default_disclaimer(),
                "ai_analysis": {"raw_response": response},
                "created_at": datetime.utcnow()
            }
    
    def _validate_risk_level(self, risk_level: str) -> str:
        """
        Validate and return appropriate risk level
        
        Args:
            risk_level: Risk level from AI
            
        Returns:
            str: Validated risk level
        """
        valid_levels = ["low", "moderate", "high", "critical"]
        if risk_level.lower() in valid_levels:
            return risk_level.lower()
        return "moderate"  # Default fallback
    
    def _get_default_disclaimer(self) -> str:
        """
        Get default medical disclaimer
        
        Returns:
            str: Medical disclaimer
        """
        return (
            "This AI analysis is for informational purposes only and should not replace "
            "professional medical advice, diagnosis, or treatment. Always consult with a "
            "qualified healthcare provider for medical concerns. In case of emergency, "
            "call emergency services immediately."
        )


# Global instance
ai_analysis_service = AIAnalysisService()