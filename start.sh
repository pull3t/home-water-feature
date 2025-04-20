#!/bin/bash

# Set constants
USER_HOME="/home/pi"
PROJECT_DIR="$USER_HOME/home-water-feature"

# Navigate to the project directory
cd "$PROJECT_DIR" || {
  echo "❌ Failed to change directory to /home/<user>/home-water-feature"
  exit 1
}

# Activate the Python virtual environment
source venv/bin/activate || {
  echo "❌ Failed to activate virtual environment at venv/bin/activate"
  exit 1
}

# Start the Flask application
exec python3 app.py