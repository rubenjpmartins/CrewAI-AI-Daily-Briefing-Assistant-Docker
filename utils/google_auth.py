import os, flask, pathlib, json, base64
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dateutil.parser import parse
from datetime import datetime
import warnings

# Suppress all OAuth warnings
warnings.filterwarnings("ignore", category=UserWarning, module="google_auth_oauthlib")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CLIENT_SECRETS_FILE = BASE_DIR / "credentials.json"

def get_client_secrets():
    """Get client secrets from file or environment variable"""
    # Try to get credentials from environment variable first
    if os.getenv("GOOGLE_CREDENTIALS_BASE64"):
        try:
            credentials_json = base64.b64decode(os.getenv("GOOGLE_CREDENTIALS_BASE64")).decode('utf-8')
            return json.loads(credentials_json)
        except Exception as e:
            print(f"Error loading credentials from environment: {e}")
    
    # Fall back to file
    if CLIENT_SECRETS_FILE.exists():
        with open(CLIENT_SECRETS_FILE, 'r') as f:
            return json.load(f)
    
    raise FileNotFoundError("No Google credentials found. Please set GOOGLE_CREDENTIALS_BASE64 environment variable or provide credentials.json file.")

def get_google_flow():
    # Get redirect URI from environment or use default for development
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
    
    client_secrets = get_client_secrets()
    
    flow = Flow.from_client_config(
        client_secrets,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    return flow

def fetch_token_safely(flow, authorization_response):
    """Fetch token with complete scope flexibility - accept whatever Google gives us"""
    from urllib.parse import urlparse, parse_qs
    import requests_oauthlib
    
    # Parse the authorization response first to validate it
    parsed_url = urlparse(authorization_response)
    query_params = parse_qs(parsed_url.query)
    
    # Check for error parameters first
    if 'error' in query_params:
        error_type = query_params['error'][0]
        error_desc = query_params.get('error_description', ['Unknown error'])[0]
        raise Exception(f"OAuth error from Google: {error_type} - {error_desc}")
    
    # Ensure we have an authorization code
    auth_code = query_params.get('code', [None])[0]
    if not auth_code:
        raise Exception("No authorization code received from Google")
    
    print(f"Attempting to fetch token with authorization code: {auth_code[:10]}...")
    
    # Create a completely new OAuth session that doesn't validate scopes
    try:
        print("Using completely permissive OAuth approach...")
        
        # Get the client config
        client_secrets = get_client_secrets()
        client_id = client_secrets['web']['client_id']
        client_secret = client_secrets['web']['client_secret']
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
        
        # Create a raw OAuth2 session without scope validation
        oauth = requests_oauthlib.OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri
        )
        
        # Fetch token without any scope validation
        token = oauth.fetch_token(
            token_url='https://oauth2.googleapis.com/token',
            code=auth_code,
            client_secret=client_secret
        )
        
        print("Token fetch successful with permissive approach!")
        
        # Create credentials object manually
        creds = Credentials(
            token=token['access_token'],
            refresh_token=token.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=token.get('scope', ' '.join(SCOPES)).split() if isinstance(token.get('scope'), str) else SCOPES
        )
        
        # Return the credentials directly - we'll handle flow assignment in the calling code
        return creds, token
        
    except Exception as e:
        error_str = str(e).lower()
        print(f"Permissive OAuth failed: {e}")
        
        if "invalid_grant" in error_str:
            if "authorization code" in error_str or "expired" in error_str:
                raise Exception("Authorization code expired or already used. Please try logging in again and complete the process quickly without refreshing the page.")
            else:
                raise Exception("Authorization code is invalid. Please try logging in again.")
        elif "bad request" in error_str:
            raise Exception(f"OAuth request failed: {e}")
        else:
            raise Exception(f"OAuth authentication failed: {e}")

def is_today(event_time_str):
    event_date = parse(event_time_str).date()
    return event_date == datetime.now().date()

def get_credentials_from_session(session):
    if "credentials" not in session:
        return None
    return Credentials(**session["credentials"])

def store_credentials_in_session(session, creds):
    session["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }

def fetch_gmail_summary(session):
    creds = get_credentials_from_session(session)
    if not creds:
        return "⚠️ Not logged in to Google."

    service = build("gmail", "v1", credentials=creds)
    response = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=10).execute()

    messages = response.get("messages", [])
    summaries = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = msg_data.get("snippet", "")
        summaries.append(snippet)

    return " ".join(summaries) if summaries else "No unread emails."

def fetch_calendar_summary(session):
    creds = get_credentials_from_session(session)
    if not creds:
        return "⚠️ Not logged in to Google."

    service = build("calendar", "v3", credentials=creds)
    now = datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return "You have no events today."

    summary_lines = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        if is_today(start):
            summary_lines.append(f"{start}: {event.get('summary', 'No title')}")

    return "\n".join(summary_lines)