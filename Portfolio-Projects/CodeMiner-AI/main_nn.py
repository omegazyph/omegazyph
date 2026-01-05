"""
Script Name: main_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Master script for LSTM-powered AI. Hard-coded to 1000 
             epochs for character-level precision.
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
    # Ensure this is the character-level tokenizer we updated
    tk = WordTokenizer(text)
    encoded = tk.encode(text)
    
    model_path = "python_brain.pth"
    model = NeuralCodeBrain(tk.vocab_size)
    
    if os.path.exists(model_path):
        print("--- Loading Memory Brain ---")
        model.load_state_dict(torch.load(model_path, weights_only=True))
    else:
        # FORCE 1000 EPOCHS HERE
        model = train_model(encoded, tk.vocab_size, epochs=1000)
        torch.save(model.state_dict(), model_path)

    model.eval()
    print("\n--- CodeMiner-AI: Ready ---")
    print("(Type 'exit' to quit)")

    while True:
        prompt = input("\nEnter Python prompt: ")
        if prompt.lower() == 'exit':
            break
        
        input_ids = tk.encode(prompt)
        if not input_ids:
            continue

        input_tensor = torch.tensor([input_ids])
        generated_ids = input_ids[:]
        hidden = None
        
        with torch.no_grad():
            logits, hidden = model(input_tensor, hidden)
            
            # Since we are using characters, we need to generate MORE 
            # (150 chars instead of 50 words)
            for _ in range(150):
                last_logit = logits[:, -1, :] / 0.8
                probs = F.softmax(last_logit, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                
                token_id = next_token.item()
                generated_ids.append(token_id)
                logits, hidden = model(next_token, hidden)

        print("\n--- AI Result ---")
        print(tk.decode(generated_ids))

if __name__ == "__main__":
    run_chat_mode()