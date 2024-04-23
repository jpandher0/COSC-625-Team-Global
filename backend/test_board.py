from constants import DEFAULT_NAME, P1_PITS, P2_PITS, P1_STORE, P2_STORE
from board import Board
from unittest.mock import patch

def test_board_init_default_values():
    board = Board()
    assert board.board == [[4, 4, 4, 4, 4, 4], [0], [4, 4, 4, 4, 4, 4], [0]]

def test_board_init_with_test_state():
    custom_state = [[1, 1, 1, 1], [0], [2, 2, 2, 2], [0]]
    board = Board(test_state=custom_state)
    assert board.board == custom_state

def test_print_board():
    custom_state = [[1, 2, 3, 4, 5, 6], [0], [1, 2, 3, 4, 5, 6], [0]]
    board = Board(test_state=custom_state)
    expected_output = "   6  5  4  3  2  1\n 0                    0\n   1  2  3  4  5  6\n"
    assert board.printBoard() == expected_output

def test_makeMove():
    board = Board()
    
    # Scenario 1: Player 1 makes a move that doesn't earn a free move or capture
    board.board = [[0, 0, 0, 0, 1, 0], [0], [0, 0, 0, 0, 0, 6], [0]]
    player_num = 1
    start_index = 4
    expected_board_state = [[0, 0, 0, 0, 0, 1], [0], [0, 0, 0, 0, 0, 6], [0]]
    expected_earned_free_move = False
    
    updated_board_state, earned_free_move = board.makeMove(player_num, start_index)
    
    assert updated_board_state == expected_board_state
    assert earned_free_move == expected_earned_free_move

    # Scenario 2: Player 2 makes a move that earns a free move but not a capture
    board.board = [[0, 0, 0, 0, 0, 2], [0], [6, 0, 0, 0, 0, 0], [0]]
    player_num = 2
    start_index = 0
    expected_board_state = [[0, 0, 0, 0, 0, 2], [0], [0, 1, 1, 1, 1, 1], [1]]
    expected_earned_free_move = True
    
    updated_board_state, earned_free_move = board.makeMove(player_num, start_index)

    assert updated_board_state == expected_board_state
    assert earned_free_move == expected_earned_free_move

    # Scenario 3: Player 1 makes a move that earns a capture
    board.board = [[0, 2, 0, 0, 1, 0], [0], [7, 5, 0, 0, 0, 0], [0]]
    player_num = 1
    start_index = 4
    expected_board_state = [[0, 2, 0, 0, 0, 0], [8], [0, 5, 0, 0, 0, 0], [0]]
    expected_earned_free_move = False

    updated_board_state, earned_free_move = board.makeMove(player_num, start_index)
 
    assert updated_board_state == expected_board_state
    assert earned_free_move == expected_earned_free_move

def test_getNextArea():
    board = Board()
    assert board.getNextArea(P1_PITS) == P1_STORE
    assert board.getNextArea(P1_STORE) == P2_PITS
    assert board.getNextArea(P2_PITS) == P2_STORE
    assert board.getNextArea(P2_STORE) == P1_PITS

def test_earnedCapture():
    board = Board()
    board.board = [[0, 0, 0, 0, 1, 0], [0], [5, 0, 0, 0, 0, 0], [0]]
    last_area = P1_PITS
    last_index = 5
    player_num = 1
    assert board.earnedCapture(player_num, last_area, last_index) == True
    board.board = [[0, 0, 0, 0, 0, 2], [0], [0, 0, 0, 0, 0, 0], [0]]
    last_area = P2_PITS
    last_index = 5
    player_num = 2
    assert board.earnedCapture(player_num, last_area, last_index) == False

def test_stealStones():
    board = Board()
    last_area = P1_PITS
    last_index = 0
    expected_opposing_area = P2_PITS
    expected_opposing_index = 5
    board.stealStones(last_area, last_index)
    assert board.board[P1_STORE][0] == 5
    assert board.board[last_area][last_index] == 0
    assert board.board[expected_opposing_area][expected_opposing_index] == 0

def test_getOpposingAreaAndIndex():
    board = Board()
    assert board.getOpposingAreaAndIndex(P1_PITS, 0) == (P2_PITS, 5)
    assert board.getOpposingAreaAndIndex(P2_PITS, 0) == (P1_PITS, 5)
    assert board.getOpposingAreaAndIndex(P1_STORE, 0) == (P2_STORE, 5)
    assert board.getOpposingAreaAndIndex(P2_STORE, 0) == (P1_STORE, 5)

def test_gatherRemaining():
    board = Board()
    assert board.gatherRemaining(1)[0] == [0, 0, 0, 0, 0, 0]
    assert board.gatherRemaining(2)[2] == [0, 0, 0, 0, 0, 0]