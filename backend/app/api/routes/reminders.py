from fastapi import APIRouter, HTTPException
from app.schemas.reminder import ReminderRequest, ReminderResponse
from app.services.scheduler_service import schedule_medication_reminder
import uuid

router = APIRouter()

# In-memory store for prototype
reminders_db = []

@router.post("/", response_model=ReminderResponse)
def add_reminder(request: ReminderRequest):
    """
    Add a new medication reminder.
    """
    try:
        rem_id = str(uuid.uuid4())
        
        # Schedule it
        schedule_medication_reminder(
            reminder_id=rem_id,
            email=request.user_email,
            medication=request.medication_name,
            time_hh_mm=request.time_to_take
        )
        
        response_data = {
            "id": rem_id,
            "user_email": request.user_email,
            "medication_name": request.medication_name,
            "time_to_take": request.time_to_take,
            "status": "scheduled"
        }
        
        reminders_db.append(response_data)
        
        return ReminderResponse(**response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[ReminderResponse])
def get_reminders():
    """
    Retrieve all reminders.
    """
    return reminders_db

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: str):
    """
    Delete a reminder by ID.
    """
    global reminders_db
    for idx, reminder in enumerate(reminders_db):
        if reminder["id"] == reminder_id:
            del reminders_db[idx]
            from app.services.scheduler_service import cancel_medication_reminder
            cancel_medication_reminder(reminder_id)
            return {"detail": "Reminder deleted successfully."}
    raise HTTPException(status_code=404, detail="Reminder not found.")
