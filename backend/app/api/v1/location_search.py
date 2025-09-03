# Location-based medical facility search API endpoints

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, Consultation
from app.schemas.schemas import (
    LocationSearchRequest, MedicalFacilityRecommendations,
    LocationBasedAnalysisRequest, EnhancedAnalysisWithLocation,
    HospitalInfo, DoctorInfo
)
from app.services.location_medical_service import location_medical_service

router = APIRouter()


@router.post("/search-hospitals", response_model=List[HospitalInfo])
async def search_hospitals(
    search_request: LocationSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search for hospitals near a specified location
    
    Args:
        search_request: Location search parameters
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[HospitalInfo]: List of hospitals matching search criteria
    """
    try:
        hospitals = await location_medical_service.search_hospitals_near_location(
            location=search_request.location,
            medical_condition=search_request.medical_condition,
            specialty=search_request.specialty,
            radius_km=search_request.radius_km
        )
        
        # Convert to HospitalInfo objects
        hospital_objects = []
        for hospital in hospitals:
            hospital_info = HospitalInfo(
                name=hospital.get("name", ""),
                address=hospital.get("address", ""),
                phone=hospital.get("phone", ""),
                type=hospital.get("type", "Hospital"),
                specialty=hospital.get("specialty"),
                rating=hospital.get("rating"),
                distance_km=hospital.get("distance_km"),
                emergency_services=hospital.get("emergency_services", False),
                accepts_insurance=hospital.get("accepts_insurance", True),
                website=hospital.get("website"),
                directions_url=hospital.get("directions_url"),
                description=hospital.get("description"),
                wait_time_minutes=hospital.get("wait_time_minutes"),
                trauma_level=hospital.get("trauma_level"),
                open_24_7=hospital.get("open_24_7")
            )
            hospital_objects.append(hospital_info)
        
        return hospital_objects
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hospital search failed: {str(e)}"
        )


@router.post("/search-doctors", response_model=List[DoctorInfo])
async def search_doctors(
    search_request: LocationSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search for doctors/specialists near a specified location
    
    Args:
        search_request: Location search parameters
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        List[DoctorInfo]: List of doctors matching search criteria
    """
    try:
        doctors = await location_medical_service.search_doctors_near_location(
            location=search_request.location,
            medical_condition=search_request.medical_condition,
            specialty=search_request.specialty,
            radius_km=search_request.radius_km
        )
        
        # Convert to DoctorInfo objects
        doctor_objects = []
        for doctor in doctors:
            doctor_info = DoctorInfo(
                name=doctor.get("name", ""),
                specialty=doctor.get("specialty", ""),
                practice_name=doctor.get("practice_name"),
                address=doctor.get("address", ""),
                phone=doctor.get("phone", ""),
                rating=doctor.get("rating"),
                years_experience=doctor.get("years_experience"),
                education=doctor.get("education"),
                accepts_new_patients=doctor.get("accepts_new_patients", True),
                accepts_insurance=doctor.get("accepts_insurance", True),
                distance_km=doctor.get("distance_km"),
                next_available=doctor.get("next_available"),
                website=doctor.get("website"),
                directions_url=doctor.get("directions_url"),
                languages=doctor.get("languages"),
                hospital_affiliations=doctor.get("hospital_affiliations")
            )
            doctor_objects.append(doctor_info)
        
        return doctor_objects
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Doctor search failed: {str(e)}"
        )


@router.post("/search-medical-facilities", response_model=MedicalFacilityRecommendations)
async def search_medical_facilities(
    search_request: LocationSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search for both hospitals and doctors near a specified location
    
    Args:
        search_request: Location search parameters
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        MedicalFacilityRecommendations: Combined results for hospitals and doctors
    """
    try:
        recommendations = {
            "hospitals": [],
            "doctors": [],
            "emergency_facilities": [],
            "urgent_care": [],
            "specialist_recommendations": {}
        }
        
        if search_request.search_type in ["hospitals", "both"]:
            hospitals = await location_medical_service.search_hospitals_near_location(
                location=search_request.location,
                medical_condition=search_request.medical_condition,
                specialty=search_request.specialty,
                radius_km=search_request.radius_km
            )
            recommendations["hospitals"] = hospitals
        
        if search_request.search_type in ["doctors", "both"]:
            doctors = await location_medical_service.search_doctors_near_location(
                location=search_request.location,
                medical_condition=search_request.medical_condition,
                specialty=search_request.specialty,
                radius_km=search_request.radius_km
            )
            recommendations["doctors"] = doctors
        
        # Also search for emergency and urgent care
        emergency_facilities = await location_medical_service.search_emergency_facilities(
            search_request.location
        )
        urgent_care = await location_medical_service.search_urgent_care_facilities(
            search_request.location
        )
        
        recommendations["emergency_facilities"] = emergency_facilities
        recommendations["urgent_care"] = urgent_care
        
        # Convert to proper response format
        hospital_objects = [HospitalInfo(**hospital) for hospital in recommendations["hospitals"]]
        doctor_objects = [DoctorInfo(**doctor) for doctor in recommendations["doctors"]]
        emergency_objects = [HospitalInfo(**facility) for facility in recommendations["emergency_facilities"]]
        urgent_care_objects = [HospitalInfo(**facility) for facility in recommendations["urgent_care"]]
        
        return MedicalFacilityRecommendations(
            hospitals=hospital_objects,
            doctors=doctor_objects,
            emergency_facilities=emergency_objects,
            urgent_care=urgent_care_objects,
            specialist_recommendations=recommendations["specialist_recommendations"],
            search_location=search_request.location,
            search_timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        return MedicalFacilityRecommendations(
            hospitals=[],
            doctors=[],
            emergency_facilities=[],
            urgent_care=[],
            specialist_recommendations={},
            search_location=search_request.location,
            search_timestamp=datetime.utcnow(),
            error_message=f"Search failed: {str(e)}"
        )


@router.post("/{consultation_id}/location-analysis", response_model=EnhancedAnalysisWithLocation)
async def get_location_based_analysis(
    consultation_id: str,
    location_request: LocationBasedAnalysisRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get enhanced analysis with location-based hospital and doctor recommendations
    
    Args:
        consultation_id: Consultation ID
        location_request: Location-based analysis parameters
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        EnhancedAnalysisWithLocation: Analysis with facility recommendations
    """
    try:
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
        
        # Get the latest analysis for this consultation
        from app.models.models import Analysis
        latest_analysis = db.query(Analysis).filter(
            Analysis.consultation_id == consultation_id
        ).order_by(Analysis.created_at.desc()).first()
        
        if not latest_analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No analysis found for this consultation. Please run analysis first."
            )
        
        # Get facility recommendations based on analysis
        diagnosed_conditions = location_request.diagnosed_conditions or []
        risk_level = location_request.risk_level or latest_analysis.risk_level.value
        
        # If no conditions provided, try to extract from analysis
        if not diagnosed_conditions and latest_analysis.ai_analysis:
            ai_data = latest_analysis.ai_analysis
            if isinstance(ai_data, dict) and "possible_conditions" in ai_data:
                conditions = ai_data["possible_conditions"]
                if isinstance(conditions, list):
                    diagnosed_conditions = [
                        condition.get("condition", "") if isinstance(condition, dict) else str(condition)
                        for condition in conditions
                    ]
        
        recommendations = await location_medical_service.get_recommended_facilities_for_condition(
            location=location_request.user_location,
            diagnosed_conditions=diagnosed_conditions,
            risk_level=risk_level
        )
        
        # Convert to proper response format
        facility_recommendations = None
        if not recommendations.get("error"):
            hospital_objects = [HospitalInfo(**hospital) for hospital in recommendations.get("hospitals", [])]
            doctor_objects = [DoctorInfo(**doctor) for doctor in recommendations.get("doctors", [])]
            emergency_objects = [HospitalInfo(**facility) for facility in recommendations.get("emergency_facilities", [])]
            urgent_care_objects = [HospitalInfo(**facility) for facility in recommendations.get("urgent_care", [])]
            
            facility_recommendations = MedicalFacilityRecommendations(
                hospitals=hospital_objects,
                doctors=doctor_objects,
                emergency_facilities=emergency_objects,
                urgent_care=urgent_care_objects,
                specialist_recommendations=recommendations.get("specialist_recommendations", {}),
                search_location=location_request.user_location,
                search_timestamp=datetime.utcnow()
            )
        
        # Create location-based recommendations
        location_based_recommendations = []
        
        if risk_level in ["critical", "high"]:
            location_based_recommendations.append({
                "priority": "critical" if risk_level == "critical" else "high",
                "category": "emergency_care",
                "action": f"Seek immediate medical attention at the nearest emergency facility in {location_request.user_location}",
                "timeline": "Immediately",
                "facilities_available": len(recommendations.get("emergency_facilities", []))
            })
        
        if diagnosed_conditions:
            for condition in diagnosed_conditions[:3]:  # Top 3 conditions
                location_based_recommendations.append({
                    "priority": "medium",
                    "category": "specialist_care",
                    "action": f"Consider consulting a specialist for {condition} in your area",
                    "timeline": "Within 1-2 weeks",
                    "condition": condition
                })
        
        location_based_recommendations.append({
            "priority": "low",
            "category": "follow_up",
            "action": f"Schedule follow-up care with local healthcare providers in {location_request.user_location}",
            "timeline": "As recommended",
            "facilities_available": len(recommendations.get("hospitals", [])) + len(recommendations.get("doctors", []))
        })
        
        # Emergency instructions for high-risk cases
        emergency_instructions = None
        if risk_level in ["critical", "high"]:
            emergency_instructions = {
                "call_911": risk_level == "critical",
                "nearest_emergency": recommendations.get("emergency_facilities", [])[:1],
                "urgent_care_options": recommendations.get("urgent_care", [])[:2],
                "warning_signs": [
                    "Difficulty breathing or shortness of breath",
                    "Severe chest pain",
                    "Sudden severe headache",
                    "Loss of consciousness",
                    "Severe bleeding"
                ],
                "instructions": f"Based on your analysis, seek immediate medical attention. If symptoms worsen, call 911 or go to the nearest emergency room in {location_request.user_location}."
            }
        
        # Convert analysis to proper format
        from app.schemas.schemas import AnalysisResponse
        analysis_response = AnalysisResponse(
            analysis_id=latest_analysis.id,
            consultation_id=consultation_id,
            summary=latest_analysis.summary or "Analysis completed",
            risk_level=latest_analysis.risk_level,
            key_findings=latest_analysis.ai_analysis.get("key_findings", []) if latest_analysis.ai_analysis else [],
            recommendations=latest_analysis.recommendations or [],
            emergency_alert=None,  # This would need to be extracted from ai_analysis if present
            follow_up_suggestions=latest_analysis.follow_up_suggestions or [],
            confidence_score=latest_analysis.confidence_score or 75,
            disclaimer="This analysis is for informational purposes only. Consult healthcare professionals for medical decisions."
        )
        
        return EnhancedAnalysisWithLocation(
            consultation_id=consultation_id,
            analysis=analysis_response,
            facility_recommendations=facility_recommendations,
            location_based_recommendations=location_based_recommendations,
            emergency_instructions=emergency_instructions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Location-based analysis failed: {str(e)}"
        )


@router.get("/emergency-facilities", response_model=List[HospitalInfo])
async def get_emergency_facilities(
    location: str = Query(..., description="Location to search for emergency facilities"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get emergency facilities near a location (for urgent situations)
    
    Args:
        location: Location to search near
        current_user: Current authenticated user
        
    Returns:
        List[HospitalInfo]: List of emergency facilities
    """
    try:
        emergency_facilities = await location_medical_service.search_emergency_facilities(location)
        
        # Convert to HospitalInfo objects
        facility_objects = []
        for facility in emergency_facilities:
            hospital_info = HospitalInfo(
                name=facility.get("name", ""),
                address=facility.get("address", ""),
                phone=facility.get("phone", ""),
                type=facility.get("type", "Emergency Room"),
                rating=facility.get("rating"),
                distance_km=facility.get("distance_km"),
                emergency_services=True,
                directions_url=facility.get("directions_url"),
                description=facility.get("description"),
                wait_time_minutes=facility.get("wait_time_minutes"),
                trauma_level=facility.get("trauma_level"),
                open_24_7=facility.get("open_24_7", True)
            )
            facility_objects.append(hospital_info)
        
        return facility_objects
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Emergency facility search failed: {str(e)}"
        )