# Docker Deployment Guide for CapRover

This guide will help you deploy the AI Daily Briefing Assistant to your CapRover server.

## Prerequisites

1. **CapRover server** set up and running
2. **Google Cloud Project** with Gmail and Calendar APIs enabled
3. **OpenRouter API key** from [OpenRouter](https://openrouter.ai/)

## Step 1: Google Cloud Setup

### 1.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Gmail API
   - Google Calendar API

### 1.2 Create OAuth 2.0 Credentials
1. Go to "Credentials" in the Google Cloud Console
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Add your CapRover domain to "Authorized redirect URIs":
   ```
   https://your-app-name.your-caprover-domain.com/callback
   ```
5. Download the credentials JSON file

### 1.3 Get OpenRouter API Key
1. Go to [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Buy credits (starting from $10)
4. Create an API key in your dashboard
5. Save it securely

## Step 2: CapRover Deployment

### 2.1 Create New App in CapRover
1. Log into your CapRover dashboard
2. Go to "Apps" → "Create New App"
3. Choose a name (e.g., `ai-briefing`)
4. Enable HTTPS

### 2.2 Configure Environment Variables
In your CapRover app settings, add these environment variables:

```bash
# Required: OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Choose your preferred model (default: anthropic/claude-3.5-sonnet)
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Required: Flask Secret Key (generate a secure random string)
SECRET_KEY=your_super_secure_secret_key_here

# Required: Google OAuth Redirect URI
GOOGLE_REDIRECT_URI=https://your-app-name.your-caprover-domain.com/callback

# Optional: Flask Environment
FLASK_ENV=production
```

### 2.3 Available Models
You can choose from 300+ models available on OpenRouter. Popular options include:

**Recommended Models:**
- `anthropic/claude-3.5-sonnet` - Excellent reasoning and writing
- `openai/gpt-4o` - Latest GPT-4 model
- `google/gemini-2.0-flash-exp` - Fast and capable
- `meta-llama/llama-3.1-405b-instruct` - Open source powerhouse
- `mistral/mistral-large` - European alternative

**Budget-Friendly Options:**
- `anthropic/claude-3-haiku` - Fast and affordable
- `openai/gpt-4o-mini` - Cheaper GPT-4 variant
- `google/gemini-1.5-flash` - Good balance of speed/cost

### 2.4 Upload Google Credentials
You have two options for the Google credentials:

**Option A: Environment Variable (Recommended)**
1. Convert your `credentials.json` to base64:
   ```bash
   base64 -i credentials.json
   ```
2. Add as environment variable:
   ```bash
   GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials
   ```

**Option B: File Upload**
1. Upload `credentials.json` to your app's persistent storage
2. Update the path in `utils/google_auth.py` if needed

### 2.5 Deploy from GitHub
1. In CapRover app settings, go to "Deployment"
2. Choose "Deploy from GitHub"
3. Enter your repository URL
4. Set branch to `main` (or your preferred branch)
5. Click "Deploy"

## Step 3: Post-Deployment Configuration

### 3.1 Update Google OAuth Settings
1. Go back to Google Cloud Console
2. Update the OAuth redirect URI to match your deployed app:
   ```
   https://your-app-name.your-caprover-domain.com/callback
   ```

### 3.2 Test the Application
1. Visit your deployed app URL
2. Click "Login with Google"
3. Authorize the application
4. Test the briefing functionality

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | No | Model to use (default: claude-3.5-sonnet) | `anthropic/claude-3.5-sonnet` |
| `SECRET_KEY` | Yes | Flask session secret | `your-secret-key` |
| `GOOGLE_REDIRECT_URI` | Yes | OAuth callback URL | `https://app.domain.com/callback` |
| `GOOGLE_CREDENTIALS_BASE64` | Optional | Base64 encoded credentials | `eyJ0eXBlIjoi...` |
| `FLASK_ENV` | Optional | Flask environment | `production` |

## Troubleshooting

### Common Issues

1. **OAuth Error**: Check that redirect URI matches exactly
2. **API Errors**: Ensure Gmail and Calendar APIs are enabled
3. **Credentials Error**: Verify credentials.json is accessible
4. **Model Not Found**: Check if model name is correct on OpenRouter
5. **Insufficient Credits**: Ensure you have credits in your OpenRouter account

### Logs
Check CapRover app logs for detailed error messages:
1. Go to your app in CapRover
2. Click "View Logs"
3. Look for Python/Flask error messages

## Security Notes

1. **Never commit credentials.json** to your repository
2. **Use strong SECRET_KEY** for Flask sessions
3. **Enable HTTPS** in CapRover for OAuth security
4. **Regularly rotate API keys** for security
5. **Monitor OpenRouter usage** to avoid unexpected charges

## Cost Management

OpenRouter offers transparent pricing:
- **Claude 3.5 Sonnet**: ~$3 per 1M input tokens
- **GPT-4o**: ~$2.50 per 1M input tokens
- **Gemini 2.0 Flash**: ~$0.075 per 1M input tokens

Monitor your usage in the OpenRouter dashboard to control costs.

## Scaling

For production use, consider:
1. Increasing worker count in Dockerfile
2. Adding Redis for session storage
3. Implementing rate limiting
4. Adding monitoring and logging
5. Setting up usage alerts in OpenRouter

## Support

If you encounter issues:
1. Check CapRover logs
2. Verify all environment variables are set
3. Test Google API credentials separately
4. Ensure all APIs are enabled in Google Cloud Console
5. Check OpenRouter dashboard for API usage and errors 