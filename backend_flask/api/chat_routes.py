from flask import Blueprint, request, jsonify
from services.dify_client import send_message_to_dify

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/', methods=['POST'])
def handle_chat():
    """
    Handles incoming chat messages from the frontend.
    Calls the Dify API and returns the response.
    """
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data.get('message')
    conversation_id = data.get('conversationId', '')
    
    # Send message to Dify
    dify_result = send_message_to_dify(user_message, conversation_id)

    if "error" in dify_result:
        return jsonify({"status": "error", "error": dify_result["error"]}), 500

    # Dify's blocking response contains 'answer', 'conversation_id', and potentially 'total_tokens'
    ai_answer = dify_result.get("answer", "No answer received from AI.")
    new_conversation_id = dify_result.get("conversation_id", "")
    
    # Extract token usage if available (from metadata.usage)
    usage = dify_result.get("metadata", {}).get("usage", {})
    total_tokens = usage.get("total_tokens", 0)

    # For now, simulate some token savings for the dashboard
    return jsonify({
        "status": "success",
        "response": ai_answer,
        "conversation_id": new_conversation_id,
        "token_metrics": {
            "savedTokens": total_tokens // 2 if total_tokens > 0 else 125,
            "optimizedCostUsd": 0.0015,
            "directCostUsd": 0.0025
        }
    })
