from flask import Blueprint, request, jsonify
from services.dify_client import send_message_to_dify
from services.agent_service import run_agent_session, refine_travel_plan, GROQ_API_KEY
from services.llm_client import generate_final_result
import re

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/', methods=['POST'])
def handle_chat():
    """
    Handles incoming chat messages from the frontend.
    If GROQ_API_KEY is set → uses local Groq AI Agent (slot-fill + refine).
    Otherwise → falls back to Dify API.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conversation_id = data.get('conversationId', '')

    # --- GROQ / QWEN AI AGENT MODE ---
    if GROQ_API_KEY:
        try:
            messages  = data.get('messages', [])
            user_text = data.get('message', '')
            current_plan   = data.get('currentPlan', None)
            current_prompt = data.get('currentAssembledPrompt', None)

            if not messages and user_text:
                messages = [{"role": "user", "content": user_text}]

            # REFINE MODE: 이미 일정표가 완성된 상태에서 수정 요청이 온 경우
            if current_plan and user_text:
                refine_result = refine_travel_plan(current_plan, current_prompt or "", user_text)

                if "error" in refine_result:
                    return jsonify({"status": "error", "error": refine_result["error"]}), 500

                return jsonify({
                    "status": "success",
                    "response": "✏️ 요청하신 내용을 반영하여 일정을 수정했습니다! 우측 패널을 확인해 주세요.",
                    "assembledPrompt": refine_result.get("assembled_prompt", current_prompt),
                    "extractedIntents": None,
                    "conversation_id": conversation_id or "gemini-session",
                    "token_metrics": {
                        "savedTokens": 210,
                        "optimizedCostUsd": 0.00012,
                        "directCostUsd": 0.00180
                    },
                    "travel_plan": refine_result.get("travel_plan")
                })

            # SLOT-FILL MODE: 일반 슬롯 수집 대화
            gemini_result = run_agent_session(messages)

            if "error" in gemini_result:
                return jsonify({"status": "error", "error": gemini_result["error"]}), 500

            is_completed   = gemini_result.get("status") == "completed"
            ai_response    = gemini_result.get("next_question")
            assembled_prompt = gemini_result.get("assembled_prompt")
            slots          = gemini_result.get("slots", {})

            return jsonify({
                "status": "success",
                "response": ai_response,
                "assembledPrompt": assembled_prompt,
                "extractedIntents": slots,
                "conversation_id": conversation_id or "gemini-session",
                "token_metrics": {
                    "savedTokens": len(assembled_prompt) // 4 if assembled_prompt else 145,
                    "optimizedCostUsd": 0.00015 if is_completed else 0.00004,
                    "directCostUsd": 0.00180 if is_completed else 0.00025
                },
                "travel_plan": gemini_result.get("travel_plan")
            })
        except Exception as route_err:
            import traceback
            with open("error.log", "a", encoding="utf-8") as f:
                f.write("--- Chat Route Groq Error ---\n")
                f.write(f"Error: {str(route_err)}\n")
                traceback.print_exc(file=f)
            return jsonify({"status": "error", "error": f"Internal Groq Agent Error: {str(route_err)}"}), 500

    # --- DIFY FALLBACK MODE ---
    if 'message' not in data:
        return jsonify({"error": "No message provided for Dify fallback"}), 400

    user_message = data.get('message')
    dify_result = send_message_to_dify(user_message, conversation_id)

    if "error" in dify_result:
        return jsonify({"status": "error", "error": dify_result["error"]}), 500

    # Dify's blocking response contains 'answer', 'conversation_id', and potentially 'total_tokens'
    ai_answer = dify_result.get("answer", "No answer received from AI.")
    new_conversation_id = dify_result.get("conversation_id", "")
    
    # Remove <think>...</think> blocks from AI reasoning models (handles unclosed tags if cut off)
    ai_answer = re.sub(r'<think>[\s\S]*?(?:</think>|$)', '', ai_answer, flags=re.IGNORECASE).strip()
    
    # Parse for <prompt>...</prompt> tags
    assembled_prompt = None
    intents = {}
    prompt_match = re.search(r'<prompt>([\s\S]*?)</prompt>', ai_answer, re.IGNORECASE)
    if prompt_match:
        assembled_prompt = prompt_match.group(1).strip()
        # Remove the prompt block from the chat answer
        ai_answer = re.sub(r'<prompt>[\s\S]*?</prompt>', '', ai_answer, flags=re.IGNORECASE).strip()
        if not ai_answer:
            ai_answer = "✨ 여행 계획 최적화 프롬프트 조립이 완료되었습니다! 우측의 'Optimized Prompt' 작업 공간을 확인해 주세요."

        # Extract intents from the assembled prompt using regex for the UI dashboard tags
        dest_m = re.search(r'목적지:\s*(.*)', assembled_prompt)
        if dest_m: intents["destination"] = dest_m.group(1).strip()

        budget_m = re.search(r'(총 예산|예산):\s*(.*)', assembled_prompt)
        if budget_m: intents["budget"] = budget_m.group(2).strip()

        dur_m = re.search(r'(여행 기간|기간):\s*(.*)', assembled_prompt)
        if dur_m: intents["duration"] = dur_m.group(2).strip()

        comp_m = re.search(r'동반자:\s*(.*)', assembled_prompt)
        if comp_m: intents["companion"] = comp_m.group(1).strip()

        style_m = re.search(r'(여행 스타일|스타일):\s*(.*)', assembled_prompt)
        if style_m: intents["style"] = style_m.group(2).strip()

        det_m = re.search(r'상세 취향:\s*(.*)', assembled_prompt)
        if det_m: intents["detailed_preference"] = det_m.group(1).strip()

        food_m = re.search(r'(음식 취향 및 피해야 할 음식|음식 취향|음식):\s*(.*)', assembled_prompt)
        if food_m: intents["food_preference"] = food_m.group(2).strip()
    
    # Extract token usage if available (from metadata.usage)
    usage = dify_result.get("metadata", {}).get("usage", {})
    total_tokens = usage.get("total_tokens", 0)

    # For now, simulate some token savings for the dashboard
    return jsonify({
        "status": "success",
        "response": ai_answer,
        "assembledPrompt": assembled_prompt,
        "extractedIntents": intents if intents else None,
        "conversation_id": new_conversation_id,
        "token_metrics": {
            "savedTokens": len(assembled_prompt) // 4 if assembled_prompt else (total_tokens // 2 if total_tokens > 0 else 125),
            "optimizedCostUsd": 0.0002 if assembled_prompt else 0.0015,
            "directCostUsd": 0.0015 if assembled_prompt else 0.0025
        }
    })

@chat_bp.route('/execute', methods=['POST'])
def execute_prompt():
    """
    Executes the generated prompt using Gemini API and returns the result.
    """
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data.get('prompt')
    result = generate_final_result(prompt)

    if "error" in result:
        return jsonify({"status": "error", "error": result["error"]}), 500

    return jsonify({
        "status": "success",
        "result": result["result"]
    })
