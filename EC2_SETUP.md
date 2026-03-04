# EC2 Setup Instructions

## Complete Setup Script (Recommended)

Run the complete setup script that fixes OpenCV and downloads the model:

```bash
cd ~/lipreader
# Upload fix_opencv.sh and download_model.py to the server, then:
chmod +x fix_opencv.sh
./fix_opencv.sh
```

This script will:
1. Fix OpenCV libGL.so.1 error (install headless version)
2. Download model weights from Hugging Face
3. Verify all dependencies
4. Restart the Flask app

## Individual Fixes

### Fix 1: libGL.so.1 Error

If you see this error:
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

### Option 2: Manual commands

Run these commands on your EC2 instance:

```bash
cd ~/lipreader
source venv/bin/activate

# Uninstall regular opencv-python
pip uninstall opencv-python -y

# Install headless version (no GUI dependencies)
pip install opencv-python-headless>=4.8.0

# Verify it works
python3 -c "import cv2; print(f'✓ cv2 version: {cv2.__version__}')"

# Restart Flask app
pkill -f 'python.*app.py' || true
python app.py 80 &
```

## Complete EC2 Setup

```bash
# 1. Navigate to project
cd ~/lipreader

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install/update all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify critical modules
python3 -c "
import cv2
import torch
import numpy as np
import face_alignment
import flask
print('✓ All modules imported successfully')
"

# 5. Start the web server
python app.py 80 &
```

### Fix 2: Model Weights Not Found

If you see this error:
```
Error: Weights file not found
```

**First, ensure all dependencies are installed:**
```bash
cd ~/lipreader
source venv/bin/activate
pip install -r requirements.txt
```

**Then download the model:**

```bash
# Option 1: Use the download script
python3 download_model.py

# Option 2: Manual download
python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='SilentSpeak/LipCoordNet', local_dir='models/LipCoordNet')"

# Verify weights exist
ls -lh models/LipCoordNet/pretrain/*.pt
```

### Fix 3: Missing huggingface_hub Module

If you see:
```
ModuleNotFoundError: No module named 'huggingface_hub'
```

Install dependencies:
```bash
cd ~/lipreader
source venv/bin/activate
pip install -r requirements.txt
```

## Alternative: Install System Libraries

If you prefer to use regular opencv-python:

```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
pip install opencv-python>=4.8.0
```

## Check if Server is Running

```bash
ps aux | grep "python.*app.py"
curl http://localhost:80
```

