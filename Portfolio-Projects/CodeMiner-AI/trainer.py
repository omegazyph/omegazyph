"""
Script Name: trainer.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Enhanced trainer with a TQDM progress bar for real-time 
             tracking of the 1000-epoch training session.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm # The progress bar library
from brain_nn import NeuralCodeBrain

def train_model(encoded_data, vocab_size, epochs=1000):
    model = NeuralCodeBrain(vocab_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001) # Lower LR for the bigger brain

    inputs = torch.tensor(encoded_data[:-1]).unsqueeze(0)
    targets = torch.tensor(encoded_data[1:]).unsqueeze(0)

    print(f"--- Training Deep LSTM Brain ({epochs} Epochs) ---")
    
    # We wrap the loop in tqdm for the progress bar
    pbar = tqdm(range(epochs), desc="Learning Progress", unit="epoch")
    
    for epoch in pbar:
        optimizer.zero_grad()
        output, _ = model(inputs)
        
        loss = criterion(output.view(-1, vocab_size), targets.view(-1))
        loss.backward()
        optimizer.step()

        # Update the progress bar with the current error level
        if (epoch + 1) % 10 == 0:
            pbar.set_postfix({"Error": f"{loss.item():.4f}"})

    return model