#!/bin/bash

echo "🔧 Google Authentication Setup Helper"
echo "======================================"
echo ""

# Check if credentials.json exists
if [ -f "credentials.json" ]; then
    echo "✅ Found credentials.json file"
    echo "Converting to base64..."
    
    # Convert to base64 and update .env file
    BASE64_CREDS=$(base64 -i credentials.json)
    
    # Update .env file
    if [ -f ".env" ]; then
        # Replace the placeholder with actual credentials
        sed -i.bak "s/GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials_here/GOOGLE_CREDENTIALS_BASE64=$BASE64_CREDS/" .env
        echo "✅ Updated .env file with base64 credentials"
        echo ""
        echo "🚀 Google authentication is now configured!"
        echo "You can restart the Docker container to test login."
    else
        echo "❌ .env file not found"
        exit 1
    fi
else
    echo "📋 Setup Instructions:"
    echo ""
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Create a new project or select existing one"
    echo "3. Enable APIs:"
    echo "   - Gmail API"
    echo "   - Google Calendar API"
    echo "4. Create OAuth 2.0 credentials:"
    echo "   - Go to 'Credentials' → 'Create Credentials' → 'OAuth 2.0 Client ID'"
    echo "   - Application type: Web application"
    echo "   - Authorized redirect URIs: http://localhost:8080/callback"
    echo "5. Download the credentials as 'credentials.json'"
    echo "6. Place the file in this directory"
    echo "7. Run this script again"
    echo ""
    echo "📁 Expected file location: $(pwd)/credentials.json"
fi 