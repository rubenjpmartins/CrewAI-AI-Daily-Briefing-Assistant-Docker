#!/usr/bin/env python3
"""
Test Mode for AI Daily Briefing Assistant
This script allows testing the OpenRouter integration without Google authentication.
"""

import os
import sys
from crew import crew

def test_openrouter_integration():
    """Test the OpenRouter integration directly"""
    print("🧪 Testing OpenRouter Integration")
    print("=" * 50)
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
    
    if not api_key or api_key == "your_openrouter_api_key_here":
        print("❌ OpenRouter API key not configured")
        print("Please set OPENAI_API_KEY in your .env file")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Model: {model}")
    print()
    
    # Test with sample data
    sample_emails = """
    Email 1: Meeting reminder for tomorrow at 2 PM with the development team.
    Email 2: Invoice #12345 from vendor ABC Corp for $1,500 due next week.
    Email 3: Project update: Phase 1 completed, moving to Phase 2.
    """
    
    sample_calendar = """
    Today's Events:
    - 9:00 AM: Daily standup meeting
    - 2:00 PM: Client presentation
    - 4:00 PM: Code review session
    """
    
    try:
        print("🚀 Running CrewAI with sample data...")
        print()
        
        # Create inputs for the crew
        inputs = {
            "email_data": sample_emails,
            "calendar_data": sample_calendar,
            "user_name": "Test User"
        }
        
        # Run the crew
        result = crew.kickoff(inputs=inputs)
        
        print("✅ CrewAI Execution Successful!")
        print("=" * 50)
        print("📋 Generated Briefing:")
        print(result)
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error running CrewAI: {e}")
        print()
        print("🔍 Troubleshooting:")
        print("1. Check your OpenRouter API key")
        print("2. Verify the model name is correct")
        print("3. Check your internet connection")
        return False

def main():
    """Main test function"""
    print("🤖 AI Daily Briefing Assistant - Test Mode")
    print("This mode tests OpenRouter integration without Google authentication")
    print()
    
    success = test_openrouter_integration()
    
    if success:
        print()
        print("🎉 Test completed successfully!")
        print("Your OpenRouter integration is working correctly.")
        print()
        print("Next steps:")
        print("1. Set up Google OAuth credentials")
        print("2. Run the full application with Docker")
    else:
        print()
        print("❌ Test failed. Please check your configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main() 