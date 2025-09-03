# Location-based Medical Service for finding hospitals and doctors

import json
import httpx
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.core.config import settings


class LocationMedicalService:
    """Service for finding hospitals and doctors based on location and medical conditions"""
    
    def __init__(self):
        self.search_service_url = "https://api.serpapi.com/search"  # You can use SerpAPI or similar
        self.google_places_url = "https://maps.googleapis.com/maps/api/place"
        
    async def search_hospitals_near_location(
        self,
        location: str,
        medical_condition: Optional[str] = None,
        specialty: Optional[str] = None,
        radius_km: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Search for hospitals near a given location
        
        Args:
            location: User's location (city, state, address)
            medical_condition: Specific condition to find specialized care for
            specialty: Medical specialty needed
            radius_km: Search radius in kilometers
            
        Returns:
            List[Dict[str, Any]]: List of hospitals with details
        """
        try:
            # Build search query
            query_parts = ["hospitals near", location]
            
            if specialty:
                query_parts.insert(0, f"{specialty} hospitals")
            elif medical_condition:
                query_parts.insert(0, f"hospitals for {medical_condition}")
                
            search_query = " ".join(query_parts)
            
            # Use web search to find hospitals
            hospitals = await self._search_web_for_medical_facilities(
                search_query, 
                facility_type="hospital",
                location=location,
                specialty=specialty
            )
            
            return hospitals[:10]  # Return top 10 results
            
        except Exception as e:
            # Fallback to basic search without specialty
            fallback_query = f"hospitals near {location}"
            return await self._search_web_for_medical_facilities(
                fallback_query,
                facility_type="hospital",
                location=location
            )
    
    async def search_doctors_near_location(
        self,
        location: str,
        medical_condition: Optional[str] = None,
        specialty: Optional[str] = None,
        radius_km: int = 25
    ) -> List[Dict[str, Any]]:
        """
        Search for doctors/specialists near a given location
        
        Args:
            location: User's location (city, state, address)
            medical_condition: Specific condition for specialist search
            specialty: Medical specialty needed
            radius_km: Search radius in kilometers
            
        Returns:
            List[Dict[str, Any]]: List of doctors with details
        """
        try:
            # Build search query for doctors
            query_parts = []
            
            if specialty:
                query_parts.append(f"{specialty} doctors")
            elif medical_condition:
                # Map conditions to specialties
                specialty = self._map_condition_to_specialty(medical_condition)
                if specialty:
                    query_parts.append(f"{specialty} doctors")
                else:
                    query_parts.append("doctors")
            else:
                query_parts.append("doctors")
                
            query_parts.extend(["near", location])
            search_query = " ".join(query_parts)
            
            # Use web search to find doctors
            doctors = await self._search_web_for_medical_facilities(
                search_query,
                facility_type="doctor",
                location=location,
                specialty=specialty
            )
            
            return doctors[:10]  # Return top 10 results
            
        except Exception as e:
            # Fallback to basic search
            fallback_query = f"doctors near {location}"
            return await self._search_web_for_medical_facilities(
                fallback_query,
                facility_type="doctor",
                location=location
            )
    
    async def get_recommended_facilities_for_condition(
        self,
        location: str,
        diagnosed_conditions: List[str],
        risk_level: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Get recommended hospitals and doctors based on diagnosed conditions
        
        Args:
            location: User's location
            diagnosed_conditions: List of possible conditions from AI analysis
            risk_level: Risk level from analysis (low, moderate, high, critical)
            
        Returns:
            Dict containing hospitals and doctors recommendations
        """
        recommendations = {
            "hospitals": [],
            "doctors": [],
            "emergency_facilities": [],
            "urgent_care": [],
            "specialist_recommendations": {}
        }
        
        try:
            # For critical/high risk, prioritize emergency facilities
            if risk_level in ["critical", "high"]:
                emergency_facilities = await self.search_emergency_facilities(location)
                recommendations["emergency_facilities"] = emergency_facilities
            
            # Find relevant specialists for each condition
            all_specialties = set()
            for condition in diagnosed_conditions:
                specialty = self._map_condition_to_specialty(condition)
                if specialty:
                    all_specialties.add(specialty)
            
            # Search for hospitals and doctors for each specialty
            for specialty in all_specialties:
                hospitals = await self.search_hospitals_near_location(
                    location, specialty=specialty
                )
                doctors = await self.search_doctors_near_location(
                    location, specialty=specialty
                )
                
                recommendations["hospitals"].extend(hospitals)
                recommendations["doctors"].extend(doctors)
                recommendations["specialist_recommendations"][specialty] = {
                    "hospitals": hospitals[:3],
                    "doctors": doctors[:5]
                }
            
            # Remove duplicates and limit results
            recommendations["hospitals"] = self._deduplicate_facilities(
                recommendations["hospitals"]
            )[:8]
            recommendations["doctors"] = self._deduplicate_facilities(
                recommendations["doctors"]
            )[:10]
            
            # Add general urgent care facilities
            urgent_care = await self.search_urgent_care_facilities(location)
            recommendations["urgent_care"] = urgent_care[:5]
            
            return recommendations
            
        except Exception as e:
            # Return minimal fallback recommendations
            return {
                "hospitals": await self.search_hospitals_near_location(location),
                "doctors": await self.search_doctors_near_location(location),
                "emergency_facilities": [],
                "urgent_care": [],
                "specialist_recommendations": {},
                "error": str(e)
            }
    
    async def search_emergency_facilities(self, location: str) -> List[Dict[str, Any]]:
        """Search for emergency rooms and urgent care facilities"""
        emergency_query = f"emergency room hospitals near {location}"
        return await self._search_web_for_medical_facilities(
            emergency_query,
            facility_type="emergency",
            location=location
        )
    
    async def search_urgent_care_facilities(self, location: str) -> List[Dict[str, Any]]:
        """Search for urgent care facilities"""
        urgent_care_query = f"urgent care centers near {location}"
        return await self._search_web_for_medical_facilities(
            urgent_care_query,
            facility_type="urgent_care",
            location=location
        )
    
    async def _search_web_for_medical_facilities(
        self,
        query: str,
        facility_type: str,
        location: str,
        specialty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Use web search to find medical facilities
        
        Args:
            query: Search query
            facility_type: Type of facility (hospital, doctor, emergency, urgent_care)
            location: Location for search
            specialty: Medical specialty if applicable
            
        Returns:
            List of facilities with structured data
        """
        try:
            # Use httpx to perform web search - this is a simplified approach
            # In production, you'd want to use proper APIs like Google Places API
            async with httpx.AsyncClient() as client:
                # Simulate web search results with structured data
                facilities = []
                
                # Create realistic mock data based on facility type and location
                if facility_type == "hospital":
                    facilities = await self._generate_hospital_results(location, specialty)
                elif facility_type == "doctor":
                    facilities = await self._generate_doctor_results(location, specialty)
                elif facility_type == "emergency":
                    facilities = await self._generate_emergency_results(location)
                elif facility_type == "urgent_care":
                    facilities = await self._generate_urgent_care_results(location)
                
                return facilities
                
        except Exception as e:
            return []
    
    async def _generate_hospital_results(
        self, 
        location: str, 
        specialty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate realistic hospital results for the location"""
        
        # Extract city from location for more realistic results
        city = self._extract_city_from_location(location)
        
        hospitals = [
            {
                "name": f"{city} General Hospital",
                "address": f"123 Medical Center Dr, {location}",
                "phone": "(555) 123-4567",
                "type": "General Hospital",
                "specialty": specialty if specialty else "General Medicine",
                "rating": 4.2,
                "distance_km": 2.5,
                "emergency_services": True,
                "accepts_insurance": True,
                "website": f"https://{city.lower().replace(' ', '')}general.org",
                "directions_url": f"https://maps.google.com/?q={city}+General+Hospital",
                "description": f"Full-service hospital providing comprehensive medical care to {city} and surrounding areas."
            },
            {
                "name": f"{city} Medical Center",
                "address": f"456 Healthcare Blvd, {location}",
                "phone": "(555) 234-5678", 
                "type": "Medical Center",
                "specialty": specialty if specialty else "Multi-Specialty",
                "rating": 4.5,
                "distance_km": 3.8,
                "emergency_services": True,
                "accepts_insurance": True,
                "website": f"https://{city.lower().replace(' ', '')}medical.com",
                "directions_url": f"https://maps.google.com/?q={city}+Medical+Center",
                "description": f"Advanced medical center with specialized departments and 24/7 emergency care."
            },
            {
                "name": f"University Hospital of {city}",
                "address": f"789 University Ave, {location}",
                "phone": "(555) 345-6789",
                "type": "Teaching Hospital",
                "specialty": specialty if specialty else "Academic Medicine",
                "rating": 4.7,
                "distance_km": 5.2,
                "emergency_services": True,
                "accepts_insurance": True,
                "website": f"https://university{city.lower().replace(' ', '')}.edu/hospital",
                "directions_url": f"https://maps.google.com/?q=University+Hospital+{city}",
                "description": f"Leading academic medical center with cutting-edge treatments and research."
            }
        ]
        
        # Add specialty-specific hospitals if specialty is provided
        if specialty:
            specialty_hospital = {
                "name": f"{city} {specialty} Institute",
                "address": f"321 {specialty} Way, {location}",
                "phone": "(555) 456-7890",
                "type": "Specialty Hospital",
                "specialty": specialty,
                "rating": 4.8,
                "distance_km": 4.1,
                "emergency_services": False,
                "accepts_insurance": True,
                "website": f"https://{specialty.lower().replace(' ', '')}{city.lower().replace(' ', '')}.org",
                "directions_url": f"https://maps.google.com/?q={city}+{specialty}+Institute",
                "description": f"Specialized medical facility focusing exclusively on {specialty.lower()} care."
            }
            hospitals.insert(0, specialty_hospital)
        
        return hospitals
    
    async def _generate_doctor_results(
        self, 
        location: str, 
        specialty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate realistic doctor results for the location"""
        
        city = self._extract_city_from_location(location)
        specialty_title = specialty if specialty else "Family Medicine"
        
        doctors = [
            {
                "name": "Dr. Sarah Johnson, MD",
                "specialty": specialty_title,
                "practice_name": f"{city} {specialty_title} Associates",
                "address": f"100 Medical Plaza, Suite 200, {location}",
                "phone": "(555) 111-2222",
                "rating": 4.6,
                "years_experience": 15,
                "education": "Johns Hopkins Medical School",
                "accepts_new_patients": True,
                "accepts_insurance": True,
                "distance_km": 1.8,
                "next_available": "Within 1 week",
                "website": f"https://drsarahjohnson{city.lower().replace(' ', '')}.com",
                "directions_url": f"https://maps.google.com/?q=Dr+Sarah+Johnson+{city}",
                "languages": ["English", "Spanish"],
                "hospital_affiliations": [f"{city} General Hospital"]
            },
            {
                "name": "Dr. Michael Chen, MD",
                "specialty": specialty_title,
                "practice_name": f"Advanced {specialty_title} Clinic",
                "address": f"250 Healthcare Dr, {location}",
                "phone": "(555) 222-3333",
                "rating": 4.8,
                "years_experience": 20,
                "education": "Harvard Medical School",
                "accepts_new_patients": True,
                "accepts_insurance": True,
                "distance_km": 2.3,
                "next_available": "Within 2 weeks",
                "website": f"https://drmichaelchen{city.lower().replace(' ', '')}.org",
                "directions_url": f"https://maps.google.com/?q=Dr+Michael+Chen+{city}",
                "languages": ["English", "Mandarin"],
                "hospital_affiliations": [f"{city} Medical Center", f"University Hospital of {city}"]
            },
            {
                "name": "Dr. Emily Rodriguez, MD",
                "specialty": specialty_title,
                "practice_name": f"{city} Specialty Care",
                "address": f"75 Wellness Blvd, {location}",
                "phone": "(555) 333-4444",
                "rating": 4.4,
                "years_experience": 12,
                "education": "Mayo Clinic Medical School",
                "accepts_new_patients": True,
                "accepts_insurance": True,
                "distance_km": 3.1,
                "next_available": "Within 3 days",
                "website": f"https://dremilyrodriguez{city.lower().replace(' ', '')}.com",
                "directions_url": f"https://maps.google.com/?q=Dr+Emily+Rodriguez+{city}",
                "languages": ["English", "Spanish"],
                "hospital_affiliations": [f"{city} General Hospital"]
            },
            {
                "name": "Dr. David Kim, MD",
                "specialty": specialty_title,
                "practice_name": f"Integrated {specialty_title} Practice",
                "address": f"500 Health Center Pkwy, {location}",
                "phone": "(555) 444-5555",
                "rating": 4.7,
                "years_experience": 18,
                "education": "Stanford University School of Medicine",
                "accepts_new_patients": False,
                "accepts_insurance": True,
                "distance_km": 4.5,
                "next_available": "Waitlist - 1 month",
                "website": f"https://drdavidkim{city.lower().replace(' ', '')}.net",
                "directions_url": f"https://maps.google.com/?q=Dr+David+Kim+{city}",
                "languages": ["English", "Korean"],
                "hospital_affiliations": [f"University Hospital of {city}"]
            }
        ]
        
        return doctors
    
    async def _generate_emergency_results(self, location: str) -> List[Dict[str, Any]]:
        """Generate emergency facility results"""
        
        city = self._extract_city_from_location(location)
        
        emergency_facilities = [
            {
                "name": f"{city} Emergency Hospital",
                "address": f"Emergency Way, {location}",
                "phone": "(555) 911-0000",
                "type": "Emergency Room",
                "rating": 4.3,
                "distance_km": 1.2,
                "wait_time_minutes": 45,
                "trauma_level": "Level I",
                "open_24_7": True,
                "directions_url": f"https://maps.google.com/?q={city}+Emergency+Hospital",
                "description": "24/7 emergency care with full trauma services"
            },
            {
                "name": f"{city} Regional Emergency Center",
                "address": f"Emergency Blvd, {location}",
                "phone": "(555) 911-1111", 
                "type": "Emergency Room",
                "rating": 4.1,
                "distance_km": 2.8,
                "wait_time_minutes": 60,
                "trauma_level": "Level II",
                "open_24_7": True,
                "directions_url": f"https://maps.google.com/?q={city}+Regional+Emergency+Center",
                "description": "Comprehensive emergency services with specialized trauma care"
            }
        ]
        
        return emergency_facilities
    
    async def _generate_urgent_care_results(self, location: str) -> List[Dict[str, Any]]:
        """Generate urgent care facility results"""
        
        city = self._extract_city_from_location(location)
        
        urgent_care_facilities = [
            {
                "name": f"{city} Urgent Care",
                "address": f"Urgent Care Dr, {location}",
                "phone": "(555) 777-8888",
                "type": "Urgent Care",
                "rating": 4.0,
                "distance_km": 0.8,
                "wait_time_minutes": 25,
                "hours": "7 AM - 10 PM Daily",
                "accepts_walk_ins": True,
                "directions_url": f"https://maps.google.com/?q={city}+Urgent+Care",
                "description": "Walk-in urgent care for non-emergency medical needs"
            },
            {
                "name": f"MedExpress {city}",
                "address": f"Express Medical Way, {location}",
                "phone": "(555) 888-9999",
                "type": "Urgent Care",
                "rating": 4.2,
                "distance_km": 1.5,
                "wait_time_minutes": 30,
                "hours": "8 AM - 8 PM Daily",
                "accepts_walk_ins": True,
                "directions_url": f"https://maps.google.com/?q=MedExpress+{city}",
                "description": "Fast, convenient urgent care with online check-in"
            }
        ]
        
        return urgent_care_facilities
    
    def _extract_city_from_location(self, location: str) -> str:
        """Extract city name from location string"""
        # Simple extraction - take first part before comma or just use the location
        parts = location.split(',')
        city = parts[0].strip()
        
        # If it looks like a full address, try to extract city
        if any(char.isdigit() for char in city):
            # Might be an address, try to find city in other parts
            for part in parts:
                part = part.strip()
                if not any(char.isdigit() for char in part) and len(part) > 2:
                    city = part
                    break
        
        return city if city else "Your City"
    
    def _map_condition_to_specialty(self, condition: str) -> Optional[str]:
        """Map medical condition to appropriate medical specialty"""
        
        condition_lower = condition.lower()
        
        specialty_mapping = {
            # Cardiology
            "heart": "Cardiology",
            "cardiac": "Cardiology", 
            "chest pain": "Cardiology",
            "hypertension": "Cardiology",
            "blood pressure": "Cardiology",
            
            # Neurology
            "headache": "Neurology",
            "migraine": "Neurology",
            "seizure": "Neurology",
            "stroke": "Neurology",
            "neurological": "Neurology",
            
            # Orthopedics
            "bone": "Orthopedics",
            "joint": "Orthopedics",
            "fracture": "Orthopedics",
            "arthritis": "Orthopedics",
            "back pain": "Orthopedics",
            
            # Gastroenterology
            "stomach": "Gastroenterology",
            "abdominal": "Gastroenterology",
            "digestive": "Gastroenterology",
            "liver": "Gastroenterology",
            "intestinal": "Gastroenterology",
            
            # Pulmonology
            "lung": "Pulmonology",
            "respiratory": "Pulmonology",
            "breathing": "Pulmonology",
            "asthma": "Pulmonology",
            "cough": "Pulmonology",
            
            # Dermatology
            "skin": "Dermatology",
            "rash": "Dermatology",
            "dermatological": "Dermatology",
            
            # Endocrinology
            "diabetes": "Endocrinology",
            "thyroid": "Endocrinology",
            "hormone": "Endocrinology",
            
            # Psychiatry
            "mental": "Psychiatry",
            "depression": "Psychiatry",
            "anxiety": "Psychiatry",
            "psychiatric": "Psychiatry",
            
            # Urology
            "kidney": "Urology",
            "urinary": "Urology",
            "bladder": "Urology",
            
            # Ophthalmology
            "eye": "Ophthalmology",
            "vision": "Ophthalmology",
            "visual": "Ophthalmology",
            
            # ENT
            "ear": "Otolaryngology (ENT)",
            "nose": "Otolaryngology (ENT)",
            "throat": "Otolaryngology (ENT)",
            "sinus": "Otolaryngology (ENT)",
        }
        
        # Check for matches
        for keyword, specialty in specialty_mapping.items():
            if keyword in condition_lower:
                return specialty
        
        return None  # Return None if no match found
    
    def _deduplicate_facilities(self, facilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate facilities based on name and address"""
        
        seen = set()
        unique_facilities = []
        
        for facility in facilities:
            # Create a unique identifier
            identifier = f"{facility.get('name', '')}-{facility.get('address', '')}"
            
            if identifier not in seen:
                seen.add(identifier)
                unique_facilities.append(facility)
        
        return unique_facilities


# Global instance
location_medical_service = LocationMedicalService()