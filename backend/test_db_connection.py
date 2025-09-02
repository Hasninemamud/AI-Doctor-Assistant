#!/usr/bin/env python3
"""
Simple script to test PostgreSQL database connection
"""
import psycopg2
from app.core.config import settings

def test_connection():
    """Test database connection with current settings"""
    try:
        # Parse the DATABASE_URL
        db_url = settings.DATABASE_URL
        print(f"Testing connection with: {db_url}")
        
        # Try to connect
        connection = psycopg2.connect(db_url)
        cursor = connection.cursor()
        
        # Test simple query
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"✅ Connection successful!")
        print(f"PostgreSQL version: {result[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PostgreSQL database connection...")
    test_connection()