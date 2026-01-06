"""
Author: omegazyph
Description: This is the very first step. It loads the "Knowledge Base" 
             (raw programming code) that our AI will use to learn 
             how to program.
"""

def load_sample_data():
    # This is a small "Universe" of code for our AI to study.
    # In the future, this could be a whole .py file.
    knowledge = """
def greet():
    print("hello")

def add(a, b):
    return a + b
    
for i in range(5):
    greet()
"""
    return knowledge

if __name__ == "__main__":
    # Test if we can see our data
    raw_code = load_sample_data()
    print("--- AI Knowledge Base Loaded ---")
    print(raw_code)
    print(f"Total characters to learn from: {len(raw_code)}")