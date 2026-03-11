from pydantic import BaseModel, Field
from typing import Optional

class ReminderRequest(BaseModel):
    user_email: str = Field(..., description="Email to send the reminder to.")
    medication_name: str = Field(..., description="Name of the medication.")
    time_to_take: str = Field(..., description="Time to take the medication, e.g., '08:00', '14:30' in HH:MM format.")

class ReminderResponse(BaseModel):
    id: str
    user_email: str
    medication_name: str
    time_to_take: str
    status: str
