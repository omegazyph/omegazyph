'''
Dot String Generator 2
by Wayne Stock
Created on: 2019-03-03
Description: This script generates a pattern of dots based on the cosine of angles. It uses the `DotStringGenerator`
class to produce a series of strings where the position of a dot ('o') is determined by the cosine of an angle.
The `generate_dot_strings` method prints a specified number of these strings.
'''

# Import necessary libraries
from math import cos, radians
import sys

# Define a class for generating dot strings
class DotStringGenerator:
    def __init__(self):
        self.angle = 0  # Initialize the angle

    def make_dot_string(self):
        """
        Create a dot string based on the current angle.
        
        Returns:
        str: A string with spaces followed by a dot, where the number of spaces is determined by the cosine of the angle.
        """
        spaces = int(10 * cos(radians(self.angle)) + 10)
        return ' ' * spaces + 'o'

    def generate_dot_strings(self, num_strings):
        """
        Generate and print a series of dot strings.
        
        Args:
        num_strings (int): The number of dot strings to generate.
        """
        for _ in range(num_strings):
            dot_string = self.make_dot_string()
            print(dot_string)
            self.angle += 1  # Increment the angle for the next string

def main():
    """
    Main function to create an instance of DotStringGenerator and generate dot strings.
    """
    generator = DotStringGenerator()
    generator.generate_dot_strings(10000000)  # Generate and print dot strings

if __name__ == "__main__":
    sys.exit(int(main() or 0))  # Exit with status code 0 if successful
