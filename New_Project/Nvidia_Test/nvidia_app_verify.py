"""
Date: 2026-01-05
Script Name: nvidia_app_verify.py
Author: omegazyph
Updated: 2026-01-05
Description: Verifies that the RTX 3050 Ti is fully recognized after updating via the NVIDIA app.
"""

import torch

def final_check():
    print("--- NVIDIA App Driver Verification ---")
    
    # Check if the software sees the driver update
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        
        print(f"✅ SUCCESS: {gpu_name} is active.")
        print(f"📊 Total VRAM: {vram:.2f} GB")
        
        # Run a small tensor calculation to prove it's working
        a = torch.ones(3, 3).cuda()
        b = a * 2
        print(f"🚀 AI Math Test: {b[0,0].item()} (Success!)")
    else:
        print("❌ Still not detected.")
        print("Tip: If the app says 'Up to date' but this fails, restart your laptop.")
    
    print("---------------------------------------")

if __name__ == "__main__":
    final_check()