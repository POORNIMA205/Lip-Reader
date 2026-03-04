#!/usr/bin/env python3
"""Wrapper to run LipCoordNet - converts video to frames first."""

import os
import sys
import subprocess
import cv2
import argparse
import shutil
import tempfile

def video_to_frames(video_path, output_dir):
    """Convert video to image frames."""
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_count += 1
    
    cap.release()
    return frame_count

def main():
    parser = argparse.ArgumentParser(description='Run LipCoordNet on video')
    parser.add_argument('video', help='Input video file')
    parser.add_argument('--model-dir', default='models/LipCoordNet', help='Model directory')
    parser.add_argument('--output', help='Output text file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video):
        print(f"Error: Video not found: {args.video}", file=sys.stderr)
        sys.exit(1)
    
    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as temp_dir:
        frames_dir = os.path.join(temp_dir, "frames")
        
        print(f"Converting video to frames...")
        frame_count = video_to_frames(args.video, frames_dir)
        
        if frame_count is None or frame_count == 0:
            print("Error: Could not extract frames from video", file=sys.stderr)
            sys.exit(1)
        
        print(f"Extracted {frame_count} frames")
        
        # Find weights file
        pretrain_dir = os.path.join(args.model_dir, "pretrain")
        weights_file = None
        if os.path.exists(pretrain_dir):
            pt_files = [f for f in os.listdir(pretrain_dir) if f.endswith('.pt')]
            if pt_files:
                weights_file = os.path.join(pretrain_dir, pt_files[0])
        
        if not weights_file:
            print(f"Error: Weights file not found", file=sys.stderr)
            sys.exit(1)
        
        weights_rel = os.path.relpath(weights_file, args.model_dir)
        
        # Run inference
        print("Running LipCoordNet inference...")
        try:
            result = subprocess.run(
                [sys.executable, "inference.py", 
                 "--input_video", frames_dir,
                 "--weights", weights_rel,
                 "--device", "cpu"],
                cwd=args.model_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            output_text = result.stdout.strip()
            
            # Extract predicted text
            if "PREDICTED TEXT:" in output_text:
                lines = output_text.split('\n')
                for i, line in enumerate(lines):
                    if "PREDICTED TEXT:" in line:
                        if i + 2 < len(lines):
                            predicted = lines[i + 2].strip()
                            break
            else:
                # Try to find the last line which might be the prediction
                predicted = output_text.split('\n')[-1].strip()
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(predicted)
                print(f"Result saved to: {args.output}")
            else:
                print("\n" + "="*60)
                print("PREDICTED TEXT:")
                print("="*60)
                print(predicted)
                print("="*60)
                
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}", file=sys.stderr)
            print(f"Output: {e.stdout}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()

