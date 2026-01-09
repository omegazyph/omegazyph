'''
Tic Tac Toe Game
Author: Omegazyph
Created on: 2019-03-12
Updated on: 2023-10-06
Description: This script implements a Tic Tac Toe game for two players. It allows players to take turns 
making moves on a board of a given size, checks for win conditions, and handles ties. The game will continue
until a player wins or the board is full.
'''

import itertools

class TicTacToe:
    def __init__(self, size=3):
        # Initialize the game board and set up players
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.players = itertools.cycle([1, 2])  # Player 1 and Player 2
        self.current_player = next(self.players)

    def display_board(self):
        # Display the current state of the board
        for row in self.board:
            print(row)

    def make_move(self, row, col):
        # Attempt to place the current player's mark on the board
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        else:
            print("This position is occupied! Choose another.")
            return False

    def check_win(self):
        # Check if the current player has won
        def all_same(line):
            return all(cell == line[0] and cell != 0 for cell in line)

        # Check horizontal and vertical lines
        for i in range(self.size):
            if all_same(self.board[i]) or all_same([self.board[j][i] for j in range(self.size)]):
                return True

        # Check diagonals
        if all_same([self.board[i][i] for i in range(self.size)]) or all_same([self.board[i][self.size - 1 - i] for i in range(self.size)]):
            return True

        return False

    def play_game(self):
        # Main game loop
        game_won = False

        while not game_won:
            print(f"Current Player: Player {self.current_player}")
            self.display_board()

            played = False
            while not played:
                try:
                    # Get player input for move
                    column_choice = int(input("What column do you want to play? (0, 1, 2): "))
                    row_choice = int(input("What row do you want to play? (0, 1, 2): "))

                    if 0 <= column_choice < self.size and 0 <= row_choice < self.size:
                        played = self.make_move(row_choice, column_choice)
                    else:
                        print("Invalid input. Please enter a valid row and column.")

                except ValueError:
                    print("Invalid input. Please enter a valid row and column.")

            if self.check_win():
                game_won = True
                self.display_board()
                print(f"Player {self.current_player} wins!")
                break

            if all(all(cell != 0 for cell in row) for row in self.board):
                game_won = True
                self.display_board()
                print("It's a tie!")
                break

            self.current_player = next(self.players)

if __name__ == "__main__":
    play = True
    while play:
        game_size = int(input("Enter the size of the Tic Tac Toe board (e.g., 3): "))
        if game_size < 3:
            print("The board size must be at least 3.")
            continue

        tic_tac_toe = TicTacToe(game_size)
        tic_tac_toe.play_game()

        play_again = input("Play again? (y/n): ").lower()
        if play_again != "y":
            play = False
