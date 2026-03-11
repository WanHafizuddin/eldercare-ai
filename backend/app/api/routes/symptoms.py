from fastapi import APIRouter, HTTPException
from app.schemas.symptom import SymptomRequest, SymptomAssessmentResponse
from app.services.gemini_service import assess_symptoms
from app.services.email_service import send_alert_email
import os

router = APIRouter()

@router.post("/check", response_model=SymptomAssessmentResponse)
async def check_symptoms(request: SymptomRequest):
    """
    Endpoint to assess symptoms using Gemini 2.0 Flash.
    Returns risk level, explanation, and recommended action.
    """
    try:
        assessment = assess_symptoms(
            symptoms=request.symptoms,
            age=request.age,
            conditions=request.pre_existing_conditions
        )
        
        if assessment.get("risk_level", "").lower() == "high":
            recipient = os.getenv("ALERT_RECIPIENT_EMAIL", "default_family_member@example.com")
            send_alert_email(
                user_email=recipient,
                risk_level=assessment.get("risk_level", "High"),
                explanation=assessment.get("explanation", "Reason not specified."),
                recommended_action=assessment.get("recommended_action", "Seek immediate medical attention.")
            )
        
        return SymptomAssessmentResponse(**assessment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
