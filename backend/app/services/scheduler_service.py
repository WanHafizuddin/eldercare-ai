from apscheduler.schedulers.background import BackgroundScheduler
from app.services.email_service import send_alert_email

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def schedule_medication_reminder(reminder_id: str, email: str, medication: str, time_hh_mm: str):
    """
    Schedules a daily reminder at the specified time.
    """
    try:
        hour, minute = map(int, time_hh_mm.split(':'))
    except ValueError:
        raise ValueError("time_hh_mm must be in HH:MM format")

    def job_func():
        print(f"Executing scheduled job for {medication} to {email}")
        send_alert_email(
            user_email=email,
            risk_level="REMINDER",
            explanation=f"It is time to take your medication: {medication}.",
            recommended_action="Please take it as prescribed and log it if necessary in your app."
        )

    # Schedule standard CRON daily
    scheduler.add_job(
        job_func, 
        'cron', 
        hour=hour, 
        minute=minute, 
        id=reminder_id, 
        replace_existing=True
    )

def cancel_medication_reminder(reminder_id: str):
    """
    Cancels a scheduled daily reminder.
    """
    if scheduler.get_job(reminder_id):
        scheduler.remove_job(reminder_id)
        return True
    return False
