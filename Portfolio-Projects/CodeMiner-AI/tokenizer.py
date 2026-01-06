"""
Author: omegazyph
Description: The "Eyes" of the AI. This script converts raw text code 
             into numerical data so the AI can perform mathematical 
             pattern recognition.
"""

class SimpleTokenizer:
    def __init__(self, text):
        # Create a list of every unique character found in the code
        # We use set() to remove duplicates and sorted() for consistency
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        
        # Create a dictionary to translate: Character -> Number
        self.char_to_int = { ch:i for i,ch in enumerate(self.chars) }
        
        # Create a dictionary to translate: Number -> Character
        self.int_to_char = { i:ch for i,ch in enumerate(self.chars) }

    def encode(self, text):
        """Converts a string of code into a list of integers."""
        return [self.char_to_int[c] for c in text]

    def decode(self, integers):
        """Converts a list of integers back into a string of code."""
        return "".join([self.int_to_char[i] for i in integers])

# --- Let's test it code-by-code ---
if __name__ == "__main__":
    from data_loader import load_sample_data
    
    # 1. Get our raw code
    raw_text = load_sample_data()
    
    # 2. Initialize the tokenizer
    tokenizer = SimpleTokenizer(raw_text)
    
    # 3. Test: Turn a small snippet of code into numbers
    test_snippet = "def"
    encoded_snippet = tokenizer.encode(test_snippet)
    
    print(f"Vocabulary Size: {tokenizer.vocab_size} unique characters")
    print(f"Original Text: '{test_snippet}'")
    print(f"Encoded (AI Version): {encoded_snippet}")
    print(f"Decoded (Back to Human): '{tokenizer.decode(encoded_snippet)}'")