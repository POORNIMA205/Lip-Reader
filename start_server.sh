#!/bin/bash
# Start the lip reading web app

cd "$(dirname "$0")"
source venv/bin/activate

PORT=${1:-80}

echo "Starting Lip Reading Web App..."
echo ""

if [ "$PORT" = "80" ] && [ "$EUID" -ne 0 ]; then
    echo "Port 80 requires sudo. Trying port 8080 instead..."
    echo "To use port 80, run: sudo ./start_server.sh 80"
    PORT=8080
fi

echo "Access at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python app.py $PORT

