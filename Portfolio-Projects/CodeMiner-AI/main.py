"""
Author: omegazyph
Description: The Orchestrator. Connects the data, tokenizer, and brain 
             to generate Python code based on a user prompt.
"""

import numpy as np
from data_loader import load_sample_data
from tokenizer import SimpleTokenizer
from brain import PatternBrain

def run_ai():
    # 1. Prepare the tools
    text = load_sample_data()
    tk = SimpleTokenizer(text)
    encoded_data = tk.encode(text)
    
    # 2. Train the brain (Context size of 3)
    brain = PatternBrain(tk.vocab_size, context_size=3)
    brain.learn(encoded_data)
    
    # 3. Get input from you!
    print("\n--- CodeMiner AI Ready ---")
    prompt = input("Type the start of a function (e.g., 'def '): ")
    
    if len(prompt) < 3:
        print("Error: Please provide at least 3 characters for context.")
        return

    # 4. Generate the rest of the code
    try:
        result_ids = tk.encode(prompt)
        
        # AI generates 40 characters of code
        for _ in range(40):
            # Take the last 3 characters as context
            context = result_ids[-3:]
            probs = brain.get_probabilities(context)
            
            if probs is None:
                break # Stop if AI hits a dead end
            
            # Pick a character based on probability
            next_id = np.random.choice(len(probs), p=probs)
            result_ids.append(next_id)
            
        # 5. Show the final result
        completed_code = tk.decode(result_ids)
        print("\n--- AI Completion ---")
        print(completed_code)
        print("----------------------")
        
    except KeyError:
        print("Error: You used a character the AI hasn't learned yet!")

if __name__ == "__main__":
    run_ai()