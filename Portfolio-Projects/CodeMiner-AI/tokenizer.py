"""
Author: omegazyph
Description: Upgraded Tokenizer that breaks Python code into words 
             instead of characters. This is the first step toward 
             Large Language Model (LLM) logic.
"""

import re

class WordTokenizer:
    def __init__(self, text):
        # This regex splits by spaces and symbols but keeps the symbols
        self.tokens = re.findall(r"[\w']+|[.,!?;:()\[\]{}]|\s+", text)
        self.vocab = sorted(list(set(self.tokens)))
        self.vocab_size = len(self.vocab)
        
        self.token_to_int = { t:i for i,t in enumerate(self.vocab) }
        self.int_to_token = { i:t for i,t in enumerate(self.vocab) }

    def encode(self, text):
        # Find all words/symbols in the input
        input_tokens = re.findall(r"[\w']+|[.,!?;:()\[\]{}]|\s+", text)
        return [self.token_to_int[t] for t in input_tokens if t in self.token_to_int]

    def decode(self, integers):
        return "".join([self.int_to_token[i] for i in integers])

if __name__ == "__main__":
    sample = "def hello():"
    tk = WordTokenizer(sample)
    encoded = tk.encode(sample)
    print(f"Tokens found: {tk.tokens}")
    print(f"Encoded: {encoded}")