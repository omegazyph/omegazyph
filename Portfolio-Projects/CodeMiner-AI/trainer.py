"""
Script Name: trainer.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: The "Teacher" script. This handles the training loop, 
             calculating how wrong the AI's guesses are and 
             adjusting the Neural Network to be more accurate.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from brain_nn import NeuralCodeBrain

def train_model(encoded_data, vocab_size, epochs=100):
    # 1. Initialize our Neural Network
    model = NeuralCodeBrain(vocab_size)
    
    # 2. Define the "Grading System" (Loss) and "Study Coach" (Optimizer)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print("--- Training Started ---")
    for epoch in range(epochs):
        total_loss = 0
        
        # We show the AI pairs: (Current Token, Next Token)
        for i in range(len(encoded_data) - 1):
            input_token = torch.tensor([encoded_data[i]])
            target_token = torch.tensor([encoded_data[i+1]])

            # Step A: The AI makes a guess
            optimizer.zero_grad()
            output = model(input_token)

            # Step B: Compare guess to reality (The Grade)
            loss = criterion(output, target_token)
            
            # Step C: The AI learns from the mistake
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Error Level: {total_loss/len(encoded_data):.4f}")

    print("--- Training Complete ---")
    return model

if __name__ == "__main__":
    print("This script will run once your PyTorch installation is finished.")