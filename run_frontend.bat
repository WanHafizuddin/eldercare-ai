@echo off
cd frontend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
echo Installing requirements...
pip install -r requirements.txt
echo Starting Streamlit app...
streamlit run app.py
pause
