import os
from dotenv import load_dotenv

def generate_final_result(prompt):
    """
    Sends the generated prompt to Gemini API (if key present) or Groq API (fallback) and returns the final result.
    """
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(dotenv_path=env_path, override=True)
    
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
            print(f"Error calling Gemini API: {e}")
            return {"error": f"제미나이 API 호출 실패 (키 또는 권한 확인 필요): {str(e)}"}

            
    # 2. Fallback to Groq API (using llama-3.3-70b-versatile)
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
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
        return {"result": response.choices[0].message.content.strip()}
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {"error": f"Failed to generate result from Groq: {str(e)}"}
