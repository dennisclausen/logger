#!/bin/bash
set -e  # stop on error

# optional: Python-Version prüfen
PYTHON=${PYTHON:-python3}

# virtuelles Env nur erstellen, wenn nicht vorhanden
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv .venv
else
    echo "Virtual environment already exists."
fi

# Aktivieren (nur sichtbar in interaktiver Shell)
source .venv/bin/activate

# Upgrade pip und install requirements
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Setup complete. Run 'source .venv/bin/activate' to activate environment."
