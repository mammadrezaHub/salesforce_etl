@echo off

if not exist salesforce (
  echo Creating "salesforce"...
  python -m venv salesforce
)

call salesforce\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo Starting App...
streamlit run app.py