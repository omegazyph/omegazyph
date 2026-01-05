"""
Script Name: main_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Master script for LSTM-powered AI. Handles training 
             and stateful generation for better Python code logic.
"""

import torch
import torch.nn.functional as F
import os
from data_loader import load_sample_data
from tokenizer import WordTokenizer
from trainer import train_model
from brain_nn import NeuralCodeBrain

def run_neural_ai():
    text = load_sample_data()
    tk = WordTokenizer(text)
    encoded = tk.encode(text)
    
    model_path = "python_brain.pth"
    model = NeuralCodeBrain(tk.vocab_size)
    
    # Check if we should load or train
    if os.path.exists(model_path):
        print(f"--- Loading Memory Brain from {model_path} ---")
        model.load_state_dict(torch.load(model_path))
    else:
        model = train_model(encoded, tk.vocab_size, epochs=200)
        torch.save(model.state_dict(), model_path)
        print(f"--- Brain saved to {model_path} ---")

    model.eval()

    # STARTING THE AI
    prompt = "def "
    print(f"\n--- AI is thinking with Memory: '{prompt}' ---")
    
    input_ids = tk.encode(prompt)
    generated_ids = input_ids[:]
    hidden = None # This will hold the AI's "short-term memory"
    
    # Prepare the initial memory
    input_tensor = torch.tensor([input_ids])
    with torch.no_grad():
        logits, hidden = model(input_tensor, hidden)
        
        for _ in range(40):
            last_logit = logits[:, -1, :]
            probs = F.softmax(last_logit, dim=-1)
            
            # This makes the choice (unfiltered/creative)
            next_token = torch.multinomial(probs, num_samples=1)
            
            generated_ids.append(next_token.item())
            
            # Feed the choice AND the memory back into the AI
            logits, hidden = model(next_token, hidden)

    print("\n--- Final Python Result (LSTM) ---")
    print(tk.decode(generated_ids))

if __name__ == "__main__":
    run_neural_ai()