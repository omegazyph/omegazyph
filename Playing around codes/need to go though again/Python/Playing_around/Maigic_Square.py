'''
Magic Square Generator
by Wayne Stock
Created on: 2019-02-25
Description: This Python program generates an odd-sized magic square. A magic square is a grid of numbers where the sums of 
the numbers in each row, each column, and both main diagonals are the same. This script fills the magic square with numbers
from 1 to n*n, where n is the size of the magic square and must be an odd number.
'''

def generate_square(n):
    """
    Generate an n x n magic square where n is an odd number.
    
    Args:
    n (int): The size of the magic square. Must be an odd number.
    
    Returns:
    None
    """
    # Initialize a 2-D array with all slots set to 0
    magic_square = [[0 for _ in range(n)] for _ in range(n)]
    
    # Initial position for the number 1
    i = n // 2
    j = n - 1

    # Fill the magic square by placing values
    num = 1
    while num <= (n * n):
        if i == -1 and j == n:  # 3rd condition
            j = n - 2
            i = 0
        else:
            # Move to the right if out of bounds
            if j == n:
                j = 0
            # Move to the bottom if out of bounds
            if i < 0:
                i = n - 1
        
        if magic_square[i][j]:  # 2nd condition
            j -= 2
            i += 1
            continue
        else:
            magic_square[i][j] = num
            num += 1

        # Move to the next position
        j += 1
        i -= 1  # 1st condition

    # Print the magic square
    print(f"Magic Square for n = {n}")
    print(f"Sum of each row or column = {n * (n * n + 1) // 2}\n")
    
    for row in magic_square:
        print(' '.join(f'{num:2d}' for num in row))

# Driver Code
# Only works when n is odd
n = 7
generate_square(n)
