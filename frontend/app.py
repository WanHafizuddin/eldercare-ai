import streamlit as st
import requests
import json
import os
from datetime import datetime

# --- Configuration ---
st.set_page_config(page_title="ElderCare AI", page_icon="❤️", layout="centered")

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# --- UI Styling ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.title("❤️ ElderCare AI")
st.markdown("Your AI-powered personal health monitoring assistant. Assess symptoms, log daily vitals, and set medication reminders.")

tab1, tab2, tab3 = st.tabs(["🩺 Symptom Checker", "📈 Vitals Logger", "💊 Medication Reminders"])

# --- Tab 1: Symptom Checker ---
with tab1:
    st.header("Symptom Assessment")
    st.info("Describe your symptoms. Our AI will assess the risk level and provide actionable advice.")
    
    with st.form("symptom_form"):
        symptoms = st.text_area("What are your current symptoms?", placeholder="E.g., I have a mild headache, feel dizzy, and have a slight fever.")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (optional)", min_value=1, max_value=120, value=70)
        with col2:
            conditions = st.text_input("Pre-existing conditions (optional)", placeholder="E.g., Hypertension, Diabetes")
            
        submitted = st.form_submit_button("Assess Symptoms")
        
        if submitted:
            if not symptoms.strip():
                st.error("Please enter your symptoms to get an assessment.")
            else:
                with st.spinner("Analyzing your symptoms with Gemini 2.0 Flash..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/api/symptoms/check", json={
                            "symptoms": symptoms,
                            "age": age,
                            "pre_existing_conditions": conditions
                        })
                        
                        if response.status_code == 200:
                            data = response.json()
                            risk_level = data.get("risk_level", "Unknown")
                            
                            # Display conditional alert box based on risk
                            if risk_level.lower() == "high":
                                st.error(f"### 🚨 Risk Level: HIGH")
                                st.warning("An emergency alert has been automatically sent to your designated family member.")
                            elif risk_level.lower() == "medium":
                                st.warning(f"### ⚠️ Risk Level: MEDIUM")
                            else:
                                st.success(f"### ✅ Risk Level: LOW")
                                
                            st.markdown("#### Explanation")
                            st.write(data.get("explanation", "No explanation provided."))
                            
                            st.markdown("#### Recommended Action")
                            st.info(data.get("recommended_action", "Consult a doctor if symptoms persist."))
                        else:
                            st.error(f"Backend Error: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Failed to connect to the backend server. Please ensure the FastAPI server is running.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

# --- Tab 2: Vitals Logger ---
with tab2:
    st.header("Daily Vitals")
    st.info("Log your blood pressure, heart rate, and glucose levels to keep a history of your health.")
    
    user_id = st.text_input("Device / User ID", value="user_123")
    
    with st.form("vitals_form"):
        col1, col2 = st.columns(2)
        with col1:
            systolic = st.number_input("Systolic BP (mmHg)", min_value=0, max_value=300, value=120)
            heart_rate = st.number_input("Heart Rate (BPM)", min_value=0, max_value=250, value=72)
        with col2:
            diastolic = st.number_input("Diastolic BP (mmHg)", min_value=0, max_value=200, value=80)
            glucose = st.number_input("Glucose Level (mg/dL)", min_value=0.0, max_value=500.0, value=90.0, step=0.1)
            
        logged = st.form_submit_button("Log Vitals")
        
        if logged:
            with st.spinner("Saving vitals to Firebase..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/api/vitals/log", json={
                        "user_id": user_id,
                        "blood_pressure_systolic": systolic,
                        "blood_pressure_diastolic": diastolic,
                        "heart_rate": heart_rate,
                        "glucose_level": glucose
                    })
                    if response.status_code == 200:
                        st.success("Your vitals have been logged successfully!")
                    else:
                        st.error(f"Failed to log vitals: {response.json().get('detail', response.text)}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    st.markdown("---")
    st.subheader("Recent Vitals History")
    if st.button("Refresh History"):
        with st.spinner("Fetching from Firebase..."):
            try:
                res = requests.get(f"{API_BASE_URL}/api/vitals/{user_id}")
                if res.status_code == 200:
                    history = res.json()
                    if history:
                        for entry in history:
                            dt = entry.get('timestamp', 'Unknown Time')
                            bp_sys = entry.get('blood_pressure_systolic', '-')
                            bp_dia = entry.get('blood_pressure_diastolic', '-')
                            hr = entry.get('heart_rate', '-')
                            gluc = entry.get('glucose_level', '-')
                            st.write(f"- **{dt}**: BP {bp_sys}/{bp_dia} | HR {hr} | Glucose {gluc}")
                    else:
                        st.info("No vitals data found for this user.")
                else:
                    st.error(f"Failed to fetch history: {res.text}")
            except Exception as e:
                st.error("Error fetching history from backend.")

# --- Tab 3: Medication Reminders ---
with tab3:
    st.header("Medication Reminders")
    st.info("Schedule daily emails to remind you to take your medications.")
    
    with st.form("reminder_form"):
        rem_email = st.text_input("Your Email Address", value="patient@example.com")
        med_name = st.text_input("Medication Name", placeholder="E.g., Lisinopril 10mg")
        time_to_take = st.time_input("Daily Reminder Time")
        
        scheduled = st.form_submit_button("Schedule Reminder")
        
        if scheduled:
            if not med_name:
                st.error("Please enter a medication name.")
            else:
                time_str = time_to_take.strftime("%H:%M")
                with st.spinner("Scheduling..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/api/reminders/", json={
                            "user_email": rem_email,
                            "medication_name": med_name,
                            "time_to_take": time_str
                        })
                        if response.status_code == 200:
                            st.success(f"Reminder set! You will receive an email for '{med_name}' daily at {time_str}.")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Backend error: {e}")
                        
    st.markdown("---")
    if st.button("View Scheduled Reminders"):
        try:
            res = requests.get(f"{API_BASE_URL}/api/reminders/")
            if res.status_code == 200:
                rems = res.json()
                if rems:
                    for r in rems:
                        st.write(f"- **{r['time_to_take']}**: {r['medication_name']} sent to {r['user_email']}")
                else:
                    st.info("No active reminders.")
            else:
                st.error("Failed to load reminders.")
        except Exception as e:
            st.error("Error loading reminders.")
