from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import symptoms, vitals, reminders
from app.services.scheduler_service import start_scheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(title="ElderCare AI API", description="API for Elderly Health Monitor", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(symptoms.router, prefix="/api/symptoms", tags=["Symptoms"])
app.include_router(vitals.router, prefix="/api/vitals", tags=["Vitals"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to ElderCare AI API"}
