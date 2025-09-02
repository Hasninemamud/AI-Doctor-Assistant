#!/usr/bin/env python3
"""
Test script to verify registration endpoint is working correctly
"""

import httpx
import asyncio
import json

async def test_registration():
    """Test the registration endpoint"""
    
    # Test data
    test_user = {
        "email": "test@example.com",
        "password": "TestPassword123",
        "name": "Test User",
        "date_of_birth": "1990-01-01",
        "gender": "male",
        "phone": "+1234567890"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Test OPTIONS request (CORS preflight)
            print("Testing CORS preflight request...")
            options_response = await client.options(
                "http://localhost:8000/api/v1/auth/register",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            print(f"OPTIONS Status: {options_response.status_code}")
            print(f"OPTIONS Headers: {dict(options_response.headers)}")
            
            # Test POST request (actual registration)
            print("\nTesting registration request...")
            response = await client.post(
                "http://localhost:8000/api/v1/auth/register",
                json=test_user,
                headers={
                    "Content-Type": "application/json",
                    "Origin": "http://localhost:3000"
                }
            )
            
            print(f"POST Status: {response.status_code}")
            print(f"POST Headers: {dict(response.headers)}")
            
            if response.status_code == 201:
                print("✅ Registration successful!")
                user_data = response.json()
                print(f"Created user: {user_data.get('name')} ({user_data.get('email')})")
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")
            print("Make sure the backend server is running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(test_registration())