"""
Author: omegazyph
Description: A Neural Network brain using PyTorch. This is the 
             foundation for a ChatGPT-style model.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class NeuralCodeBrain(nn.Module):
    def __init__(self, vocab_size, embedding_dim=32):
        super().__init__()
        # Embedding turns tokens into vectors (meaningful numbers)
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # A simple linear layer that "thinks" about the next word
        self.fc = nn.Linear(embedding_dim, vocab_size)

    def forward(self, x):
        # x is the input token
        x = self.embedding(x)
        # Predict the next token
        logits = self.fc(x)
        return logits