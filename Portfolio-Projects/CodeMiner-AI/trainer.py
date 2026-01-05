"""
Script Name: trainer.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Handles the training loop. Correctly imports the brain 
             to teach it Python patterns.
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
    inputs = torch.tensor(encoded_data[:-1]).unsqueeze(0)
    targets = torch.tensor(encoded_data[1:]).unsqueeze(0)

    for epoch in range(epochs):
        optimizer.zero_grad()
        output, _ = model(inputs)
        loss = criterion(output.view(-1, vocab_size), targets.view(-1))
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Error Level: {loss.item():.4f}")

    return model