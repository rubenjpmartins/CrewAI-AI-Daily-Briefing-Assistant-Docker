# 🤖 CrewAI AI Daily Briefing Assistant (Docker)

A powerful AI-powered daily briefing assistant that connects to your Gmail and Google Calendar to provide personalized daily summaries using multiple LLM models via OpenRouter.

## ✨ Features

- **🔗 Google Integration**: Seamlessly connects to Gmail and Google Calendar via OAuth
- **🤖 Multi-Agent AI System**: Uses CrewAI with specialized agents for different tasks
- **🌐 Multiple LLM Support**: Powered by OpenRouter with access to 300+ AI models
- **🐳 Docker Ready**: Fully containerized for easy deployment
- **📱 Web Interface**: Clean, modern web UI for easy interaction
- **🔒 Secure**: OAuth authentication and environment-based configuration

## 🏗️ Architecture

The system uses a multi-agent approach with CrewAI:

- **📧 Email Agent**: Analyzes and summarizes important emails
- **📅 Calendar Agent**: Reviews today's schedule and upcoming events  
- **📋 Summary Agent**: Composes a comprehensive daily briefing

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenRouter API key ([Get one here](https://openrouter.ai/))
- Google Cloud Console project with Gmail and Calendar APIs enabled

### 1. Clone the Repository

```bash
git clone https://github.com/rubenjpmartins/CrewAI-AI-Daily-Briefing-Assistant-Docker.git
cd CrewAI-AI-Daily-Briefing-Assistant-Docker
```

### 2. Set Up Environment

```bash
# Create environment file
./setup_env.sh

# Edit .env file with your credentials
nano .env
```

### 3. Configure Google OAuth

```bash
# Place your credentials.json file in the project root
# Then run the setup script
./setup_google_auth.sh
```

### 4. Build and Run

```bash
# Build the Docker image
docker build -t ai-briefing-assistant .

# Run the container
docker run -p 8080:5000 --env-file .env ai-briefing-assistant
```

### 5. Access the Application

Open your browser and go to: `http://localhost:8080`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenRouter API key | ✅ |
| `OPENROUTER_MODEL` | AI model to use (default: mistralai/mistral-7b-instruct) | ❌ |
| `SECRET_KEY` | Flask session secret key | ✅ |
| `GOOGLE_CREDENTIALS_BASE64` | Base64 encoded Google OAuth credentials | ✅ |
| `GOOGLE_REDIRECT_URI` | OAuth redirect URI (default: http://localhost:8080/callback) | ❌ |

### Supported AI Models

The application supports 300+ models via OpenRouter, including:

- **Claude**: `anthropic/claude-3.5-sonnet` (recommended)
- **GPT-4**: `openai/gpt-4o`
- **Gemini**: `google/gemini-2.0-flash-exp`
- **Llama**: `meta-llama/llama-3.1-405b-instruct`
- **Mistral**: `mistralai/mistral-7b-instruct` (default)

## 📖 Usage

1. **Login**: Click "Login with Google" and authorize access to Gmail and Calendar
2. **Generate Briefing**: Click "Generate Daily Briefing" to create your personalized summary
3. **Review**: The AI will analyze your emails and calendar to provide actionable insights

## 🛠️ Development

### Local Testing

```bash
# Test OpenRouter integration without Docker
python3 test_mode.py

# Run with development settings
FLASK_ENV=development python3 app.py
```

### Project Structure

```
├── agents/              # CrewAI agent definitions
├── tasks/               # CrewAI task definitions  
├── templates/           # HTML templates
├── utils/               # Utility functions
├── app.py              # Main Flask application
├── crew.py             # CrewAI crew configuration
├── Dockerfile          # Docker configuration
├── requirements.txt    # Python dependencies
└── setup_*.sh         # Setup scripts
```

## 🔍 API Endpoints

- `GET /` - Main dashboard
- `GET /login` - Initiate Google OAuth
- `GET /callback` - OAuth callback handler
- `POST /generate-briefing` - Generate daily briefing
- `GET /health` - Health check
- `GET /api-status` - API status and model info

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  ai-briefing:
    build: .
    ports:
      - "8080:5000"
    env_file:
      - .env
    restart: unless-stopped
```

### Production Deployment

For production deployment, see [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for detailed instructions.

### CapRover Deployment

For easy deployment to CapRover servers, see [CAPROVER_DEPLOYMENT.md](CAPROVER_DEPLOYMENT.md) for step-by-step instructions.

## 🧪 Testing

```bash
# Test OpenRouter integration
python3 test_mode.py

# Test health endpoints
curl http://localhost:8080/health
curl http://localhost:8080/api-status
```

## 📚 Documentation

- [Local Testing Guide](LOCAL_TESTING.md)
- [Docker Deployment Guide](DOCKER_DEPLOYMENT.md)
- [CapRover Deployment Guide](CAPROVER_DEPLOYMENT.md)
- [Environment Setup](env_complete_example)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [OpenRouter](https://openrouter.ai/) for LLM API access
- [Google APIs](https://developers.google.com/) for Gmail and Calendar integration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/rubenjpmartins/CrewAI-AI-Daily-Briefing-Assistant-Docker/issues) page
2. Review the documentation files
3. Create a new issue with detailed information

---

**⭐ If you find this project helpful, please give it a star!**
