"""
Date: 2024-04-15
Script Name: hashtag_creator.py
Author: omegazyph
Updated: 2026-01-08
Description: A utility class that processes a list of terms and ensures 
             they are correctly formatted as hashtags (starting with '#').
"""

class HashtagsCreator:
    """Class to transform and manage a list of strings into hashtag format."""

    def __init__(self, list_of_terms):
        """
        Initializes the class and processes the terms immediately.
        :param list_of_terms: A list of strings to be converted.
        """
        self.hashtags = []
        
        # Process each term to ensure it starts with a '#'
        for term in list_of_terms:
            # Handle terms incorrectly using '@' by replacing it with '#'
            if '@' in term:
                self.hashtags.append(term.replace('@', '#'))
            
            # If the term already has a '#', add it as is
            elif '#' in term:
                self.hashtags.append(term)
            
            # If no prefix exists, prepend the '#' symbol
            else:
                self.hashtags.append(f"#{term}")

    def list_hashtags(self):
        """Iterates through the processed hashtags and prints each to the console."""
        if not self.hashtags:
            print("No hashtags found.")
            return

        print("--- Generated Hashtags ---")
        for hashtag in self.hashtags:
            print(hashtag)

# --- Testing Code ---

if __name__ == "__main__":
    # Sample data containing various prefixes and plain strings
    terms_to_convert = ["@codecademy", "#python", "programming", "#strings"]
    
    # Create instance and process terms
    test_hashtags = HashtagsCreator(terms_to_convert)
    
    # Output the final results
    test_hashtags.list_hashtags()