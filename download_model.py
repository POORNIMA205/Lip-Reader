#!/usr/bin/env python3
"""Download LipCoordNet model from Hugging Face."""

import os
import sys
from huggingface_hub import snapshot_download

def main():
    model_dir = os.path.join(os.path.dirname(__file__), 'models', 'LipCoordNet')
    
    print("Downloading LipCoordNet model from Hugging Face...")
    print(f"Target directory: {model_dir}")
    
    try:
        snapshot_download(
            repo_id='SilentSpeak/LipCoordNet',
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        print("\n✓ Model downloaded successfully!")
        
        # Check for weights file
        pretrain_dir = os.path.join(model_dir, 'pretrain')
        if os.path.exists(pretrain_dir):
            pt_files = [f for f in os.listdir(pretrain_dir) if f.endswith('.pt')]
            if pt_files:
                print(f"✓ Found weights file: {pt_files[0]}")
            else:
                print("⚠ Warning: No .pt files found in pretrain directory")
        else:
            print("⚠ Warning: pretrain directory not found")
            
    except Exception as e:
        print(f"\n✗ Error downloading model: {e}")
        print("\nAlternative: Download manually from:")
        print("https://huggingface.co/SilentSpeak/LipCoordNet")
        sys.exit(1)

if __name__ == '__main__':
    main()

