#!/bin/bash
set -e

if [ ! -d "salesforce" ]; then
  echo 'Creating "salesforce"...'
  python3 -m venv salesforce
fi

source salesforce/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "Starting App..."
streamlit run app.py

# to run grand permission first by chmod +x salesforce.command