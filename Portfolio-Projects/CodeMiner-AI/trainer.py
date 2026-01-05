"""
Script Name: trainer.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Updated trainer for LSTM support. It feeds sequences 
             of tokens to the AI so it can learn long-term patterns 
             in Python programming.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from brain_nn import NeuralCodeBrain

def train_model(encoded_data, vocab_size, epochs=200):
    model = NeuralCodeBrain(vocab_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)

    print("--- Training LSTM Brain Started ---")
    
    # We turn the code into a "tensor" (math list) for PyTorch
    inputs = torch.tensor(encoded_data[:-1]).unsqueeze(0)
    targets = torch.tensor(encoded_data[1:]).unsqueeze(0)

    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # AI makes a guess based on the sequence
        output, _ = model(inputs)
        
        # We check the grade (loss)
        loss = criterion(output.view(-1, vocab_size), targets.view(-1))
        
        # Backpropagation: AI adjusts its weights
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Error Level: {loss.item():.4f}")

    return model