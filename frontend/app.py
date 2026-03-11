import streamlit as st
import requests
import pandas as pd
import pickle
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
st.markdown("Your AI-powered personal health monitoring assistant. Assess symptoms, log daily vitals, set medication reminders, and predict sleep disorders.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🩺 Symptom Checker",
    "📈 Vitals Logger",
    "💊 Medication Reminders",
    "😴 Sleep Disorder Predictor"
])

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
                            
                            if risk_level.lower() == "high":
                                st.error("### 🚨 Risk Level: HIGH")
                                st.warning("An emergency alert has been automatically sent to your designated family member.")
                            elif risk_level.lower() == "medium":
                                st.warning("### ⚠️ Risk Level: MEDIUM")
                            else:
                                st.success("### ✅ Risk Level: LOW")
                                
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
        time_to_take = st.text_input("Daily Reminder Time (24-hour HH:MM)", value="08:00")
        
        scheduled = st.form_submit_button("Schedule Reminder")
        
        if scheduled:
            if not med_name:
                st.error("Please enter a medication name.")
            else:
                time_str = time_to_take.strip()
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
    st.subheader("Your Scheduled Reminders")
    try:
        res = requests.get(f"{API_BASE_URL}/api/reminders/")
        if res.status_code == 200:
            rems = res.json()
            if rems:
                for r in rems:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"- **{r.get('time_to_take', '')}**: {r.get('medication_name', '')} sent to {r.get('user_email', 'Unknown')}")
                    with col2:
                        if st.button("Cancel", key=f"cancel_{r.get('id', '')}"):
                            try:
                                delete_res = requests.delete(f"{API_BASE_URL}/api/reminders/{r.get('id', '')}")
                                if delete_res.status_code == 200:
                                    st.success("Reminder cancelled!")
                                    st.rerun()
                                else:
                                    st.error("Failed to cancel reminder.")
                            except Exception as e:
                                st.error(f"Error cancelling reminder: {e}")
            else:
                st.info("No active reminders.")
        else:
            st.error("Failed to load reminders.")
    except Exception as e:
        st.error("Error loading reminders.")

# --- Tab 4: Sleep Disorder Predictor ---
with tab4:
    st.header("Sleep Disorder Predictor")
    st.info("Fill in your health and lifestyle details to predict your sleep disorder risk.")

    # --- Load Model ---
    @st.cache_resource
    def load_sleep_model():
        with open('sleep_disorder_model.pkl', 'rb') as f:
            return pickle.load(f)

    try:
        sleep_model = load_sleep_model()
        model_loaded = True
    except FileNotFoundError:
        st.error("⚠️ Model file `sleep_disorder_model.pkl` not found. Please ensure it is in the same directory as this app.")
        model_loaded = False

    if model_loaded:
        col1, col2 = st.columns(2)

        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            age_sleep = st.slider("Age", 18, 80, 30, key="sleep_age")
            sleep_duration = st.slider("Sleep Duration (hours)", 4.0, 10.0, 7.0, step=0.1)
            quality_of_sleep = st.slider("Quality of Sleep (1-10)", 1, 10, 7)
            physical_activity = st.slider("Physical Activity Level (min/day)", 0, 120, 45)
            stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)

        with col2:
            bmi_category = st.selectbox("BMI Category", ["Underweight", "Normal", "Overweight", "Obese"])
            heart_rate_sleep = st.number_input("Heart Rate (bpm)", 40, 120, 72, key="sleep_hr")
            daily_steps = st.number_input("Daily Steps", 0, 20000, 7000, step=500)
            bp_systolic = st.number_input("Blood Pressure Systolic", 80, 200, 120, key="sleep_sys")
            bp_diastolic = st.number_input("Blood Pressure Diastolic", 50, 130, 80, key="sleep_dia")

        st.divider()

        # --- Encode Inputs ---
        gender_encoded = 1 if gender == "Male" else 0
        bmi_map = {"Underweight": 0, "Normal": 1, "Overweight": 2, "Obese": 3}
        bmi_encoded = bmi_map[bmi_category]

        # --- Predict ---
        if st.button("🔍 Predict Sleep Disorder", use_container_width=True, type="primary"):
            input_data = pd.DataFrame([{
                'Gender': gender_encoded,
                'Age': age_sleep,
                'Sleep Duration': sleep_duration,
                'Quality of Sleep': quality_of_sleep,
                'Physical Activity Level': physical_activity,
                'Stress Level': stress_level,
                'BMI Category': bmi_encoded,
                'Heart Rate': heart_rate_sleep,
                'Daily Steps': daily_steps,
                'BP Systolic': bp_systolic,
                'BP Diastolic': bp_diastolic
            }])

            prediction = sleep_model.predict(input_data)[0]

            st.divider()

            if prediction == "None":
                st.success("✅ No Sleep Disorder Detected")
                st.markdown("Your sleep health looks good! Keep maintaining a healthy lifestyle.")

            elif prediction == "Insomnia":
                st.warning("⚠️ Insomnia Detected")
                st.markdown("""
                **Insomnia** means difficulty falling or staying asleep.  
                **Suggestions:**
                - Reduce stress and screen time before bed
                - Maintain a consistent sleep schedule
                - Avoid caffeine in the evening
                """)

            elif prediction == "Sleep Apnea":
                st.error("🚨 Sleep Apnea Detected")
                st.markdown("""
                **Sleep Apnea** means breathing repeatedly stops during sleep.  
                **Suggestions:**
                - Consult a doctor for proper diagnosis
                - Maintain a healthy BMI
                - Avoid sleeping on your back
                """)

            st.caption("⚠️ This is an ML prediction, not a medical diagnosis. Please consult a doctor.")

# --- Footer ---
st.divider()
st.caption("Built with Streamlit & scikit-learn | ElderCare AI © 2025")