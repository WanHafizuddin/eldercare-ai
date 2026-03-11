from pydantic import BaseModel, Field
from typing import Literal

class SymptomRequest(BaseModel):
    symptoms: str = Field(..., description="The symptoms described by the user.")
    age: int | None = Field(None, description="Age of the patient. Optional.")
    pre_existing_conditions: str | None = Field(None, description="Any pre-existing conditions. Optional.")

class SymptomAssessmentResponse(BaseModel):
    risk_level: Literal["Low", "Medium", "High"] = Field(..., description="The assessed risk level.")
    explanation: str = Field(..., description="A clear, beginner-friendly explanation of why this risk level was chosen.")
    recommended_action: str = Field(..., description="Recommended immediate action for the user or family to take.")
