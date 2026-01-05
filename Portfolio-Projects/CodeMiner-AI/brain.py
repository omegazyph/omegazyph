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
            return None 
            
        # Convert counts into percentages
        return row / row_sum