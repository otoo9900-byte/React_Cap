import os
import google.generativeai as genai
from dotenv import load_dotenv

def generate_final_result(prompt):
    """
    Sends the generated prompt to Gemini API and returns the final result.
    """
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    load_dotenv(dotenv_path=env_path, override=True)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {"error": "GEMINI_API_KEY is not set in .env file"}

    genai.configure(api_key=api_key)

    # Use gemini-2.5-flash for fast and cost-effective responses
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {"error": f"Failed to generate result from Gemini: {str(e)}"}
