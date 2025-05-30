# 🚀 CapRover Deployment Guide

This guide will help you deploy the CrewAI AI Daily Briefing Assistant to your CapRover server.

## 📋 Prerequisites

- CapRover server running and accessible
- CapRover CLI installed (`npm install -g caprover`)
- Your CapRover server configured and logged in
- OpenRouter API key
- Google OAuth credentials

## 🎯 Deployment Methods

### **Method 1: GitHub Repository Deployment (Recommended)**

#### Step 1: Create App in CapRover Dashboard

1. **Login to CapRover Dashboard**: `https://your-caprover-domain.com`
2. **Go to Apps**: Click on "Apps" in the sidebar
3. **Create New App**: 
   - App Name: `ai-briefing-assistant`
   - Check "Has Persistent Data" if you want to persist logs
4. **Click "Create New App"**

#### Step 2: Configure Environment Variables

In the CapRover dashboard, go to your app and set these environment variables:

```bash
# Required Variables
OPENAI_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your_super_secure_secret_key_here
GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_google_credentials
GOOGLE_REDIRECT_URI=https://your-app-name.your-caprover-domain.com/callback

# Optional Variables
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
FLASK_ENV=production
```

#### Step 3: Deploy from GitHub

1. **Go to Deployment Tab** in your app
2. **Select "Deploy from Github/Bitbucket/Gitlab"**
3. **Repository Info**:
   - Repository: `https://github.com/rubenjpmartins/CrewAI-AI-Daily-Briefing-Assistant-Docker`
   - Branch: `main`
   - Username: `rubenjpmartins` (if public repo, leave empty)
   - Password: Leave empty for public repo
4. **Click "Deploy Now"**

#### Step 4: Configure Domain (Optional)

1. **Go to HTTP Settings** tab
2. **Enable HTTPS**: Recommended for production
3. **Custom Domain**: Set up your custom domain if desired
4. **Force HTTPS**: Enable for security

### **Method 2: CapRover CLI Deployment**

#### Step 1: Setup CapRover CLI

```bash
# Install CapRover CLI (if not already installed)
npm install -g caprover

# Login to your CapRover server
caprover login
```

#### Step 2: Deploy from Local Directory

```bash
# Navigate to your project directory
cd /path/to/CrewAI-AI-Daily-Briefing-Assistant-Docker

# Deploy to CapRover
caprover deploy
```

Follow the prompts:
- **App Name**: `ai-briefing-assistant`
- **Captain Definition**: Use existing `captain-definition` file

#### Step 3: Set Environment Variables via CLI

```bash
# Set environment variables
caprover api --caproverUrl https://your-caprover-domain.com --path "/user/apps/appDefinitions/ai-briefing-assistant" --method POST --data '{
  "envVars": [
    {"key": "OPENAI_API_KEY", "value": "your_openrouter_api_key_here"},
    {"key": "SECRET_KEY", "value": "your_super_secure_secret_key_here"},
    {"key": "GOOGLE_CREDENTIALS_BASE64", "value": "your_base64_encoded_google_credentials"},
    {"key": "GOOGLE_REDIRECT_URI", "value": "https://ai-briefing-assistant.your-caprover-domain.com/callback"},
    {"key": "OPENROUTER_MODEL", "value": "mistralai/mistral-7b-instruct"},
    {"key": "FLASK_ENV", "value": "production"}
  ]
}'
```

## 🔧 Configuration Details

### **Environment Variables Explained**

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenRouter API key | `sk-or-v1-...` |
| `SECRET_KEY` | Flask session secret (generate random string) | `your-secret-key-here` |
| `GOOGLE_CREDENTIALS_BASE64` | Base64 encoded Google OAuth credentials | `eyJ3ZWIiOnsic...` |
| `GOOGLE_REDIRECT_URI` | OAuth callback URL | `https://your-app.domain.com/callback` |
| `OPENROUTER_MODEL` | AI model to use | `mistralai/mistral-7b-instruct` |
| `FLASK_ENV` | Flask environment | `production` |

### **Google OAuth Setup for CapRover**

1. **Google Cloud Console**: Go to your OAuth credentials
2. **Authorized Redirect URIs**: Add your CapRover app URL:
   ```
   https://ai-briefing-assistant.your-caprover-domain.com/callback
   ```
3. **Update Credentials**: Download updated `credentials.json`
4. **Convert to Base64**:
   ```bash
   base64 -i credentials.json
   ```
5. **Set Environment Variable**: Use the base64 output

## 🚀 Deployment Process

### **What Happens During Deployment**

1. **CapRover pulls** your code from GitHub
2. **Docker builds** the image using your Dockerfile
3. **Container starts** with your environment variables
4. **Health checks** verify the application is running
5. **Reverse proxy** routes traffic to your app

### **Expected Build Time**

- **First deployment**: 3-5 minutes (downloading dependencies)
- **Subsequent deployments**: 1-2 minutes (using cached layers)

## 🔍 Monitoring & Troubleshooting

### **Check Application Status**

1. **CapRover Dashboard**: Monitor app status and logs
2. **Health Check**: Visit `https://your-app-url.com/health`
3. **API Status**: Visit `https://your-app-url.com/api-status`

### **View Logs**

```bash
# Via CapRover CLI
caprover logs --app ai-briefing-assistant

# Or in CapRover Dashboard
# Go to Apps > ai-briefing-assistant > App Logs
```

### **Common Issues & Solutions**

#### **Build Failures**
```bash
# Check build logs in CapRover dashboard
# Common causes:
# - Missing captain-definition file
# - Dockerfile syntax errors
# - Dependency conflicts
```

#### **Runtime Errors**
```bash
# Check application logs
# Common causes:
# - Missing environment variables
# - Invalid Google credentials
# - OpenRouter API key issues
```

#### **OAuth Redirect Issues**
```bash
# Verify redirect URI matches exactly:
# Google Console: https://your-app.domain.com/callback
# Environment: GOOGLE_REDIRECT_URI=https://your-app.domain.com/callback
```

## 🔄 Updates & Maintenance

### **Updating the Application**

#### **Method 1: GitHub Auto-Deploy**
1. **Push changes** to your GitHub repository
2. **CapRover Dashboard**: Go to Deployment tab
3. **Click "Deploy Now"** to pull latest changes

#### **Method 2: CLI Update**
```bash
# Pull latest changes locally
git pull origin main

# Deploy updated version
caprover deploy
```

### **Scaling**

```bash
# Scale to multiple instances (in CapRover dashboard)
# Go to App Configs > Instance Count
# Increase for higher availability
```

## 🛡️ Security Considerations

### **Production Security Checklist**

- ✅ **HTTPS Enabled**: Force HTTPS in CapRover
- ✅ **Environment Variables**: Never commit secrets to Git
- ✅ **Google OAuth**: Restrict redirect URIs
- ✅ **API Keys**: Use environment variables only
- ✅ **Regular Updates**: Keep dependencies updated

### **Backup Strategy**

```bash
# Backup environment variables
caprover api --path "/user/apps/appDefinitions/ai-briefing-assistant" --method GET

# Backup application data (if using persistent volumes)
# Configure in CapRover dashboard under "App Configs"
```

## 📊 Performance Optimization

### **Resource Allocation**

```bash
# In CapRover Dashboard > App Configs:
# - Memory: 512MB minimum, 1GB recommended
# - CPU: 0.5 cores minimum, 1 core recommended
# - Instance Count: 1 for development, 2+ for production
```

### **Monitoring**

```bash
# Set up monitoring in CapRover:
# - Enable app metrics
# - Configure alerts for downtime
# - Monitor resource usage
```

## 🎉 Success!

Once deployed, your AI Daily Briefing Assistant will be available at:
`https://ai-briefing-assistant.your-caprover-domain.com`

### **Test the Deployment**

1. **Health Check**: `https://your-app-url.com/health`
2. **API Status**: `https://your-app-url.com/api-status`
3. **Login Flow**: Test Google OAuth login
4. **Generate Briefing**: Test the full workflow

---

**🚀 Your CrewAI Daily Briefing Assistant is now running on CapRover!** 