import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase only once
if not firebase_admin._apps:
    cert_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-adminsdk.json")
    if os.path.exists(cert_path):
        cred = credentials.Certificate(cert_path)
        firebase_admin.initialize_app(cred)
    else:
        print(f"WARNING: FIREBASE_CREDENTIALS_PATH ({cert_path}) not found. Firebase features will fail.")

def get_db():
    if not firebase_admin._apps:
        raise Exception(f"Firebase app is not initialized. Please ensure {os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase-adminsdk.json')} exists.")
    return firestore.client()
