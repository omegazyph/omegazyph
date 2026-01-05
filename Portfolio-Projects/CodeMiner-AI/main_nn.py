"""
Script Name: brain_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: Upgraded Neural Network using LSTM. Cleaned imports 
             by removing the redundant 'import torch' to satisfy 
             the VS Code linter.
"""

import torch.nn as nn

class NeuralCodeBrain(nn.Module):
    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=128):
        super(NeuralCodeBrain, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        # x is the sequence of tokens
        x = self.embedding(x)
        output, hidden = self.lstm(x, hidden)
        logits = self.fc(output)
        return logits, hidden