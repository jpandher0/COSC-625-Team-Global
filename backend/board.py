from constants import P1_PITS, P1_STORE, P2_PITS, P2_STORE

class Board(object):
    def __init__(self, pits=6, stones=4, test_state=None):
        if test_state:
            self.board = test_state
        else:
            self.board = [[stones] * pits, [0], [stones] * pits, [0]]

    def print_board(self):
        return "   %d  %d  %d  %d  %d  %d\n %d                    %d\n   %d  %d  %d  %d  %d  %d\n" % (
                       self.board[2][5], self.board[2][4], self.board[2][3],
                       self.board[2][2], self.board[2][1], self.board[2][0],
                       self.board[3][0], self.board[1][0],
                       self.board[0][0], self.board[0][1], self.board[0][2],
                       self.board[0][3], self.board[0][4], self.board[0][5])

    def _move_stones(self, player_num, start_index):
        if player_num == 1:
            current_area = P1_PITS
        else:
            current_area = P2_PITS
        stones_grabbed = self.board[current_area][start_index]
        self.board[current_area][start_index] = 0
        index = start_index

        for stone in range(stones_grabbed):
            try:
                self.board[current_area][index+1] += 1
                index += 1
            except IndexError:
                current_area = self._get_next_area(current_area)
                if player_num == 1 and current_area == P2_STORE:
                    current_area = self._get_next_area(current_area)
                elif player_num == 2 and current_area == P1_STORE:
                    current_area = self._get_next_area(current_area)
                else:
                    pass
                index = 0
                self.board[current_area][index] += 1

        if self._earned_free_move(player_num, current_area):
            earned_free_move = True
        else:
            earned_free_move = False
        if self._earned_capture(player_num, current_area, index):
            self.board = self._process_capture(current_area, index)

        return self.board, earned_free_move

    def _earned_free_move(self, player_num, last_area):
        if player_num == 1 and last_area == P1_STORE:
            print "Earned free move!"
            return True
        elif player_num == 2 and last_area == P2_STORE:
            print "Earned free move!"
            return True
        else:
            return False

    def _earned_capture(self, player_num, last_area, last_index):

        opposing_area, opposing_index = self._get_opposing_area_and_index(
            last_area, last_index)
        if player_num == 1:
            if not last_area == P1_PITS:
                return False
        elif player_num == 2:
            if not last_area == P2_PITS:
                return False
        else:
            pass
        if self.board[last_area][last_index] > 1:
            return False
        elif self.board[opposing_area][opposing_index] == 0:
            return False
        else:
            return True

    def _process_capture(self, last_area, last_index):
        if last_area == P1_PITS:
            destination_store = P1_STORE
        else:
            destination_store = P2_STORE

        opposing_area, opposing_index = self._get_opposing_area_and_index(
            last_area, last_index)

        captured_stones = self.board[opposing_area][opposing_index]
        print "%d stones captured!" % captured_stones
        self.board[last_area][last_index] = 0
        self.board[opposing_area][opposing_index] = 0
        total_gain = captured_stones + 1
        self.board[destination_store][0] += total_gain

        return self.board

    def gather_remaining(self, player_num):
        if player_num == 1:
            remaining_area = P1_PITS
            destination_store = P1_STORE
        elif player_num == 2:
            remaining_area = P2_PITS
            destination_store = P2_STORE
        else:
            raise Exception("Unknown player.")

        remaining_stones = 0
        for i in range(6):
            remaining_stones += self.board[remaining_area][i]
            self.board[remaining_area][i] = 0

        self.board[destination_store][0] += remaining_stones

        return self.board

    def _get_opposing_area_and_index(self, orig_area, index):
        from mancala import reverse_index

        if orig_area == P1_PITS:
            opposing_area = P2_PITS
        elif orig_area == P2_PITS:
            opposing_area = P1_PITS
        elif orig_area == P1_STORE:
            opposing_area = P2_STORE
        elif orig_area == P2_STORE:
            opposing_area = P1_STORE


        opposing_index = reverse_index(index)

        return opposing_area, opposing_index


    def _get_next_area(self, current_area):
        if current_area == P1_PITS:
            return P1_STORE
        elif current_area == P1_STORE:
            return P2_PITS
        elif current_area == P2_PITS:
            return P2_STORE
        elif current_area == P2_STORE:
            return P1_PITS


    def get_score(self, player_num):
        if player_num == 1:
            return self.board[1][0]
        else:
            return self.board[3][0]

    def get_scores(self):
        return (self.board[1][0], self.board[3][0])