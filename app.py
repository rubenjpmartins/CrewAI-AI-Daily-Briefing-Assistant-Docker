from flask import Flask, jsonify, redirect, session, request, render_template, Response
from dotenv import load_dotenv
from crew import crew
from utils.google_auth import get_google_flow, store_credentials_in_session, fetch_calendar_summary, fetch_gmail_summary, fetch_token_safely
import os
import time
import logging
import sys
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/app.log')
    ]
)
logger = logging.getLogger(__name__)

# Only set insecure transport for local development
if os.getenv("FLASK_ENV") == "development":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")

# Simple in-memory store to prevent duplicate callback processing
processed_codes = {}

@app.route('/')
def index():
    logger.info("Index page accessed")
    return render_template("index.html")

@app.route('/login')
def login():
    logger.info("Login initiated")
    # Clear any existing session data to prevent conflicts
    session.clear()
    
    flow = get_google_flow()
    auth_url, state = flow.authorization_url(
        prompt="consent", 
        access_type="offline", 
        include_granted_scopes="true"
    )
    session["state"] = state
    session["oauth_flow_started"] = True
    session["login_timestamp"] = time.time()
    logger.info(f"OAuth flow started, redirecting to: {auth_url[:100]}...")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    logger.info("OAuth callback received")
    # Validate that we have a proper OAuth flow state
    if "state" not in session or "oauth_flow_started" not in session:
        logger.warning("Invalid OAuth state - no session data")
        return '''
        <h2>Invalid OAuth State</h2>
        <p>The OAuth flow was not properly initiated. Please start over.</p>
        <p><a href="/login">Click here to login again</a></p>
        ''', 400
    
    # Check if the login is too old (more than 10 minutes)
    login_time = session.get("login_timestamp", 0)
    if time.time() - login_time > 600:  # 10 minutes
        logger.warning("Login session expired")
        session.clear()
        return '''
        <h2>Login Session Expired</h2>
        <p>The login session has expired. Please start over.</p>
        <p><a href="/login">Click here to login again</a></p>
        ''', 400
    
    # Validate state parameter
    if request.args.get('state') != session.get('state'):
        logger.warning("OAuth state mismatch")
        return '''
        <h2>OAuth State Mismatch</h2>
        <p>Security validation failed. Please try logging in again.</p>
        <p><a href="/login">Click here to login again</a></p>
        ''', 400
    
    # Check for duplicate processing
    auth_code = request.args.get('code')
    if auth_code:
        logger.info(f"Processing authorization code: {auth_code[:10]}...")
        current_time = time.time()
        # Clean old entries (older than 10 minutes)
        processed_codes.clear()  # Simple cleanup for this demo
        
        if auth_code in processed_codes:
            logger.warning("Duplicate authorization code detected")
            return '''
            <h2>Duplicate Request</h2>
            <p>This authorization code has already been processed. Please start over.</p>
            <p><a href="/login">Click here to login again</a></p>
            ''', 400
        
        # Mark this code as being processed
        processed_codes[auth_code] = current_time
    
    flow = get_google_flow()
    
    try:
        logger.info("Attempting to fetch OAuth token...")
        # Use the safe token fetching function
        creds, token = fetch_token_safely(flow, request.url)
        logger.info("OAuth token fetch successful!")
    except Exception as e:
        error_msg = str(e)
        logger.error(f"OAuth error: {error_msg}")
        
        # Clear session on error to prevent stale state
        session.clear()
        
        # Remove from processed codes on error
        if auth_code and auth_code in processed_codes:
            del processed_codes[auth_code]
        
        # Provide user-friendly error messages
        if "expired or invalid" in error_msg.lower() or "invalid_grant" in error_msg.lower() or "already used" in error_msg.lower():
            return '''
            <h2>Authentication Expired</h2>
            <p>The authorization code has expired or been used already. This can happen if:</p>
            <ul>
                <li>You took too long to complete the login process</li>
                <li>You refreshed the page during authentication</li>
                <li>You clicked the login link multiple times</li>
                <li>You went back in your browser during the process</li>
            </ul>
            <p><strong>To fix this:</strong></p>
            <ol>
                <li>Click the login button below</li>
                <li>Complete the Google authentication quickly</li>
                <li>Do NOT refresh the page or go back</li>
                <li>Do NOT click login multiple times</li>
            </ol>
            <p><a href="/login" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Login Again</a></p>
            ''', 400
        elif "scope" in error_msg.lower():
            return '''
            <h2>Permission Scope Issue</h2>
            <p>There was an issue with the requested permissions. This can happen when:</p>
            <ul>
                <li>Google modifies the available permissions</li>
                <li>Your Google account has restrictions</li>
                <li>The app permissions need to be refreshed</li>
            </ul>
            <p><strong>To fix this:</strong></p>
            <ol>
                <li>Try logging in again</li>
                <li>Make sure to accept all requested permissions</li>
                <li>If the problem persists, try using a different Google account</li>
            </ol>
            <p><a href="/login" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Try Again</a></p>
            ''', 400
        else:
            return f'''
            <h2>Authentication Failed</h2>
            <p>Error: {error_msg}</p>
            <p>If this problem persists, please try:</p>
            <ul>
                <li>Using a different browser or incognito mode</li>
                <li>Clearing your browser cache and cookies</li>
                <li>Trying with a different Google account</li>
            </ul>
            <p><a href="/login">Click here to try again</a></p>
            ''', 400

    # Use the credentials directly instead of getting them from flow
    store_credentials_in_session(session, creds)
    
    # Clear OAuth flow state since we're done
    session.pop("state", None)
    session.pop("oauth_flow_started", None)
    session.pop("login_timestamp", None)
    
    logger.info("OAuth flow completed successfully, redirecting to briefing UI")
    return redirect("/briefing-ui")

@app.route('/briefing')
def briefing():
    logger.info("Starting briefing generation...")
    
    try:
        logger.info("Fetching email summary...")
        email_summary = fetch_gmail_summary(session)
        logger.info(f"Email summary retrieved: {len(email_summary)} characters")

        logger.info("Fetching calendar summary...")
        calendar_summary = fetch_calendar_summary(session)
        logger.info(f"Calendar summary retrieved: {len(calendar_summary)} characters")

        logger.info("🟡 EMAIL SUMMARY INPUT TO AGENT:")
        logger.info(email_summary[:500] + "..." if len(email_summary) > 500 else email_summary)

        logger.info("🔵 CALENDAR SUMMARY INPUT TO AGENT:")
        logger.info(calendar_summary)
        
        logger.info("Starting CrewAI processing...")
        start_time = time.time()
        
        result = crew.kickoff(inputs={
            "emails_data": email_summary,
            "calendar_data": calendar_summary
        })
        
        processing_time = time.time() - start_time
        logger.info(f"CrewAI processing completed in {processing_time:.2f} seconds")
        logger.info(f"Crew Result type: {type(result)}")
        logger.info(f"Crew Result: {str(result)[:500]}...")

        return jsonify({
            "briefing": str(result),
            "processing_time": f"{processing_time:.2f}s"
        })
        
    except Exception as e:
        logger.error(f"Error during briefing generation: {str(e)}", exc_info=True)
        return jsonify({
            "error": f"Failed to generate briefing: {str(e)}"
        }), 500

@app.route('/briefing-ui')
def briefing_ui():
    logger.info("Briefing UI accessed")
    return render_template("briefing.html")

@app.route('/logs')
def logs():
    """Stream real-time logs to the web interface"""
    def generate_logs():
        try:
            with open('/tmp/app.log', 'r') as f:
                # Get existing logs
                f.seek(0, 2)  # Go to end of file
                while True:
                    line = f.readline()
                    if line:
                        yield f"data: {line}\n\n"
                    else:
                        time.sleep(0.1)
        except FileNotFoundError:
            yield "data: Log file not found\n\n"
    
    return Response(generate_logs(), mimetype='text/plain')

@app.route('/api-status')
def api_status():
    """Check OpenRouter API status"""
    logger.info("Checking API status...")
    
    try:
        # OpenRouter configuration using same pattern as CrewAI LLM
        model_name = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct")
        api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter key stored as OPENAI_API_KEY
        base_url = "https://openrouter.ai/api/v1"  # OpenRouter endpoint
        
        if not api_key:
            raise Exception("OPENAI_API_KEY is required (contains OpenRouter key)")
        
        logger.info(f"Testing OpenRouter API with model: {model_name}")
        start_time = time.time()
        
        # Simple test request to OpenRouter
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8080",
            "X-Title": "AI Daily Briefing Assistant"
        }
        
        data = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "Hello, this is a test. Please respond with 'API working'."}
            ],
            "max_tokens": 20
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            test_response = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            
            logger.info(f"OpenRouter API test successful in {response_time:.2f}s")
            
            return jsonify({
                "status": "healthy",
                "api": "openrouter",
                "model": model_name,
                "response_time": f"{response_time:.2f}s",
                "test_response": test_response.strip(),
                "timestamp": datetime.now().isoformat()
            })
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            logger.error(f"OpenRouter API test failed: {error_msg}")
            return jsonify({
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }), 500
        
    except Exception as e:
        logger.error(f"API status check failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/health')
def health():
    logger.info("Health check accessed")
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # For development only
    app.run(debug=True, host="0.0.0.0", port=5000)