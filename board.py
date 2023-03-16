import random
from array import *


class Board:
    def __init__(self):
        self.init_board()

    def init_board(self):
        self.size = 3
        self.board = [[0 for j in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j] = ' '
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.current_player = random.choice([self.player_1, self.player_2])
        self.state = 'IN_PROGRESS' #states available: IN_PROGRESS, END

    def debug_print(self):
        for i in range(self.size):
            string = ""
            for j in range(self.size):
                string += self.board[i][j] + " "
            print(string + "\n")

    def make_move(self, x, y):
        # check if a figure can be placed
        if (self.board[y][x] != ' '):
            return False

        # place figure
        self.board[y][x] = self.current_player

        # check if current player wins
        for i in range(self.size):
            current_player_wins_vertical = True
            current_player_wins_horizontal = True
            for j in range(self.size):
                if self.board[i][j] != self.current_player:
                    current_player_wins_vertical = False
                if self.board[j][i] != self.current_player:
                    current_player_wins_horizontal = False
            if current_player_wins_vertical or current_player_wins_horizontal:
                self.state = 'END'
                return True

        current_player_wins_left = True
        current_player_wins_right = True
        for i in range(self.size):
            if self.board[i][i] != self.current_player:
                current_player_wins_left = False
            if self.board[i][self.size - 1 - i] != self.current_player:
                current_player_wins_right = False
        if current_player_wins_left or current_player_wins_right:
            self.state = 'END'
            return True

        # check if draw
        draw = True
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    draw = False

        if draw:
            self.state = 'DRAW'
            return True

        # change player
        if self.current_player == 'x':
            self.current_player = 'o'
        else:
            self.current_player = 'x'
        return True


