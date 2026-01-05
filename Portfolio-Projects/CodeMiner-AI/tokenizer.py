"""
Script Name: tokenizer.py
Author: omegazyph
Created: 2026-01-05
Last Updated: 2026-01-05
Description: High-precision character tokenizer. Captures every 
             single symbol (+, %, =, :) without exception.
"""

class WordTokenizer: 
    def __init__(self, text):
        # We use set() to find every unique character, including symbols
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        
        # Mapping every character to a unique ID
        self.char_to_int = {ch: i for i, ch in enumerate(self.chars)}
        self.int_to_char = {i: ch for i, ch in enumerate(self.chars)}

    def encode(self, text):
        # The 'if ch in' ensures we don't crash if a new char appears
        return [self.char_to_int[ch] for ch in text if ch in self.char_to_int]

    def decode(self, ids):
        # Joins the characters back together exactly as they were
        return "".join([self.int_to_char[i] for i in ids])