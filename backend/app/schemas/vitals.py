from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VitalsLogRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user.")
    blood_pressure_systolic: Optional[int] = Field(None, description="Systolic blood pressure (e.g., 120).")
    blood_pressure_diastolic: Optional[int] = Field(None, description="Diastolic blood pressure (e.g., 80).")
    heart_rate: Optional[int] = Field(None, description="Heart rate in BPM.")
    glucose_level: Optional[float] = Field(None, description="Blood glucose level.")

class VitalsLogResponse(BaseModel):
    id: str
    user_id: str
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    glucose_level: Optional[float] = None
    timestamp: datetime
