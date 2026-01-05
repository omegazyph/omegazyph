"""
Script Name: main_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Master script for LSTM-powered AI. This version is 
             fully optimized for Ruff/Linter standards.
"""

import torch
import torch.nn.functional as F
import os
from data_loader import load_sample_data
from tokenizer import WordTokenizer
from trainer import train_model
from brain_nn import NeuralCodeBrain

def run_chat_mode():
    text = load_sample_data()
    tk = WordTokenizer(text)
    encoded = tk.encode(text)
    
    model_path = "python_brain.pth"
    model = NeuralCodeBrain(tk.vocab_size)
    
    if os.path.exists(model_path):
        print(f"--- Loading Memory Brain from {model_path} ---")
        model.load_state_dict(torch.load(model_path))
    else:
        model = train_model(encoded, tk.vocab_size, epochs=200)
        torch.save(model.state_dict(), model_path)

    model.eval()

    print("\n--- CodeMiner-AI: No Guidelines Mode ---")
    print("(Type 'exit' to quit)")

    while True:
        prompt = input("\nEnter Python prompt: ")
        if prompt.lower() == 'exit':
            break
        
        try:
            input_ids = tk.encode(prompt)
            if not input_ids:
                continue

            input_tensor = torch.tensor([input_ids])
            generated_ids = input_ids[:]
            hidden = None
            
            with torch.no_grad():
                logits, hidden = model(input_tensor, hidden)
                
                for _ in range(40):
                    last_logit = logits[:, -1, :] / 0.8
                    probs = F.softmax(last_logit, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)
                    
                    generated_ids.append(next_token.item())
                    logits, hidden = model(next_token, hidden)

            print("\n--- AI Suggestion ---")
            print(tk.decode(generated_ids))
            
        except Exception:
            # Removed 'as e' because it wasn't being used
            print("I don't recognize one of those characters yet!")

if __name__ == "__main__":
    run_chat_mode()