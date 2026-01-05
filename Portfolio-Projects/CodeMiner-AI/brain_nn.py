"""
Script Name: brain_nn.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: High-capacity LSTM model. Cleaned imports to resolve 
             linter 'unused' warnings.
"""

from torch import nn

class NeuralCodeBrain(nn.Module):
    def __init__(self, vocab_size):
        super(NeuralCodeBrain, self).__init__()
        # 512 neurons to prevent your Blackjack & Password scripts from mixing
        self.hidden_size = 512 
        self.num_layers = 2 
        
        self.embedding = nn.Embedding(vocab_size, 512)
        # 2 layers of LSTM help the brain 'categorize' different projects
        self.lstm = nn.LSTM(512, 512, num_layers=2, batch_first=True)
        self.fc = nn.Linear(512, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embedding(x)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out)
        return out, hidden