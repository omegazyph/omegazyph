"""
Author: omegazyph
Description: Upgraded Brain. Instead of looking at 1 character, 
             this model looks at a "Context" (N characters) to 
             better understand Python syntax and structure.
"""

import numpy as np

class PatternBrain:
    def __init__(self, vocab_size, context_size=3):
        # context_size=3 means the AI looks at the last 3 characters to guess the 4th
        self.context_size = context_size
        self.matrix = {} 
        self.vocab_size = vocab_size

    def learn(self, encoded_data):
        """
        Reads the numbers and remembers what follows specific sequences.
        """
        for i in range(len(encoded_data) - self.context_size):
            # Take a "window" of characters (e.g., ['d', 'e', 'f'])
            context = tuple(encoded_data[i : i + self.context_size])
            next_char = encoded_data[i + self.context_size]
            
            if context not in self.matrix:
                # Create a list of zeros for every possible next character
                self.matrix[context] = np.zeros(self.vocab_size)
            
            self.matrix[context][next_char] += 1
            
        print(f"Learning complete. AI now understands {len(self.matrix)} Python patterns.")

    def get_probabilities(self, context_sequence):
        """
        Looks at the last few characters and returns the probability of the next one.
        """
        context = tuple(context_sequence[-self.context_size:])
        
        if context not in self.matrix:
            return None
            
        row = self.matrix[context]
        row_sum = np.sum(row)
        return row / row_sum