import os
from dotenv import load_dotenv

def generate_final_result(prompt):
    """
    Sends the generated prompt to Gemini API (if key present) or Groq API (fallback) and returns the final result.
    """
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(dotenv_path=env_path, override=True)
    
    gemini_error = None
    
    # 1. Try Gemini API if key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and api_key.strip():
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key.strip())
            # Use gemini-2.5-flash for fast and cost-effective responses
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            return {"result": response.text}
        except Exception as e:
            gemini_error = str(e)
            print(f"Error calling Gemini API: {e}")
            # We will fall through to Groq fallback but keep the error message
            
    # 2. Fallback to Groq API (using llama-3.3-70b-versatile)
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        if gemini_error:
            return {"error": f"제미나이 API 호출 실패 (할당량 초과 등): {gemini_error} (Groq 백업 키 없음)"}
        return {"error": "GEMINI_API_KEY or GROQ_API_KEY must be set in .env file"}

    try:
        from groq import Groq
        client = Groq(api_key=groq_api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        result_text = response.choices[0].message.content.strip()
        
        # If Gemini was intended but failed, prepend an informational banner
        if gemini_error:
            banner = (
                "> ⚠️ **안내:** 제미나이(Gemini) API 할당량(하루 20회 무료 제한)을 초과하여, "
                "**Groq 백업 엔진(Llama-3.3-70B)**으로 자동 우회하여 완성된 일정표입니다.\n\n---\n\n"
            )
            result_text = banner + result_text
            
        return {"result": result_text}
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        if gemini_error:
            return {"error": f"제미나이 실패: {gemini_error} | Groq 실패: {str(e)}"}
        return {"error": f"Failed to generate result from Groq: {str(e)}"}
