import os
import smtplib
from email.message import EmailMessage

def send_alert_email(user_email: str, risk_level: str, explanation: str, recommended_action: str):
    """
    Sends an email alert to the designated family member.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        print(f"--- EMAIL ALERT (Simulated) ---")
        print(f"To: {user_email}")
        print(f"Subject: HIGH RISK ALERT: Immediate Action Required")
        print(f"Explanation: {explanation}")
        print(f"Recommended Action: {recommended_action}")
        print(f"-------------------------------")
        print("Note: Email not sent because SENDER_EMAIL or SENDER_PASSWORD is not set in environment.")
        return

    try:
        msg = EmailMessage()
        msg.set_content(f"High risk detected!\n\nDetails:\n{explanation}\n\nPlease take the following action immediately:\n{recommended_action}")
        msg["Subject"] = "HIGH RISK ALERT: Immediate Action Required"
        msg["From"] = sender_email
        msg["To"] = user_email

        # Gmail SMTP server
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email alert successfully sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")
