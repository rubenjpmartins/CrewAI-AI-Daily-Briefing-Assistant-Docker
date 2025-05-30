# Local Docker Testing Guide

This guide will help you test the Docker setup locally before deploying to CapRover.

## Prerequisites

1. **Docker** installed and running
2. **Google Cloud credentials** (`credentials.json` file)
3. **OpenRouter API key** from [OpenRouter](https://openrouter.ai/)

## Step 1: Prepare Environment

### Option A: Using credentials.json file (Recommended for local testing)
1. Place your `credentials.json` file in the project root
2. Create a `.env` file with:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
SECRET_KEY=local-dev-secret-key
GOOGLE_REDIRECT_URI=http://localhost:5000/callback
FLASK_ENV=development
```

### Option B: Using environment variables
1. Convert your credentials to base64:
```bash
base64 -i credentials.json
```
2. Create a `.env` file with:
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
SECRET_KEY=local-dev-secret-key
GOOGLE_REDIRECT_URI=http://localhost:5000/callback
GOOGLE_CREDENTIALS_BASE64=your_base64_encoded_credentials
FLASK_ENV=development
```

## Step 2: Build Docker Image

```bash
# Build the Docker image
docker build -t ai-briefing-local .

# Check if the image was built successfully
docker images | grep ai-briefing-local
```

## Step 3: Run Container Locally

### Option A: With .env file
```bash
docker run -p 5000:5000 --env-file .env ai-briefing-local
```

### Option B: With individual environment variables
```bash
docker run -p 5000:5000 \
  -e OPENROUTER_API_KEY=your_key_here \
  -e OPENROUTER_MODEL=anthropic/claude-3.5-sonnet \
  -e SECRET_KEY=local-dev-secret \
  -e GOOGLE_REDIRECT_URI=http://localhost:5000/callback \
  -e FLASK_ENV=development \
  ai-briefing-local
```

### Option C: With credentials file mounted
```bash
docker run -p 5000:5000 \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -e OPENROUTER_API_KEY=your_key_here \
  -e OPENROUTER_MODEL=anthropic/claude-3.5-sonnet \
  -e SECRET_KEY=local-dev-secret \
  -e GOOGLE_REDIRECT_URI=http://localhost:5000/callback \
  -e FLASK_ENV=development \
  ai-briefing-local
```

## Step 4: Test the Application

1. Open your browser and go to: http://localhost:5000
2. Test the health endpoint: http://localhost:5000/health
3. Try the Google OAuth login flow
4. Test the briefing functionality

## Available Models

You can test with different models by changing the `OPENROUTER_MODEL` environment variable:

**Popular Options:**
- `anthropic/claude-3.5-sonnet` (recommended)
- `openai/gpt-4o`
- `google/gemini-2.0-flash-exp`
- `meta-llama/llama-3.1-405b-instruct`
- `mistral/mistral-large`

**Budget-Friendly:**
- `anthropic/claude-3-haiku`
- `openai/gpt-4o-mini`
- `google/gemini-1.5-flash`

## Step 5: Debug if Needed

### View container logs
```bash
# Get container ID
docker ps

# View logs
docker logs <container_id>

# Follow logs in real-time
docker logs -f <container_id>
```

### Access container shell
```bash
docker exec -it <container_id> /bin/bash
```

### Stop container
```bash
docker stop <container_id>
```

## Common Issues and Solutions

### 1. Port already in use
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
docker run -p 8080:5000 --env-file .env ai-briefing-local
```

### 2. Credentials not found
- Ensure `credentials.json` exists or `GOOGLE_CREDENTIALS_BASE64` is set
- Check file permissions and paths

### 3. API key issues
- Verify your OpenRouter API key is correct
- Check if you have sufficient credits in your OpenRouter account
- Ensure the model name is correct

### 4. OAuth redirect issues
- Ensure redirect URI matches exactly: `http://localhost:5000/callback`
- Update Google Cloud Console OAuth settings if needed

### 5. Model errors
- Check if the model is available on OpenRouter
- Verify you have access to the specific model
- Some models may require special permissions

## Success Indicators

✅ Container builds without errors
✅ Health check returns 200 OK
✅ Home page loads at http://localhost:5000
✅ Google OAuth login works
✅ Briefing generation completes with your chosen model

## Cost Monitoring

- Monitor your usage in the [OpenRouter dashboard](https://openrouter.ai/activity)
- Set up usage alerts to avoid unexpected charges
- Start with budget-friendly models for testing

Once local testing is successful, you're ready to deploy to CapRover! 