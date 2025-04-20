#!/bin/bash

# === Set constants ===
USERNAME=$(basename "$USER_HOME")
USER_HOME=$(eval echo ~${SUDO_USER:-$USER})
PROJECT_DIR="$USER_HOME/home-water-feature"
VENV_DIR="$PROJECT_DIR/venv"
START_SCRIPT="$PROJECT_DIR/start.sh"
UPDATE_SCRIPT="$PROJECT_DIR/update.sh"
SERVICE_NAME="water-feature"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
REPO_URL="https://github.com/pull3t/home-water-feature.git"

# === Ensure project directory exists ===
echo "📁 Ensuring project directory exists: $PROJECT_DIR"
if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Error: Project directory does not exist."
  exit 1
fi

# === Generate start.sh ===
echo "📝 Creating start.sh"
cat << 'EOF' > "$START_SCRIPT"
#!/bin/bash

# Set constants
USER_HOME="$USER_HOME"
PROJECT_DIR="$PROJECT_DIR"

# Navigate to user's home directory
cd "\$USER_HOME"

# Navigate to the project directory
cd "$PROJECT_DIR" || {
  echo "❌ Failed to change directory to $PROJECT_DIR"
  exit 1
}

# Activate the Python virtual environment
source venv/bin/activate || {
  echo "❌ Failed to activate virtual environment at venv/bin/activate"
  exit 1
}

# Print which virtual environment is active
echo "✅ Virtual environment: $VIRTUAL_ENV"
echo "✅ Python interpreter: $(which python3)"

# Start the Flask application
exec python3 app.py
EOF

# === Generate update.sh ===
echo "📝 Creating update.sh"
cat << EOF > "$UPDATE_SCRIPT"
#!/bin/bash

set -e  # Exit immediately on error

# === Configurable Variables ===
USER_HOME="$USER_HOME"
REPO_URL="$REPO_URL"
PROJECT_DIR="$PROJECT_DIR"
SERVICE_NAME="$SERVICE_NAME"

# === Navigate to user's home directory ===
cd "\$USER_HOME"

# === Check if the service is running and stop it ===
echo "Checking if service is running and terminate"
if systemctl is-active --quiet "\$SERVICE_NAME"; then
    echo "Stopping service: \$SERVICE_NAME"
    sudo systemctl stop "\$SERVICE_NAME"
fi

# === Remove the existing project directory ===
echo "Removing existing project directory: \$PROJECT_DIR"
rm -rf "\$PROJECT_DIR"

# === Clone the Git repository ===
echo "Cloning repository: \$REPO_URL"
git clone "\$REPO_URL" "\$PROJECT_DIR"

# === Change to the project directory ===
cd "\$PROJECT_DIR"

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

echo "✅ Setup complete."
EOF

# === Set permissions ===
chmod +x "$START_SCRIPT"
chmod +x "$UPDATE_SCRIPT"

# === Create systemd service file ===
echo "🛠️ Creating systemd service file: $SERVICE_FILE"
cat << EOF | sudo tee "$SERVICE_FILE" > /dev/null
[Unit]
Description=Raspberry Pi Home Water Feature Web App
After=network.target

[Service]
ExecStart=$START_SCRIPT
WorkingDirectory=$PROJECT_DIR
Restart=always
User=pi
Environment=FLASK_ENV=production
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# === Enable and restart service ===
echo "🔄 Reloading systemd daemon and enabling service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

# === Output usage info ===
echo ""
echo "✅ Setup complete! Use the following commands to manage the service:"
echo ""
echo "🔎 View status:       sudo systemctl status $SERVICE_NAME"
echo "📜 View logs:         journalctl -u $SERVICE_NAME -f"
echo "▶️  Start manually:   sudo systemctl start $SERVICE_NAME"
echo "⏹️  Stop manually:    sudo systemctl stop $SERVICE_NAME"
echo "🔁 Restart manually:  sudo systemctl restart $SERVICE_NAME"
