from flask import Blueprint, request, jsonify
import time

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/', methods=['POST'])
def handle_chat():
    """
    Handles incoming chat messages from the frontend.
    Currently returns a mocked response for testing the connection.
    """
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data.get('message')
    
    # Simulate processing delay
    time.sleep(1)

    # Mock response
    mock_response = f"백엔드에서 받은 메시지 '{user_message}'에 대한 가짜(Mock) 응답입니다. Dify 연동 전 테스트용입니다!"

    return jsonify({
        "status": "success",
        "response": mock_response,
        # We can also mock some token savings for testing the UI
        "token_metrics": {
            "savedTokens": 125,
            "optimizedCostUsd": 0.0015,
            "directCostUsd": 0.0025
        }
    })
