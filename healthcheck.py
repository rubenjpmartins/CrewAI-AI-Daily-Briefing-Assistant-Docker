#!/usr/bin/env python3
"""
Simple health check script for the AI Daily Briefing Assistant
"""
import requests
import sys
import os

def health_check():
    try:
        # Check if the Flask app is responding
        response = requests.get('http://localhost:5000/health', timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return 0
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(health_check()) 