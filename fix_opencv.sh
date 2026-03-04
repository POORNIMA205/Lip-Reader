#!/bin/bash
# Complete EC2 setup script - fixes OpenCV and downloads model
# Run this on your EC2 server via Remote SSH

set -e

echo "=========================================="
echo "EC2 Setup: Fixing OpenCV and Model"
echo "=========================================="

cd ~/lipreader || { echo "Error: lipreader directory not found"; exit 1; }

# Activate virtual environment
source venv/bin/activate || { echo "Error: venv not found"; exit 1; }

echo ""
echo "Step 1: Fixing OpenCV libGL.so.1 error..."
echo "------------------------------------------"
pip uninstall -y opencv-python opencv-contrib-python 2>/dev/null || true
pip install opencv-python-headless>=4.8.0

echo ""
echo "Step 2: Verifying OpenCV..."
python3 -c "import cv2; print(f'✓ cv2 version: {cv2.__version__}')" || { 
    echo "✗ cv2 still not working"; 
    exit 1; 
}

echo ""
echo "Step 3: Installing/updating all dependencies..."
echo "------------------------------------------"
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Step 4: Checking model weights..."
echo "------------------------------------------"
PRETRAIN_DIR="models/LipCoordNet/pretrain"
if [ -d "$PRETRAIN_DIR" ] && [ -n "$(ls -A $PRETRAIN_DIR/*.pt 2>/dev/null)" ]; then
    echo "✓ Model weights already exist"
    ls -lh $PRETRAIN_DIR/*.pt | head -1
else
    echo "⚠ Model weights not found. Downloading..."
    python3 download_model.py || {
        echo "✗ Model download failed, trying manual download..."
        python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='SilentSpeak/LipCoordNet', local_dir='models/LipCoordNet')" || {
            echo "✗ Manual download also failed"
            echo "  Please check your internet connection and try again"
            exit 1
        }
    }
    echo "✓ Model downloaded successfully"
fi

echo ""
echo "Step 5: Verifying all dependencies..."
echo "------------------------------------------"
python3 -c "
import sys
modules = ['cv2', 'torch', 'numpy', 'face_alignment', 'flask']
for m in modules:
    try:
        __import__(m)
        print(f'✓ {m}')
    except ImportError:
        print(f'✗ {m} NOT installed')
        sys.exit(1)
"

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "Restarting Flask app..."
pkill -f 'python.*app.py' || true
sleep 2
cd ~/lipreader && source venv/bin/activate && nohup python app.py 80 > app.log 2>&1 &
echo "✓ Flask app restarted"
echo ""
echo "Check status:"
echo "  tail -f ~/lipreader/app.log"
echo "  ps aux | grep 'python.*app.py'"

