from board import Board
from random import randrange
import sys

P1_PITS = 0
P1_STORE = 1
P2_PITS = 2
P2_STORE = 3

class Player(object):
    def __init__(self, name="placeholderName"):
        self.name = name

    def __str__(self):
        return "Player: %s" % self.name

    def get_name(self):
        return self.name

class HumanPlayer(Player):
    def __init__(self, number, board, name="HUMAN_NAME"):
        super(HumanPlayer, self).__init__(number, board, name)

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

class ComputerRandomPlayer(Player):
    def __init__(self, name="COMPUTER_NAME"):
        super(ComputerRandomPlayer, self).__init__(name)

    def getNextMove(self):
        selection = randrange(0,6)
        print("computers turn")
        return selection

    def getNextMoveAI(self, board=None):
        return 0 

class Match(object):
    def __init__(self, board=None):
        if board is None:
            self.board = Board()  
        else:
            self.board = Board(board)

    def checkMove(self, player, index, curr_board):
        if index == 10:
            index = computer_player.getNextMove()
        elif index == 100:
            index = computer_player.getNextMoveAI()
        print("index")
        print(index)
        updated_board, earned_free_move = self.board.makeMove(player, index, curr_board)
        is_game_over, updated_board = self.checkForWinner(player, updated_board)
        print("UPDATED BOARD")
        print(updated_board)
        return updated_board, earned_free_move, is_game_over 

    def checkForWinner(self, player, curr_board):
        if set(curr_board[P1_PITS]) == set([0]):
            curr_board = self.board.gatherRemaining(player, curr_board)
            return True, curr_board
        elif set(curr_board[P2_PITS]) == set([0]):
            curr_board = self.board.gatherRemaining(player, curr_board)
            return True, curr_board
        else:
            return False, curr_board
    
computer_player = ComputerRandomPlayer()
