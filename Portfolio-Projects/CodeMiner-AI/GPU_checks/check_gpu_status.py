"""
Date: 2026-01-05
Script Name: check_gpu_status.py
Author: omegazyph
Updated: 2026-01-05
Description: This script checks for available NVIDIA GPUs and provides basic device info.
"""

import torch

def main():
    # Check if a CUDA-enabled GPU is available
    is_available = torch.cuda.is_available()
    
    print("--- GPU Status Report ---")
    if is_available:
        # Get the name of the GPU (e.g., NVIDIA GeForce RTX 4090)
        gpu_name = torch.cuda.get_device_name(0)
        gpu_count = torch.cuda.device_count()
        print("Status: GPU Found!")
        print(f"Device Name: {gpu_name}")
        print(f"Number of GPUs: {gpu_count}")
    else:
        print("Status: No GPU detected. Running on CPU.")
    print("-------------------------")

if __name__ == "__main__":
    main()