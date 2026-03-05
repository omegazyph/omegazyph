'''
Dot Pattern Generator
Author: Omegazyph
Created on: 2017-12-10
Description: This script generates a pattern of dots based on the cosine of angles ranging from 0 to 10,000,000 degrees.
The `make_dot_string` function calculates the horizontal position of the dot, and the `main` function prints the pattern
for a range of angles. Note: Printing 10,000,000 lines can be very resource-intensive.
'''

from math import cos, radians
import sys

def make_dot_string(angle):
    """
    Generate a string with a dot ('o') positioned based on the cosine of the angle.
    
    Args:
    angle (int): The angle in degrees.
    
    Returns:
    str: A string with spaces followed by a dot, where the number of spaces is determined by the cosine of the angle.
    """
    position = int(10 * cos(radians(angle)) + 10)
    return ' ' * position + 'o'

# Test assertions to verify function output
assert make_dot_string(90) == '          o'
assert make_dot_string(180) == 'o'

def main():
    """
    Generate and print a dot pattern for angles from 0 to 10,000,000.
    """
    for angle in range(10000000):
        print(make_dot_string(angle))

if __name__ == "__main__":
    # Run the main function and exit with a status code of 0 if successful
    sys.exit(main() or 0)
