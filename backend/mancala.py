from constants import DEFAULT_NAME, P1_PITS, P2_PITS, P1_STORE, P2_STORE
from board import Board
from random import randrange
import sys

class Player(object):
    def __init__(self, number=None, board=None, name=DEFAULT_NAME):
        self.name = name
        self.number = number
        self.board = board

    def __str__(self):
        return "Player: %s" % self.name

    def get_name(self):
        return self.name


class HumanPlayer(Player):
    def __init__(self, number, board, name=None):
        super(HumanPlayer, self).__init__(number, board)
        if name:
            self.name = name
        else:
            self.name = self.getHumanName()

    def getHumanName(self):
        return input("Please input your name: ")

    def getNextMove(self):
        try:
            selection = int(input("%s Please input your next move (1 to 6): " % self.name))
            if (selection < 1) or (selection > 6):
                print("Input is out of range (1 to 6)")
                sys.exit()
            return selection-1
        except ValueError:
            print("Input is not an integer")
            sys.exit()

class ComputerMinimaxPlayer(Player):
    def __init__(self, number, board, name="computer"):
        super(ComputerMinimaxPlayer, self).__init__(number, board, name)

    def evaluate(self, board):
        # Basic evaluation: difference in store counts
        return board[P1_STORE][0] - board[P2_STORE][0] if self.number == 1 else board[P2_STORE][0] - board[P1_STORE][0]

    def simulate_move(self, board, player_number, move):
        # Simulates a move and returns the new board state and whether a free move was earned
        new_board, free_move = board.makeMove(player_number, move)
        return new_board, free_move

    def minimax(self, board, depth, is_maximizing_player):
        if depth == 0 or self.checkForWinner():
            return self.evaluate(board)

        if is_maximizing_player:
            best_value = -sys.maxsize
            for move in range(6):  # Assuming 6 pits per player
                if board[self.number - 1][move] > 0:  # Only consider valid moves
                    new_board, free_move = self.simulate_move(board, self.number, move)
                    value = self.minimax(new_board, depth - 1, not free_move)
                    best_value = max(best_value, value)
            return best_value
        else:
            best_value = sys.maxsize
            opponent_number = 2 if self.number == 1 else 1
            for move in range(6):  # Assuming 6 pits per player
                if board[opponent_number - 1][move] > 0:  # Only consider valid moves
                    new_board, free_move = self.simulate_move(board, opponent_number, move)
                    value = self.minimax(new_board, depth - 1, free_move)
                    best_value = min(best_value, value)
            return best_value

    def getNextMove(self):
        best_move = None
        best_value = -sys.maxsize
        for move in range(6):
            if self.board.board[self.number - 1][move] > 0:  # Ensure the pit is not empty
                simulated_board, free_move = self.simulate_move(self.board.board, self.number, move)
                value = self.minimax(simulated_board, 3, not free_move)  # Depth set to 3 for example
                if value > best_value:
                    best_value = value
                    best_move = move
        print(f"Computer selects pit {best_move + 1}")
        return best_move

class Match(object):
    def __init__(self, player1_type=Player, player2_type=Player):
        self.board = Board()
        self.players = [player1_type(1, self.board), player2_type(2, self.board)]
        self.player1 = self.players[0]
        self.player2 = self.players[1]
        self.current_turn = self.player1

    def checkMove(self):
        print(self.board.printBoard())
        
        next_move = self.current_turn.getNextMove()
        self.board.board, free_move_earned = self.board.makeMove(self.current_turn.number, next_move)
        if self.checkForWinner():
            import sys
            sys.exit()
        if free_move_earned:
            print("Earned free move!")
            self.checkMove()
        else:
            self.swapCurrentTurn()
            self.checkMove()

    def swapCurrentTurn(self):
        if self.current_turn == self.player1:
            self.current_turn = self.player2
            return self.player2
        else:
            self.current_turn = self.player1
            return self.player1

    def checkForWinner(self):
        if set(self.board.board[P1_PITS]) == set([0]):
            self.board.board = self.board.gatherRemaining(self.player2.number)
            print("Player 1 wins! %s: %d to %s: %d\n" % (self.player1.name, self.board.board[P1_STORE][0], self.player2.name, self.board.board[P2_STORE][0]))
            return True
        elif set(self.board.board[P2_PITS]) == set([0]):
            self.board.board = self.board.gatherRemaining(self.player1.number)
            print("Player 2 wins! %s: %d to %s: %d\n" % (self.player1.name, self.board.board[P1_STORE][0], self.player2.name, self.board.board[P2_STORE][0]))
            return True
        else:
            return False
    