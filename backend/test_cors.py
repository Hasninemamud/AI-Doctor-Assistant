#!/usr/bin/env python3
"""
Simple CORS test script
"""

import requests
import json

def test_cors():
    """Test CORS preflight and registration"""
    base_url = "http://localhost:8000/api/v1/auth/register"
    
    # Test OPTIONS (CORS preflight)
    try:
        print("Testing CORS preflight...")
        options_response = requests.options(
            base_url,
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
        print(f"OPTIONS Status: {options_response.status_code}")
        print(f"OPTIONS Headers: {dict(options_response.headers)}")
        
        if options_response.status_code == 200:
            print("✅ CORS preflight successful!")
        else:
            print(f"❌ CORS preflight failed: {options_response.status_code}")
            print(f"Response text: {options_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing CORS: {e}")

def test_health():
    """Test health endpoint"""
    try:
        print("\nTesting health endpoint...")
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health Response: {response.json()}")
            print("✅ Backend is running!")
        else:
            print("❌ Backend health check failed")
    except Exception as e:
        print(f"❌ Backend not running: {e}")

if __name__ == "__main__":
    test_health()
    test_cors()