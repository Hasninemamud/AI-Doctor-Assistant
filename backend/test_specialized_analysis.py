# Test script for specialized medical models and timeline analysis

import asyncio
import json
from datetime import datetime, timedelta

from app.services.specialized_medical_service import specialized_medical_service, SymptomTimelineEntry
from app.services.timeline_analysis_service import timeline_analyzer


async def test_emergency_screening():
    """Test emergency screening functionality"""
    print("🚨 Testing Emergency Screening...")
    
    # Test case: chest pain with high severity
    symptoms = {
        "symptoms": [{
            "location": "chest",
            "severity": 9,
            "duration": "30 minutes",
            "quality": "crushing, radiating to left arm",
            "onset": "sudden"
        }]
    }
    
    result = await specialized_medical_service.emergency_screening_analysis(
        symptoms=symptoms,
        chief_complaint="severe chest pain with shortness of breath"
    )
    
    print(f"✅ Emergency screening result: {result['emergency_level']}")
    print(f"   Is emergency: {result['is_emergency']}")
    print(f"   Confidence: {result['confidence']}%")
    return result


async def test_timeline_analysis():
    """Test symptom timeline analysis"""
    print("\n📊 Testing Timeline Analysis...")
    
    # Create sample timeline entries
    base_time = datetime.now() - timedelta(hours=24)
    timeline_entries = [
        SymptomTimelineEntry(
            timestamp=base_time,
            symptom="mild headache",
            severity=3,
            location="frontal",
            quality="dull ache"
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(hours=2),
            symptom="nausea",
            severity=4,
            location="stomach",
            quality="queasy feeling"
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(hours=4),
            symptom="severe headache",
            severity=8,
            location="frontal and temporal",
            quality="throbbing pain"
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(hours=6),
            symptom="vomiting",
            severity=7,
            location="stomach",
            quality="projectile"
        )
    ]
    
    # Analyze timeline
    analysis = await timeline_analyzer.analyze_comprehensive_timeline(timeline_entries)
    
    print(f"✅ Timeline analysis completed")
    print(f"   Risk level: {analysis['risk_assessment']['risk_level']}")
    print(f"   Patterns found: {len(analysis['pattern_analysis']['rapid_onset'])}")
    print(f"   Recommendations: {len(analysis['clinical_recommendations'])}")
    
    return analysis


async def test_clinical_analysis():
    """Test clinical differential analysis"""
    print("\n🔬 Testing Clinical Analysis...")
    
    symptoms = {
        "symptoms": [{
            "location": "abdomen",
            "severity": 6,
            "duration": "2 days",
            "quality": "cramping pain",
            "associated_symptoms": ["diarrhea", "fever", "loss of appetite"]
        }]
    }
    
    test_results = """
    Lab Results:
    - WBC: 15,000 (elevated)
    - Temperature: 101.2°F
    - C-reactive protein: elevated
    - Stool culture: pending
    """
    
    result = await specialized_medical_service.clinical_differential_analysis(
        symptoms=symptoms,
        test_results=test_results,
        medical_history={"conditions": ["no known allergies"], "medications": []}
    )
    
    print(f"✅ Clinical analysis completed")
    print(f"   Analysis type: {result.get('analysis_type', 'clinical_analysis')}")
    print(f"   Summary available: {bool(result.get('summary'))}")
    
    return result


def test_pattern_detection():
    """Test pattern detection algorithms"""
    print("\n🔍 Testing Pattern Detection...")
    
    # Create timeline with rapid onset pattern
    base_time = datetime.now() - timedelta(hours=2)
    rapid_onset_timeline = [
        SymptomTimelineEntry(
            timestamp=base_time,
            symptom="chest tightness",
            severity=6
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(minutes=15),
            symptom="shortness of breath",
            severity=7
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(minutes=30),
            symptom="left arm pain",
            severity=8
        ),
        SymptomTimelineEntry(
            timestamp=base_time + timedelta(minutes=45),
            symptom="nausea",
            severity=5
        )
    ]
    
    # Analyze patterns
    patterns = timeline_analyzer._analyze_timeline_patterns(rapid_onset_timeline)
    severity_trends = timeline_analyzer._analyze_severity_trends(rapid_onset_timeline)
    
    print(f"✅ Pattern detection completed")
    print(f"   Patterns identified: {len(patterns)}")
    print(f"   Severity trends: {len(severity_trends)}")
    
    for pattern in patterns:
        print(f"   - {pattern.pattern_type}: {pattern.description}")
    
    return patterns


async def run_comprehensive_test():
    """Run all tests"""
    print("🧪 Starting Comprehensive Medical Analysis Tests\n")
    print("="*60)
    
    try:
        # Test 1: Emergency Screening
        emergency_result = await test_emergency_screening()
        
        # Test 2: Timeline Analysis
        timeline_result = await test_timeline_analysis()
        
        # Test 3: Clinical Analysis
        clinical_result = await test_clinical_analysis()
        
        # Test 4: Pattern Detection
        pattern_result = test_pattern_detection()
        
        print("\n" + "="*60)
        print("🎉 All Tests Completed Successfully!")
        print("="*60)
        
        # Summary
        print("\n📋 Test Summary:")
        print(f"✅ Emergency screening: {'PASS' if emergency_result else 'FAIL'}")
        print(f"✅ Timeline analysis: {'PASS' if timeline_result else 'FAIL'}")
        print(f"✅ Clinical analysis: {'PASS' if clinical_result else 'FAIL'}")
        print(f"✅ Pattern detection: {'PASS' if pattern_result else 'FAIL'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        return False


def test_configuration():
    """Test system configuration"""
    print("\n⚙️ Testing Configuration...")
    
    from app.core.config import settings
    
    # Check required settings
    tests = [
        ("OpenRouter API Key", bool(settings.OPENROUTER_API_KEY)),
        ("OpenRouter Base URL", bool(settings.OPENROUTER_BASE_URL)),
        ("OpenRouter Model", bool(settings.OPENROUTER_MODEL)),
        ("Database URL", bool(settings.DATABASE_URL)),
        ("Secret Key", bool(settings.SECRET_KEY))
    ]
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    return all(result for _, result in tests)


if __name__ == "__main__":
    print("🏥 AI Doctor Assistant - Specialized Medical Models Test Suite")
    print("="*70)
    
    # Test configuration first
    config_ok = test_configuration()
    
    if config_ok:
        # Run async tests
        success = asyncio.run(run_comprehensive_test())
        
        if success:
            print("\n🌟 All systems operational! Ready for specialized medical analysis.")
        else:
            print("\n⚠️ Some tests failed. Please check the configuration and try again.")
    else:
        print("\n❌ Configuration issues detected. Please check your .env file.")
        
    print("\n" + "="*70)