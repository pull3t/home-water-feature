#!/bin/bash

# Set constants
USER_HOME="/home/pi"
PROJECT_DIR="$USER_HOME/home-water-feature"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="water-feature"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
START_SCRIPT="$PROJECT_DIR/start.sh"

echo "📁 Ensuring project directory exists: $PROJECT_DIR"
if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ Error: Project directory does not exist."
  exit 1
fi

echo "📝 Creating start.sh..."
cat << 'EOF' > "$START_SCRIPT"
#!/bin/bash
cd /home/pi/home-water-feature || exit 1
source venv/bin/activate
exec python3 app.py
EOF

chmod +x "$START_SCRIPT"

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

echo "🔄 Reloading systemd daemon and enabling service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo ""
echo "✅ Setup complete! Use the following commands to manage the service:"
echo ""
echo "🔎 View status:       sudo systemctl status $SERVICE_NAME"
echo "📜 View logs:         journalctl -u $SERVICE_NAME -f"
echo "▶️  Start manually:   sudo systemctl start $SERVICE_NAME"
echo "⏹️  Stop manually:    sudo systemctl stop $SERVICE_NAME"
echo "🔁 Restart manually:  sudo systemctl restart $SERVICE_NAME"
