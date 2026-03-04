# Lip Reading Web App

A simple web application for lip reading - upload a video and get text predictions using the LipCoordNet model from Hugging Face.

## Prerequisites

### System Requirements

- **macOS** (tested) or Linux
- **Python 3.11** (Python 3.10+ required)
- **Homebrew** (for macOS) - to install system dependencies

### System Dependencies

**For macOS:**
```bash
# Install cmake (required for dlib)
brew install cmake

# Install dlib system library (optional, but recommended)
brew install dlib
```

**For Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y cmake libdlib-dev
```

## Installation

### 1. Clone or Navigate to Project

```bash
cd py
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If `dlib` installation fails, install `dlib-bin` instead:
```bash
pip install dlib-bin
```

### 4. Download Model (Automatic)

The model will be automatically downloaded from Hugging Face on first run, or you can download it manually:

```bash
# The model is automatically downloaded when you first run the app
# Or manually:
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='SilentSpeak/LipCoordNet', local_dir='models/LipCoordNet')"
```

## Usage

### Start the Web Server

**Option 1: Using the startup script (Port 8080)**
```bash
source venv/bin/activate
./start_server.sh
```

**Option 2: Using the startup script (Port 80 - requires sudo)**
```bash
sudo ./start_server.sh 80
```

**Option 3: Direct Python command**
```bash
source venv/bin/activate
python app.py 8080  # or 80 with sudo
```

### Access the Web App

Open your browser and go to:
- **http://localhost:8080** (default)
- **http://localhost:80** (if running with sudo)

### Using the Web App

1. **Upload Video**: Drag and drop a video file or click to browse
2. **Supported Formats**: MP4, AVI, MOV, MPG, MPEG, MKV, WEBM
3. **Process**: Click "Process Video" button
4. **View Results**: Predicted text will appear below
5. **Clear**: Click "Clear" button to remove video and upload a new one

### Command Line Usage

You can also use the command line directly:

```bash
source venv/bin/activate
python run_lipcoordnet.py path/to/your/video.mp4
```

## Project Structure

```
py/
├── app.py                  # Flask web server
├── run_lipcoordnet.py      # Lip reading script
├── start_server.sh         # Startup script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface
├── models/
│   └── LipCoordNet/       # Pre-trained model (auto-downloaded)
├── samples/
│   └── videos/            # Sample videos for testing
├── uploads/               # Temporary upload directory
└── results/               # Results storage
```

## Dependencies

### Summary by Category

| Category | Libraries |
|----------|-----------|
| **Deep Learning** | torch, torchvision |
| **Computer Vision** | opencv-python-headless, dlib-bin, face-alignment |
| **Numerical** | numpy |
| **Image Processing** | scikit-image, Pillow |
| **Web Framework** | flask, werkzeug, Jinja2 |
| **Text Processing** | editdistance |
| **Model Management** | huggingface_hub |
| **Utilities** | tqdm |

### Python Packages

#### Deep Learning
- **torch** (>=2.0.0) - PyTorch deep learning framework
- **torchvision** (>=0.15.0) - Computer vision utilities for PyTorch

#### Computer Vision
- **opencv-python-headless** (>=4.8.0) - Video/image processing (headless version for server environments)
- **dlib-bin** - Face detection and landmark extraction
- **face-alignment** (>=1.1.1) - Face alignment and landmark detection library

#### Numerical Computing
- **numpy** (>=1.24.0, <2.0.0) - Numerical computing library

#### Image Processing
- **scikit-image** (>=0.22.0) - Image processing algorithms
- **Pillow** (>=9.0.0) - Image manipulation library

#### Web Framework
- **flask** (>=2.0.0) - Web framework
- **werkzeug** (>=2.0.0) - WSGI utilities
- **Jinja2** (>=3.0.0) - Template engine

#### Text Processing
- **editdistance** (>=0.6.2) - String distance calculations (for WER/CER metrics)

#### Model Management
- **huggingface_hub** (>=0.16.0) - Downloading models from Hugging Face

#### Utilities
- **tqdm** (>=4.66.0) - Progress bars

### System Libraries

- **cmake** - Build system (for dlib compilation)
- **dlib** - C++ library for machine learning (optional, dlib-bin works)

## Troubleshooting

### dlib Installation Fails

If `pip install dlib` fails:
```bash
# Use pre-built binary instead
pip install dlib-bin
```

### Port 80 Permission Denied

Port 80 requires root privileges. Either:
- Use port 8080 (default): `python app.py 8080`
- Run with sudo: `sudo python app.py 80`

### Model Download Issues

If model download fails:
```bash
# Manual download
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='SilentSpeak/LipCoordNet', local_dir='models/LipCoordNet')"
```

### OpenCV libGL.so.1 Error (EC2/Linux)

If you see `ImportError: libGL.so.1: cannot open shared object file`:

**Solution 1 (Recommended):** Use opencv-python-headless (already in requirements.txt)
```bash
pip uninstall opencv-python -y
pip install opencv-python-headless>=4.8.0
```

**Solution 2:** Install system libraries
```bash
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0
```

### Video Processing Errors

- Ensure video shows a clear face/lip region
- Video should be in supported format
- Check video file is not corrupted
- Processing may take 1-5 minutes depending on video length

### Memory Issues

If you run out of memory:
- Use shorter videos
- Close other applications
- Process videos one at a time

## Performance

- **Processing Time**: 1-5 minutes per video (depending on length and hardware)
- **Accuracy**: ~1.7% WER (Word Error Rate) on GRID corpus
- **Model Size**: ~27MB (pretrained weights)
- **Supports**: CPU and GPU (CUDA)

## License

This project uses the LipCoordNet model which is licensed under MIT License.

## Credits

- **LipCoordNet Model**: [SilentSpeak/LipCoordNet](https://huggingface.co/SilentSpeak/LipCoordNet) on Hugging Face
- Based on LipNet architecture with enhanced lip landmark coordinates

## Quick Start Summary

```bash
# 1. Install system dependencies
brew install cmake  # macOS
# or: sudo apt-get install cmake  # Linux

# 2. Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Start web app
./start_server.sh

# 4. Open browser
# http://localhost:8080
```

That's it! Upload a video and get text predictions.
