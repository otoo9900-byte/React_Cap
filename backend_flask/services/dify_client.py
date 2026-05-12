import os
import requests
from dotenv import load_dotenv

# Load .env file (try both root and backend_flask directory)
load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

DIFY_API_KEY = os.getenv('DIFY_API_KEY')
DIFY_API_URL = os.getenv('DIFY_API_URL', 'https://api.dify.ai/v1')

def send_message_to_dify(query, conversation_id="", user_id="promptgate-user"):
    """
    Send a message to Dify API and get a response.
    Uses blocking mode for now to match the existing frontend implementation.
    """
    if not DIFY_API_KEY:
        return {"error": "DIFY_API_KEY is not set in .env file"}

    headers = {
        'Authorization': f'Bearer {DIFY_API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking", # Request blocking mode
        "conversation_id": conversation_id, # Pass the conversation_id to maintain history
        "user": user_id
    }

    try:
        response = requests.post(
            f"{DIFY_API_URL}/chat-messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Dify API: {e}")
        return {"error": f"Failed to connect to Dify API: {str(e)}"}
