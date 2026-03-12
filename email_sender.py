import os
import base64
import json
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# The permission we need to send emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def load_credentials():
    """
    Loads authentication credentials.
    1. Tries to load from a local 'token.json' file.
    2. If running in the cloud (GitHub Actions), tries to load from the 'GMAIL_TOKEN_JSON' environment variable.
    """
    creds = None
    
    # Check if we have the file locally
    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except Exception:
            print("⚠️ Local token.json seems corrupt.")

    # If no local file, checks environment variables (Critical for GitHub Actions)
    if not creds or not creds.valid:
        env_token = os.getenv("GMAIL_TOKEN_JSON")
        if env_token:
            print("☁️ Loading credentials from Environment Variable...")
            try:
                # Parse the JSON string from the env var and save it to a temp file needed by the library
                token_data = json.loads(env_token)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
                
                # Optional: Save it locally for next time (re-hydration)
                with open('token.json', 'w') as token_file:
                    token_file.write(env_token)
            except Exception as e:
                print(f"❌ Error loading token from environment: {e}")

    # Final check: If still no credentials, we might need manual login (only works locally)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired access token...")
            from google.auth.transport.requests import Request
            creds.refresh(Request())
        else:
            print("⚠️ No valid token found in file or environment.")
            if os.path.exists('credentials.json'):
                print("🖥️ Starting manual browser login...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                # Try standard port 8080, fallback just in case
                try:
                    # We use prompt='consent' to force Google to give us a 'refresh_token'
                    # This is CRITICAL for the GitHub Action to work forever, not just for 1 hour.
                    creds = flow.run_local_server(port=8080, prompt='consent', access_type='offline')
                except OSError:
                    print("⚠️ Port 8080 busy, trying random port...")
                    creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')
            else:
                print("❌ 'credentials.json' is also missing. Cannot authenticate.")
                return None
                
        # Save the new valid token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def send_email(html_content):
    """
    Composes and sends the email via Gmail API.
    """
    recipient = os.getenv("EMAIL_RECIPIENT")
    if not recipient:
        print("❌ Error: EMAIL_RECIPIENT is not set.")
        return

    print("🔐 Authenticating with Gmail...")
    creds = load_credentials()
    if not creds:
        print("❌ Authentication failed. Email will not be sent.")
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Create the email message
        subject = f"MorningByte – {datetime.datetime.now().strftime('%Y-%m-%d')}"
        message = MIMEText(html_content, 'html')
        message['to'] = recipient
        message['from'] = "Arjun Singh Kandari <arjunkandari15@gmail.com>"
        message['subject'] = subject
        
        # Encode for Gmail API
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        
        print(f"📤 Sending email to {recipient}...")
        service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print("✅ Email sent successfully!")
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
