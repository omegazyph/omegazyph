"""
Script Name: brain_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Upgraded Neural Network using LSTM (Long Short-Term Memory). 
             This allows the AI to remember Python syntax (like open 
             parentheses) across multiple lines of code.
"""

import torch
import torch.nn as nn

class NeuralCodeBrain(nn.Module):
    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128):
        super(NeuralCodeBrain, self).__init__()
        # Embedding: Converts word IDs into math vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # LSTM: The memory engine that tracks the sequence of Python code
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        
        # FC (Fully Connected): The final layer that picks the next word
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        # x is the input sequence of tokens
        embedded = self.embedding(x)
        
        # Pass through memory cells
        # output = the 'thoughts' for each word
        # hidden = the 'memory' to keep for the next word
        output, hidden = self.lstm(embedded, hidden)
        
        # Map the thoughts to our vocabulary (words)
        logits = self.fc(output)
        return logits, hidden