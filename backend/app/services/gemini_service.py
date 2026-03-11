import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

# Configure the API key directly from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY is not set in environment.")

MODEL_ID = "gemini-1.5-flash-latest"

def assess_symptoms(symptoms: str, age: int = None, conditions: str = None) -> dict:
    """
    Calls Gemini to assess the risk of the given symptoms.
    Expected to return a JSON containing 'risk_level', 'explanation', and 'recommended_action'.
    """
    prompt = f"""
    You are an AI-powered elderly health monitoring assistant. Your job is to assess the risk of the symptoms provided and return a structured JSON response.

    Input Details:
    Symptoms: {symptoms}
"""
    if age:
        prompt += f"    Patient Age: {age}\n"
    if conditions:
        prompt += f"    Pre-existing Conditions: {conditions}\n"

    prompt += """
    Based on the information above, provide an assessment with the following exact JSON structure:
    {
        "risk_level": "Low" | "Medium" | "High",
        "explanation": "A clear, concise explanation of why this risk level was chosen, suitable for elderly patients or their families.",
        "recommended_action": "Clear actionable step to take (e.g., 'Rest and drink water', 'Call a doctor within 24 hours', 'Go to the emergency room immediately')."
    }
    
    Output nothing but the valid JSON. No markdown backticks, no extra text.
    """

    try:
        model = genai.GenerativeModel(MODEL_ID)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error accessing Gemini API: {e}")
        # Fallback response in case of error
        return {
            "risk_level": "High",
            "explanation": f"Failed to get AI assessment due to an error: {e}. Defaulting to high risk for safety.",
            "recommended_action": "Please consult a healthcare professional as we could not automate the assessment."
        }
