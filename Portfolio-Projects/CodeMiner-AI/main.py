"""
Author: omegazyph
Description: The Orchestrator. This script connects all the components 
             to take a "Seed" character and let the AI generate 
             a sequence of programming code.
"""

import numpy as np
from data_loader import load_sample_data
from tokenizer import SimpleTokenizer
from brain import PatternBrain

def generate_code(start_char, length=20):
    # 1. Load and Prepare
    text = load_sample_data()
    tk = SimpleTokenizer(text)
    encoded_data = tk.encode(text)
    
    # 2. Train the Brain
    brain = PatternBrain(tk.vocab_size)
    brain.learn(encoded_data)
    
    # 3. Start Generating
    current_char_text = start_char
    result = start_char
    
    print(f"\n--- AI is starting with: '{start_char}' ---")
    
    for _ in range(length):
        # Convert current char to its ID
        current_idx = tk.char_to_int[current_char_text]
        
        # Get probabilities from the brain
        probs = brain.get_probabilities(current_idx)
        
        if probs is None:
            break # Stop if the AI hits a character it doesn't know
            
        # The AI "makes a choice" based on the patterns it learned
        next_idx = np.random.choice(len(probs), p=probs)
        
        # Convert that ID back to a character
        next_char = tk.int_to_char[next_idx]
        
        result += next_char
        current_char_text = next_char
        
    return result

if __name__ == "__main__":
    # Let's ask the AI to finish a line starting with 'd' (like 'def')
    generated_text = generate_code('d', length=30)
    
    print("\n--- AI Generated Result ---")
    print(generated_text)
    print("---------------------------")