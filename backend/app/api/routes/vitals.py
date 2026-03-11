from fastapi import APIRouter, HTTPException
from app.schemas.vitals import VitalsLogRequest, VitalsLogResponse
from app.db.firestore import get_db
from google.cloud import firestore
from datetime import datetime, timezone
import uuid

router = APIRouter()

@router.post("/log", response_model=VitalsLogResponse)
def log_vitals(request: VitalsLogRequest):
    """
    Log daily vitals to Firebase Firestore.
    """
    try:
        db = get_db()
        data = request.model_dump()
        doc_id = str(uuid.uuid4())
        data["timestamp"] = datetime.now(timezone.utc)
        data["id"] = doc_id
        
        db.collection("vitals").document(doc_id).set(data)
        
        return VitalsLogResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save vitals: {str(e)}")

@router.get("/{user_id}", response_model=list[VitalsLogResponse])
def get_user_vitals(user_id: str):
    """
    Retrieve vitals for a specific user.
    """
    try:
        db = get_db()
        query = db.collection("vitals").where(
            filter=firestore.FieldFilter("user_id", "==", user_id)
        ).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(30)
        
        docs = query.stream()
        results = [doc.to_dict() for doc in docs]
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve vitals: {str(e)}")
