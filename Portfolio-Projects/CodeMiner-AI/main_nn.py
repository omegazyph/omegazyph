"""
Script Name: main_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Master script for Neural Network version. Includes logic 
             to save the model's memory to a .pth file after training.
"""

import torch
import torch.nn.functional as F
import os
from data_loader import load_sample_data
from tokenizer import WordTokenizer
from trainer import train_model
from brain_nn import NeuralCodeBrain

def run_neural_ai():
    # 1. Setup Data and Tokenizer
    text = load_sample_data()
    tk = WordTokenizer(text)
    encoded = tk.encode(text)
    
    # 2. Check if we already have a saved brain
    model_path = "python_brain.pth"
    model = NeuralCodeBrain(tk.vocab_size)
    
    if os.path.exists(model_path):
        print(f"--- Loading existing brain from {model_path} ---")
        model.load_state_dict(torch.load(model_path))
    else:
        # Train and then save
        print("--- No saved brain found. Starting school... ---")
        model = train_model(encoded, tk.vocab_size, epochs=100)
        torch.save(model.state_dict(), model_path)
        print(f"--- Brain saved to {model_path} ---")

    model.eval()

    # 3. Generate Code
    prompt = "def "
    print(f"\n--- AI is generating Python based on: '{prompt}' ---")
    
    current_tokens = tk.encode(prompt)
    generated_ids = current_tokens[:]

    with torch.no_grad():
        for _ in range(30):
            input_tensor = torch.tensor([generated_ids[-1]])
            logits = model(input_tensor)
            
            # Apply a little temperature for "No Guidelines" creativity
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1).item()
            
            generated_ids.append(next_token)

    print("\n--- Final Python Result ---")
    print(tk.decode(generated_ids))

if __name__ == "__main__":
    run_neural_ai()