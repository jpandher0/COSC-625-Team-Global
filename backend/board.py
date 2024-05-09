P1_PITS = 0
P1_STORE = 1
P2_PITS = 2
P2_STORE = 3

DEFAULT_NAME = 'Player'

class Board(object):
    def __init__(self, board=[[4]*6, [0], [4]*6, [0]]):
        self.board = board

    def makeMove(self, player_num, start_index, curr_board):
        curr_board_copy = curr_board
        if player_num == 1:
            current_area = P1_PITS
            direction = -1
            # start_index = (-1*(start_index)) + 5 
        else:
            current_area = P2_PITS
            direction = 1
        stones_grabbed = curr_board[current_area][start_index]
        curr_board_copy[current_area][start_index] = 0
        index = start_index
        for stone in range(stones_grabbed):
            try:
                curr_board_copy[current_area][index + direction] += 1
                index += direction
            except IndexError:
                current_area = self.getNextArea(current_area)
                if player_num == 1 and current_area == P2_STORE:
                    current_area = self.getNextArea(current_area)
                    direction *= -1 
                    index = 0 if direction == 1 else 5
                elif player_num == 0 and current_area == P1_STORE:
                    current_area = self.getNextArea(current_area)
                    direction *= -1 
                    index = 0 if direction == 1 else 5
                elif current_area == P1_STORE or current_area == P2_STORE:
                    index = 0
                else:
                    pass
                curr_board_copy[current_area][index] += 1
        earned_free_move = True if (player_num == 1 and current_area == P1_STORE) or (player_num == 2 and current_area == P2_STORE) else False
        if self.earnedCapture(player_num, current_area, index):
            curr_board_copy = self.stealStones(current_area, index, curr_board_copy)
        return curr_board_copy, earned_free_move

    def getNextArea(self, current_area):
        if current_area == P1_PITS:
            return P1_STORE
        elif current_area == P1_STORE:
            return P2_PITS
        elif current_area == P2_PITS:
            return P2_STORE
        elif current_area == P2_STORE:
            return P1_PITS

    def earnedCapture(self, player_num, last_area, last_index):
        opposing_area, opposing_index = self.getOpposingAreaAndIndex(
            last_area, last_index)
        if (((player_num == 1 and last_area == P1_PITS) or (player_num == 2 and last_area == P2_PITS)) 
            and ((self.board[last_area][last_index] <= 1) and (self.board[opposing_area][opposing_index] != 0))):
            return True
        else:
            return False

    def stealStones(self, last_area, last_index, curr_board):
        if last_area == P1_PITS:
            destination_store = P1_STORE
        else:
            destination_store = P2_STORE
        opposing_area, opposing_index = self.getOpposingAreaAndIndex(
            last_area, last_index)
        captured_stones = curr_board[opposing_area][opposing_index]
        curr_board[last_area][last_index] = 0
        curr_board[opposing_area][opposing_index] = 0
        total_gain = captured_stones + 1
        curr_board[destination_store][0] += total_gain
        return curr_board

    def getOpposingAreaAndIndex(self, orig_area, index):
        if orig_area == P1_PITS:
            opposing_area = P2_PITS
        elif orig_area == P2_PITS:
            opposing_area = P1_PITS
        elif orig_area == P1_STORE:
            opposing_area = P2_STORE
        elif orig_area == P2_STORE:
            opposing_area = P1_STORE
        rev_index = list(range(5, -1, -1))
        opposing_index = rev_index[index]
        return opposing_area, opposing_index    

    def gatherRemaining(self, player_num, curr_board):
        if player_num == 0:
            remaining_area = P1_PITS
            destination_store = P1_STORE
        elif player_num == 1:
            remaining_area = P2_PITS
            destination_store = P2_STORE
        remaining_stones = 0
        curr_board_copy = curr_board
        for i in range(6):
            remaining_stones += curr_board[remaining_area][i]
            curr_board[remaining_area][i] = 0
        curr_board[destination_store][0] += remaining_stones
        return curr_board