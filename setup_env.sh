#!/bin/bash

# AI Daily Briefing Assistant - Environment Setup Script
# This script creates a .env file with the correct configuration

echo "Creating .env file for AI Daily Briefing Assistant..."

cat > .env << 'EOF'
# AI Daily Briefing Assistant - Environment Configuration
# Fill in your actual values below

# ===== REQUIRED: OpenRouter API Configuration =====
# Get your API key from https://openrouter.ai/
OPENAI_API_KEY=your_openrouter_api_key_here

# Choose your preferred AI model (default: mistralai/mistral-7b-instruct)
# Popular options:
# - anthropic/claude-3.5-sonnet (recommended)
# - openai/gpt-4o
# - google/gemini-2.0-flash-exp
# - meta-llama/llama-3.1-405b-instruct
# - anthropic/claude-3-haiku (budget-friendly)
OPENROUTER_MODEL=mistralai/mistral-7b-instruct

# ===== REQUIRED: Flask Configuration =====
# Generate a secure random string for session encryption
SECRET_KEY=your_super_secure_secret_key_here

# ===== REQUIRED: Google OAuth Configuration =====
# For local testing
GOOGLE_REDIRECT_URI=http://localhost:8080/callback

# ===== GOOGLE CREDENTIALS (Choose ONE method) =====

# METHOD 1: Base64 encoded credentials (RECOMMENDED for Docker)
# 1. Download credentials.json from Google Cloud Console
# 2. Convert to base64: base64 -i credentials.json
# 3. Paste the output here:
GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials_here

# ===== OPTIONAL: Environment Settings =====
# Set to 'development' for local testing, 'production' for deployment
FLASK_ENV=development
EOF

echo "✅ .env file created successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Edit the .env file and replace placeholder values with your actual credentials"
echo "2. Get your OpenRouter API key from https://openrouter.ai/"
echo "3. Set up Google OAuth credentials and convert to base64"
echo "4. Generate a secure SECRET_KEY"
echo ""
echo "🚀 Then run: docker run -p 8080:8080 --env-file .env ai-briefing-assistant" 