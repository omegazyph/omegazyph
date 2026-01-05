"""
Author: omegazyph
Description: The Orchestrator upgraded for N-gram context.
"""

import numpy as np
from data_loader import load_sample_data
from tokenizer import SimpleTokenizer
from brain import PatternBrain

def generate_code(seed_text, length=50):
    text = load_sample_data()
    tk = SimpleTokenizer(text)
    encoded_data = tk.encode(text)
    
    # We set context_size=3 here
    brain = PatternBrain(tk.vocab_size, context_size=3)
    brain.learn(encoded_data)
    
    # The seed must be at least 3 chars long
    result_ids = tk.encode(seed_text)
    
    print(f"\n--- AI is completing your Python code ---")
    
    for _ in range(length):
        # Get the last 3 characters we've generated
        current_context = result_ids[-3:]
        probs = brain.get_probabilities(current_context)
        
        if probs is None:
            break
            
        next_idx = np.random.choice(len(probs), p=probs)
        result_ids.append(next_idx)
        
    return tk.decode(result_ids)

if __name__ == "__main__":
    # Give the AI a real Python start
    prompt = "def" 
    print(generate_code(prompt))