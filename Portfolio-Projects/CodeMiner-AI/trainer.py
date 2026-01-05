"""
Author: omegazyph
Description: This script represents the "Learning Center." 
             It creates a probability map to track how often 
             characters follow each other in programming code.
"""

import numpy as np

class PatternBrain:
    def __init__(self, vocab_size):
        # A square grid of zeros. 
        # Size is (Number of possible chars) x (Number of possible chars)
        self.matrix = np.zeros((vocab_size, vocab_size))

    def learn(self, encoded_data):
        """
        Reads the numbers and counts the patterns.
        """
        # We look at every pair of numbers in the data
        for i in range(len(encoded_data) - 1):
            current_num = encoded_data[i]
            next_num = encoded_data[i+1]
            
            # Add a 'point' to the grid for this specific pair
            self.matrix[current_num][next_num] += 1
            
        print("Learning complete. Pattern grid updated.")

    def get_probabilities(self, current_num):
        """
        Returns the AI's 'confidence' for what comes next.
        """
        row = self.matrix[current_num]
        row_sum = np.sum(row)
        
        if row_sum == 0:
            return None # The AI hasn't seen this character before
            
        # Divide the row by the sum to get percentages (0.0 to 1.0)
        return row / row_sum

# --- Let's test the "Brain" ---
if __name__ == "__main__":
    from data_loader import load_sample_data
    from tokenizer import SimpleTokenizer
    
    # 1. Setup
    text = load_sample_data()
    tk = SimpleTokenizer(text)
    encoded = tk.encode(text)
    
    # 2. Initialize Brain and Learn
    brain = PatternBrain(tk.vocab_size)
    brain.learn(encoded)
    
    # 3. Ask the brain: "What usually follows 'd'?"
    char_to_check = 'd'
    idx = tk.char_to_int[char_to_check]
    probs = brain.get_probabilities(idx)
    
    print(f"\nAI is looking at character: '{char_to_check}'")
    print(f"Probabilities for next character IDs: \n{probs}")