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
            selection = int(input("%s Please input your next move (0 to 5): " % self.name))
            if (selection < 0) or (selection > 5):
                print("Input is out of range (0 to 5)")
                sys.exit()
            return selection
        except ValueError:
            print("Input is not an integer")
            sys.exit()

class ComputerRandomPlayer(Player):
    def __init__(self, number, board, name="computer"):
        super(ComputerRandomPlayer, self).__init__(number, board)

    def getNextMove(self):
        selection = randrange(0,6)
        print(selection)
        return selection

class Match(object):
    def __init__(self, player1_type=Player, player2_type=Player):
        self.board = Board()
        self.players = [player1_type(1, self.board), player2_type(2, self.board)]
        self.player1 = self.players[0]
        self.player2 = self.players[1]
        self.current_turn = self.player1

    def makeMove(self):
        print(self.board.printBoard())
        
        next_move = self.current_turn.getNextMove()
        self.board.board, free_move_earned = self.board.moveStones(self.current_turn.number, next_move)
        if self.checkForWinner():
            import sys
            sys.exit()
        if free_move_earned:
            print("Earned free move!")
            self.makeMove()
        else:
            self.swapCurrentTurn()
            self.makeMove()

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
    