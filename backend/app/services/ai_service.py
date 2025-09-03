# AI Analysis Service for medical consultation

import json
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.core.config import settings
from app.schemas.schemas import (
    RiskLevelEnum, AnalysisResponse, EmergencyAlert,
    SymptomData, SymptomSubmission
)


class AIAnalysisService:
    """Service for AI-powered medical analysis"""
    
    def __init__(self):
        self.model = settings.OPENROUTER_MODEL  # Use OpenRouter model
        self.max_tokens = 2000
        self.temperature = 0.3  # Lower temperature for more consistent medical advice
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        
        # Validate API key
        if not self.api_key or self.api_key == "" or self.api_key == "your-openrouter-api-key-here":
            self.api_key = None
    
    async def analyze_consultation(
        self,
        symptoms: Optional[Dict[str, Any]] = None,
        test_report_text: Optional[str] = None,
        medical_history: Optional[Dict[str, Any]] = None,
        chief_complaint: Optional[str] = None,
        user_location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze medical consultation data using AI
        
        Args:
            symptoms: Patient symptoms data
            test_report_text: Extracted text from test reports
            medical_history: Patient medical history
            chief_complaint: Chief complaint description
            user_location: User's location for facility recommendations
            
        Returns:
            Dict[str, Any]: AI analysis results
        """
        # Check if API key is configured
        if not self.api_key:
            return self._create_fallback_analysis(
                "OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your .env file.",
                symptoms, test_report_text, medical_history, chief_complaint, user_location
            )
        
        # Prepare context for AI analysis
        context = self._prepare_medical_context(
            symptoms, test_report_text, medical_history, chief_complaint
        )
        
        # Create AI prompt with location awareness
        prompt = self._create_analysis_prompt(context, user_location)
        
        try:
            # Call OpenRouter API
            response = await self._call_openrouter_api(prompt)
            
            # Parse and structure the response
            analysis_result = self._parse_ai_response(response)
            
            # Add location-based recommendations if location provided
            if user_location and analysis_result.get("possible_conditions"):
                analysis_result = await self._add_location_recommendations(
                    analysis_result, user_location
                )
            
            return analysis_result
            
        except Exception as e:
            # Return fallback analysis with error details
            return self._create_fallback_analysis(
                f"AI analysis failed: {str(e)}",
                symptoms, test_report_text, medical_history, chief_complaint, user_location
            )
    
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
    
    def _create_analysis_prompt(self, context: str, user_location: Optional[str] = None) -> str:
        """
        Create AI analysis prompt
        
        Args:
            context: Medical context
            user_location: User's location for location-aware recommendations
            
        Returns:
            str: AI prompt
        """
        location_context = ""
        if user_location:
            location_context = f"\nPATIENT LOCATION: {user_location}\nPlease consider the patient's location when making recommendations for follow-up care and specialist referrals.\n"
        
        prompt = f"""You are an AI medical assistant analyzing a patient consultation. Please provide a comprehensive analysis based on the following information:

{context}{location_context}

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
    
    async def _call_openrouter_api(self, prompt: str) -> str:
        """
        Call OpenRouter API for medical analysis
        
        Args:
            prompt: Analysis prompt
            
        Returns:
            str: AI response
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "AI Doctor Assistant"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a knowledgeable medical AI assistant that provides thorough analysis while always emphasizing the need for professional medical consultation. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                
                # Handle specific OpenRouter errors
                if response.status_code == 404:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                    if "data policy" in str(error_data).lower() or "free model publication" in str(error_data).lower():
                        # Try alternative free model
                        return await self._try_alternative_model(prompt, headers)
                    else:
                        raise Exception(f"Model not found: {response.text}")
                
                if response.status_code != 200:
                    raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
                
                result = response.json()
                if "choices" not in result or not result["choices"]:
                    raise Exception("No response choices returned from API")
                    
                return result["choices"][0]["message"]["content"].strip()
                
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    async def _try_alternative_model(self, prompt: str, headers: dict) -> str:
        """
        Try alternative free models when the primary model fails
        
        Args:
            prompt: Analysis prompt
            headers: Request headers
            
        Returns:
            str: AI response
        """
        # List of alternative free models to try
        alternative_models = [
            "microsoft/wizardlm-2-8x22b:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "google/gemma-2-9b-it:free",
            "huggingfaceh4/zephyr-7b-beta:free",
            "openchat/openchat-7b:free"
        ]
        
        for model in alternative_models:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a medical AI assistant. Provide analysis in JSON format with medical recommendations while emphasizing professional consultation."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": self.max_tokens,
                    "temperature": self.temperature
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if "choices" in result and result["choices"]:
                            return result["choices"][0]["message"]["content"].strip()
                    
            except Exception:
                continue  # Try next model
        
        # If all models fail, raise an exception
        raise Exception("All free models are currently unavailable. Please try again later or configure a paid model.")
    
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
    
    def _create_fallback_analysis(
        self, 
        error_message: str,
        symptoms: Optional[Dict[str, Any]] = None,
        test_report_text: Optional[str] = None,
        medical_history: Optional[Dict[str, Any]] = None,
        chief_complaint: Optional[str] = None,
        user_location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a comprehensive fallback analysis when AI service is unavailable
        
        Args:
            error_message: Error that occurred
            symptoms: Patient symptoms
            test_report_text: Test report text
            medical_history: Medical history
            chief_complaint: Chief complaint
            user_location: User's location for basic recommendations
            
        Returns:
            Dict[str, Any]: Fallback analysis
        """
        # Determine risk level based on available data
        risk_level = "moderate"  # Default
        severity_score = 0
        emergency_indicators = []
        
        # Analyze symptoms for risk assessment
        if symptoms:
            severity = None
            if isinstance(symptoms, dict) and "symptoms" in symptoms:
                symptom_list = symptoms["symptoms"]
                if isinstance(symptom_list, list) and symptom_list:
                    for symptom in symptom_list:
                        if isinstance(symptom, dict):
                            # Check severity
                            if "severity" in symptom:
                                severity = symptom.get("severity")
                                if isinstance(severity, (int, float)):
                                    severity_score = max(severity_score, severity)
                                    if severity >= 9:
                                        risk_level = "critical"
                                        emergency_indicators.append("Severe pain/symptom reported (9-10/10)")
                                    elif severity >= 7:
                                        risk_level = "high"
                                    elif severity >= 5:
                                        risk_level = "moderate"
                            
                            # Check for emergency keywords
                            symptom_text = str(symptom).lower()
                            if any(keyword in symptom_text for keyword in [
                                "chest pain", "difficulty breathing", "shortness of breath", 
                                "severe headache", "loss of consciousness", "seizure",
                                "severe bleeding", "severe abdominal pain", "stroke",
                                "heart attack", "suicide", "overdose"
                            ]):
                                risk_level = "high"
                                emergency_indicators.append("Potential emergency symptoms reported")
        
        # Check chief complaint for emergency indicators
        if chief_complaint:
            complaint_text = chief_complaint.lower()
            if any(keyword in complaint_text for keyword in [
                "emergency", "urgent", "severe", "can't breathe", "chest pain",
                "heart attack", "stroke", "bleeding", "unconscious"
            ]):
                if risk_level not in ["high", "critical"]:
                    risk_level = "high"
                emergency_indicators.append("Emergency keywords in chief complaint")
        
        # Create appropriate recommendations based on risk level
        recommendations = self._generate_fallback_recommendations(risk_level, severity_score, emergency_indicators)
        
        # Generate key findings
        key_findings = self._generate_fallback_findings(symptoms, chief_complaint, severity_score)
        
        fallback_result = {
            "summary": self._generate_fallback_summary(risk_level, error_message, chief_complaint),
            "risk_level": risk_level,
            "key_findings": key_findings,
            "recommendations": recommendations,
            "follow_up_suggestions": self._generate_follow_up_suggestions(risk_level),
            "confidence_score": 40 if symptoms else 25,  # Higher confidence if we have symptom data
            "disclaimer": self._get_default_disclaimer(),
            "ai_analysis": {
                "error": error_message,
                "fallback_analysis": True,
                "chief_complaint": chief_complaint,
                "risk_assessment_method": "rule-based",
                "severity_score": severity_score,
                "emergency_indicators": emergency_indicators,
                "analysis_timestamp": datetime.utcnow().isoformat()
            },
            "created_at": datetime.utcnow(),
            "emergency_alert": self._create_emergency_alert(risk_level, emergency_indicators) if risk_level in ["high", "critical"] else None
        }
        
        # Add basic location recommendations if location is provided
        if user_location:
            fallback_result["location_recommendations"] = {
                "user_location": user_location,
                "note": "AI analysis unavailable. Please search for local healthcare providers manually.",
                "general_advice": [
                    f"Contact local hospitals in {user_location} for medical evaluation",
                    f"Consider urgent care centers in {user_location} for non-emergency concerns",
                    f"Call 911 if experiencing a medical emergency in {user_location}"
                ]
            }
        
        return fallback_result
    
    def _generate_fallback_recommendations(self, risk_level: str, severity_score: float, emergency_indicators: list) -> list:
        """Generate appropriate recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == "critical":
            recommendations.extend([
                {
                    "category": "emergency",
                    "action": "Seek immediate emergency medical attention - call 911 or go to emergency room",
                    "priority": "critical",
                    "timeline": "Immediately"
                },
                {
                    "category": "immediate",
                    "action": "Do not delay medical care - this may be a medical emergency",
                    "priority": "critical",
                    "timeline": "Now"
                }
            ])
        elif risk_level == "high":
            recommendations.extend([
                {
                    "category": "urgent",
                    "action": "Seek urgent medical attention within 2-4 hours",
                    "priority": "high",
                    "timeline": "Within 2-4 hours"
                },
                {
                    "category": "follow_up",
                    "action": "Consider urgent care or emergency room if symptoms worsen",
                    "priority": "high",
                    "timeline": "If symptoms change"
                }
            ])
        else:
            recommendations.extend([
                {
                    "category": "follow_up",
                    "action": "Schedule an appointment with your primary care physician",
                    "priority": "medium",
                    "timeline": "Within 24-48 hours" if risk_level == "moderate" else "Within 1-2 weeks"
                }
            ])
        
        # Always add monitoring recommendation
        recommendations.append({
            "category": "monitoring",
            "action": "Monitor symptoms closely and seek immediate care if they worsen significantly",
            "priority": "high",
            "timeline": "Ongoing"
        })
        
        return recommendations
    
    def _generate_fallback_findings(self, symptoms: Optional[Dict[str, Any]], chief_complaint: Optional[str], severity_score: float) -> list:
        """Generate key findings based on available data"""
        findings = []
        
        if chief_complaint:
            findings.append(f"Chief complaint reported: {chief_complaint[:100]}..." if len(chief_complaint) > 100 else f"Chief complaint: {chief_complaint}")
        
        if severity_score > 0:
            if severity_score >= 8:
                findings.append(f"High symptom severity reported ({severity_score}/10)")
            elif severity_score >= 5:
                findings.append(f"Moderate symptom severity reported ({severity_score}/10)")
            else:
                findings.append(f"Mild symptom severity reported ({severity_score}/10)")
        
        findings.extend([
            "Comprehensive medical evaluation recommended",
            "Professional medical assessment required for proper diagnosis",
            "AI analysis system temporarily unavailable"
        ])
        
        return findings
    
    def _generate_fallback_summary(self, risk_level: str, error_message: str, chief_complaint: Optional[str]) -> str:
        """Generate appropriate summary based on risk level"""
        if risk_level == "critical":
            return "URGENT: Based on reported symptoms, this may require immediate medical attention. AI analysis is unavailable, but symptom severity suggests emergency evaluation."
        elif risk_level == "high":
            return "HIGH PRIORITY: Reported symptoms suggest need for urgent medical evaluation. While AI analysis is unavailable, prompt medical attention is recommended."
        else:
            return f"Medical consultation recommended for proper evaluation. {error_message.split(':')[0] if ':' in error_message else 'AI analysis temporarily unavailable'}. Please consult with a healthcare provider."
    
    def _generate_follow_up_suggestions(self, risk_level: str) -> list:
        """Generate follow-up suggestions based on risk level"""
        base_suggestions = [
            "Keep a detailed symptom diary with times, severity, and triggers",
            "Prepare a list of questions for your healthcare provider",
            "Bring any relevant medical records and test results to your appointment"
        ]
        
        if risk_level in ["high", "critical"]:
            base_suggestions.insert(0, "Do not delay seeking medical care if symptoms worsen or new symptoms develop")
            base_suggestions.append("Have emergency contact information readily available")
        else:
            base_suggestions.append("Schedule follow-up as recommended by your healthcare provider")
            base_suggestions.append("Contact your doctor if symptoms persist or worsen")
        
        return base_suggestions
    
    def _create_emergency_alert(self, risk_level: str, emergency_indicators: list) -> dict:
        """Create emergency alert for high-risk situations"""
        if risk_level == "critical":
            return {
                "is_emergency": True,
                "severity_level": risk_level,
                "immediate_actions": [
                    "Call 911 or emergency services immediately",
                    "Go to the nearest emergency room",
                    "Do not drive yourself - call for ambulance or have someone drive you",
                    "Bring all medications and medical information with you"
                ],
                "emergency_contacts": ["911", "Local Emergency Services", "Poison Control: 1-800-222-1222"],
                "message": "This appears to be a potential medical emergency. Seek immediate professional medical attention."
            }
        elif risk_level == "high":
            return {
                "is_emergency": False,
                "severity_level": risk_level,
                "immediate_actions": [
                    "Seek urgent medical attention within 2-4 hours",
                    "Consider urgent care or emergency room",
                    "Monitor symptoms closely",
                    "Have someone available to assist if needed"
                ],
                "emergency_contacts": ["Primary Care Physician", "Urgent Care Center", "Emergency Services: 911"],
                "message": "Urgent medical evaluation recommended. Do not delay seeking professional medical care."
            }
        
    async def _add_location_recommendations(
        self, 
        analysis_result: Dict[str, Any], 
        user_location: str
    ) -> Dict[str, Any]:
        """
        Add location-based hospital and doctor recommendations to analysis result
        
        Args:
            analysis_result: Existing AI analysis result
            user_location: User's location
            
        Returns:
            Dict[str, Any]: Enhanced analysis result with location recommendations
        """
        try:
            # Import here to avoid circular imports
            from app.services.location_medical_service import location_medical_service
            
            # Extract diagnosed conditions from analysis
            diagnosed_conditions = []
            if "possible_conditions" in analysis_result:
                conditions = analysis_result["possible_conditions"]
                if isinstance(conditions, list):
                    for condition in conditions:
                        if isinstance(condition, dict) and "condition" in condition:
                            diagnosed_conditions.append(condition["condition"])
                        elif isinstance(condition, str):
                            diagnosed_conditions.append(condition)
            
            # Get facility recommendations
            if diagnosed_conditions:
                risk_level = analysis_result.get("risk_level", "moderate")
                
                facility_recommendations = await location_medical_service.get_recommended_facilities_for_condition(
                    location=user_location,
                    diagnosed_conditions=diagnosed_conditions,
                    risk_level=risk_level
                )
                
                # Add location recommendations to the analysis result
                analysis_result["location_recommendations"] = {
                    "user_location": user_location,
                    "facility_search_results": facility_recommendations,
                    "location_based_advice": self._generate_location_advice(
                        diagnosed_conditions, risk_level, user_location, facility_recommendations
                    )
                }
                
                # Enhance existing recommendations with location-specific advice
                existing_recommendations = analysis_result.get("recommendations", [])
                location_enhanced_recommendations = self._enhance_recommendations_with_location(
                    existing_recommendations, user_location, facility_recommendations
                )
                analysis_result["recommendations"] = location_enhanced_recommendations
            
            return analysis_result
            
        except Exception as e:
            # If location recommendations fail, return original analysis with error note
            analysis_result["location_recommendations"] = {
                "user_location": user_location,
                "error": f"Unable to fetch location-based recommendations: {str(e)}",
                "note": "Please search for local healthcare providers manually."
            }
            return analysis_result
    
    def _generate_location_advice(
        self, 
        conditions: List[str], 
        risk_level: str, 
        location: str,
        facility_data: Dict[str, Any]
    ) -> List[str]:
        """
        Generate location-specific medical advice
        
        Args:
            conditions: Diagnosed conditions
            risk_level: Risk level from analysis
            location: User location
            facility_data: Available facilities data
            
        Returns:
            List[str]: Location-specific advice
        """
        advice = []
        
        if risk_level in ["critical", "high"]:
            emergency_count = len(facility_data.get("emergency_facilities", []))
            if emergency_count > 0:
                advice.append(f"Seek immediate emergency care - {emergency_count} emergency facilities found in {location}")
            else:
                advice.append(f"Seek immediate emergency care - contact 911 or go to the nearest hospital in {location}")
        
        hospital_count = len(facility_data.get("hospitals", []))
        doctor_count = len(facility_data.get("doctors", []))
        
        if hospital_count > 0:
            advice.append(f"Found {hospital_count} hospitals in {location} for comprehensive medical care")
        
        if doctor_count > 0:
            advice.append(f"Located {doctor_count} healthcare providers in {location} for follow-up care")
        
        # Add specialty-specific advice
        specialist_recs = facility_data.get("specialist_recommendations", {})
        for specialty, data in specialist_recs.items():
            specialist_count = len(data.get("doctors", []))
            if specialist_count > 0:
                advice.append(f"Found {specialist_count} {specialty} specialists in your area")
        
        if not advice:
            advice.append(f"Please consult with healthcare providers in {location} for further evaluation")
        
        return advice
    
    def _enhance_recommendations_with_location(
        self, 
        recommendations: List[Dict[str, Any]], 
        location: str,
        facility_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Enhance existing recommendations with location-specific information
        
        Args:
            recommendations: Existing recommendations
            location: User location
            facility_data: Available facilities
            
        Returns:
            List[Dict[str, Any]]: Enhanced recommendations
        """
        enhanced = recommendations.copy()
        
        # Add location-specific recommendations
        if facility_data.get("emergency_facilities"):
            enhanced.insert(0, {
                "category": "emergency_access",
                "action": f"Emergency facilities are available in {location} if symptoms worsen significantly",
                "priority": "high",
                "timeline": "If needed immediately",
                "location_specific": True
            })
        
        if facility_data.get("urgent_care"):
            enhanced.append({
                "category": "urgent_care_access",
                "action": f"Urgent care centers in {location} are available for non-emergency concerns",
                "priority": "medium",
                "timeline": "Within 24 hours if symptoms persist",
                "location_specific": True
            })
        
        if facility_data.get("doctors"):
            enhanced.append({
                "category": "local_follow_up",
                "action": f"Schedule follow-up with healthcare providers in {location}",
                "priority": "medium",
                "timeline": "Within 1-2 weeks",
                "location_specific": True
            })
        
        return enhanced


# Global instance
ai_analysis_service = AIAnalysisService()