#!/bin/bash

set -e  # Exit immediately on error

# === Configurable Variables ===
USER_HOME="/home/pi"
REPO_URL="https://github.com/pull3t/home-water-feature.git"
PROJECT_DIR="/home-water-feature"
SERVICE_NAME="water-feature"

# === Navigate to user's home directory ===
cd "$USER_HOME"

# === Check if the service is running and stop it ===
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping service: $SERVICE_NAME"
    sudo systemctl stop "$SERVICE_NAME"
fi

# === Remove the existing project directory ===
echo "Removing existing project directory: $PROJECT_DIR"
rm -rf "$PROJECT_DIR"

# === Clone the Git repository ===
echo "Cloning repository: $REPO_URL"
git clone "$REPO_URL" "$PROJECT_DIR"

# === Change to the project directory ===
cd "$PROJECT_DIR"

# === Create a virtual environment ===
echo "Creating virtual environment..."
python3 -m venv venv

# === Activate the virtual environment ===
echo "Activating virtual environment..."
source venv/bin/activate

# === Install dependencies ===
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete."
