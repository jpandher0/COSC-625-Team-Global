import numpy as np
import random
from dataclasses import dataclass
from typing import List


board = None

# Calculate the next index position, handle loop overruns
def next_idx(idx: int):
   # Calculate the next index value of the moving piece, with the handle wrapped around the end of the board
    nidx = idx + 1
    if nidx > 13:
        return 0
    return nidx

#Calculates the index of the opposite pit, which is used for the "capture" operation in the game.
def opposite_idx(idx: int):
   # Calculate the index directly relative to the given index for capturing stones
    assert idx <= 12
    return 12 - idx


@dataclass
class Rule:
   # Data classes that store the rules of the game

    # This attribute determines whether the player can wrap around the entire game board multiple times in a single action.
    # If set to True, when a player has enough stones in an action to continue distributing them again from the beginning of the board, 
    #they may continue distributing stones until they are finished in their hand. If set to False, a player's action ends when they reach the end of the board, even if there are still stones in their hand
    multi_lap: bool = True

    # This attribute determines whether a player can capture the opposite player's stone.
    # When set to True, if a player's last stone lands in their empty pit, they may capture all stones (if any) on the opposite side of this pit (the corresponding pit on their opponent's side) into their scoring area. When set to False, 
    # such capture actions are not allowed.
    capture_opposite: bool = True

    # This attribute determines whether or not a player can continue to act when he or she places the last stone in his or her scoring pit (also known as a "scoring hole" or "scoring point").
    # If set to True, when a player's last stone lands in their scoring pit, they may take another action; if set to False, the player's turn ends even if the last stone lands in the scoring pit.
    continue_on_point: bool = True


class Mancala:
    # Initialize an instance of the Karamanga game. Set the number of pits, the initial number of stones per pit, and the rules of the game.
    def __init__(self, players, pits: int = 6, initial_stones: int = 4, rule: Rule = Rule()):
        # Initialize the Mancala board with the specified pits, the initial pieces for each pit, and the rules
        self.__pits = pits
        self.__initial_stones = initial_stones
        self.rule = rule
        self.human = players[0]
        self.robot = players[1]
        self.init_board()
        num = [int(i) for i in board]
        self.human_info = num[0: len(num) // 2]
        self.robot_info = num[len(num) // 2: len(num)]
        self.hand = 0
        self.selection = [str(i) for i in range(1, self.__pits + 1)]
        # TODO
        self.turn = 0 # random.randint(0, 1)  # player: 0, ai: 1
        self.end = False
        self.winner = ""

    # Initialize the game board and set the stones on the board according to the number of pits and the initial number of stones.
    def init_board(self):
        # Initialize the board by placing initial pieces in each pit (each pit defaults to 4 pieces)
        global board
        board = np.zeros(((self.__pits + 1) * 2,), dtype=np.int)
        # Player 1 
        for i in range(0, self.__pits):
            board[i] = self.__initial_stones
        # Player 2 
        for i in range(self.__pits + 1, self.__pits * 2 + 1):
            board[i] = self.__initial_stones

    # Remove all stones from the selected pit and set that pit to empty.
    def take_pit(self, idx: int):
        # Remove all stones from a given pit, making that pit empty.
        """
        idx: Manipulated pits
        num:
        """
        # Operation Logic:
        # self.hand += self.board[idx]：
        # This line adds the number of stones in the selected pit to the self.hand variable. self.hand represents the number of stones currently in the player's hand, which is the basis for the next step in allocating stones.
        # self.board[idx] = 0：
        # This line sets the number of stones in the selected pit to 0, i.e. it empties the pit. This is because all the stones have been removed and placed in the player's hand.
        global board
        self.hand += int(board[idx])
        board[idx] = 0

    # When making a move, place the stone in the designated pit.
    def fill_pit(self, idx: int, num: int = 1):
        # Reduce the number of stones in your hand by placing them in the designated pits
        assert self.hand > 0 and num <= self.hand
        global board
        board[idx] += num
        self.hand -= int(num)

    @property
    def _player0_field_range(self):
        # Index range representing the side of player 0 on the field
        return range(0, self.__pits)

    @property
    def _player1_field_range(self):
        # Index range representing Player 1's side
        return range(self.__pits + 1, self.__pits * 2 + 1)

    @property
    def _player0_point_index(self):
        # Index to Player 0's Scoring Bag
        return self.__pits

    @property
    def _player1_point_index(self):
        # Index of Player 1's Scoring Bag
        return self.__pits * 2 + 1

    @property
    def _active_player_point_index(self):
        # Index of currently active players scoring sacks
        return (
            self._player0_point_index if self.turn == 0 else self._player1_point_index
        )

    def is_own_pointpit(self, idx: int):
        # Determine if the given index is the current player's score (score pit)
        if self.turn == 0:
            return idx == 6
        else:
            return idx == 13

    def is_own_fieldpit(self, idx: int):
        # Determine if a given index is within the current player's field (non-scoring) range
        if self.turn == 0:
            return 0 <= idx < 6
        else:
            return 7 <= idx < 13

    def render_cli(self):
        # Rendering the game board in the command line interface
        # Print top border:This line prints the top border of the board." ====" is the sequence of characters used to represent the border, repeated as many times as the number of pits plus one (plus one to include scoring pits)
        global board
        print("\n" + "====" * (self.__pits + 1))
        # AI Side
        # Rendering the AI player's piece distribution:This code first prints the number of stones in the AI player's scoring pit (located at one end of the board), then iterates through the pits controlled by the AI player, printing the number of stones in each pit from right to left (since [::-1] is a reverse iteration). end=" " Make sure to print on the same line.
        print(f"[{board[self._player1_point_index]:>2}]", end=" ")
        for i in self._player1_field_range[::-1]:
            print(f"{board[i]:>2}", end=" ")
        # Print Separator:This line prints a separator line that is used to provide a visual distinction between the AI player and the player's side.
        print("\n" + "----" * (self.__pits + 1))
        # players' side
        # Rendering the player's piece distribution:These lines of code print the player's piece distribution. It starts with a four-space offset to align with the AI player's scoring pits, then prints the number of stones in each of the player's pits from left to right, and finally prints the player's scoring pits.
        print(" " * 4, end=" ")
        for i in self._player0_field_range:
            print(f"{board[i]:>2}", end=" ")
        print(f"[{board[self._player0_point_index]:>2}]", end=" ")
        # Print Bottom Boundary: As with the top boundary, this line of code prints out the bottom boundary of the board
        print("\n" + "====" * (self.__pits + 1))

    def show_actions(self):
        # Displays the available actions for the current player
        # Print Indentation:This line of code serves to add a four-space indentation before the print operation, and the end=" " parameter ensures that subsequent prints are on the same line. This indentation can help visually distinguish between different parts of the output, making the interface more tidy.
        print(" " * 4, end=" ")
        # Loop over print operations: This loop iterates over the self.selection list, which contains the characters representing each of the optional operations. {char:>2} is a formatted string, where >2 means that each character occupies a space at least two characters wide and is right-aligned. This ensures that the output remains aligned even if the characters are of different widths. end=" " is again used to ensure that all characters are output on the same line and separated by spaces.
        for char in self.selection:
            print(f"{char:>2}", end=" ")
        print()

    def get_sided_all_actions(self):
        # Get all the possible moves of the current player according to his position on the field
        if self.turn == 0:
            return list(self._player0_field_range)
        else:
            return list(self._player1_field_range)

    def filter_available_actions(self, actions: List[int]) -> List[int]:
        # Filters out all possible actions. This method checks if there are still stones in the pit corresponding to each action, and only the index of a non-empty pit is returned.
        return [i for i in actions if board[i] > 0]

    # def get_player_action(self):
    #     # Get player actions from command line input, validate them, and handle exit actions
    #     while True:
    #         # Input Request:This line of code displays the prompt "You throw ..... >" and waits for player input. The player's input will be stored in the variable key_input.
    #         key_input = input("You throw..... > ")
    #         # Exit check:If the player enters "q", sys.exit() is called, which causes the program to exit immediately and is an emergency way to stop the program.
    #         if key_input == "q":
    #             sys.exit()
    #         # Input validation:Here an attempt is made to find the index corresponding to the player's input from self.selection (a list containing valid choices) and store it in idx. assert idx >= 0 ensures that idx is a valid index, which is usually redundant because if the key_input is not in self.selection, the . index() method will throw an exception
    #         idx = self.selection.index(key_input)
    #         assert idx >= 0
    #         # Action validity check: This line of code calls the filter_available_actions method (which returns a list of all possible, valid actions) to check if idx is a valid action. If it is, the method returns idx, indicating that the action selected by the player is valid and the program continues to execute.
    #         if idx in self.filter_available_actions(self.get_sided_all_actions()):
    #             return idx
    #         # Error Feedback:If the player selects a pit that is empty (i.e. the idx is not in the list of valid actions returned), "Cannot pick from empty pit" is printed, reminding the player that they must select a non-empty pit.
    #         else:
    #             print("Cannot pick from empty pit")

    def flip_turn(self):
        # It's another player's turn.
        self.turn = 1 if self.turn == 0 else 0
        self.judge_end_condition()

    # Perform an action and decide what to do next based on the current number of stones in hand and the rules of the game.
    def take_action(self, idx: int):
        # Performs actions according to the index of the selected pit; handles the rules of the game when moving the stone
        # Taking stones:First call the take_pit method to take all the stones from the player specified pit idx and empty that pit.
        self.take_pit(idx)
        # Initialize the continue_turn flag:Set the continue_turn flag to False.This flag is used to determine if the player can continue to the next action (if allowed by the game rules).
        continue_turn = False
        # Allocating stones:A loop is used to allocate stones on the board, pit by pit, based on the number of stones in the player's hand (self.hand). Each loop calls the next_idx function to compute the index idx of the next pit.
        for _ in range(self.hand):
            idx = next_idx(idx)
            # Determine whether or not to continue the turn: if the last stone in your hand lands in your scoring pit, and the rules of the game continue_on_point allow for continued action, then set continue_turn to True
            if (
                self.hand == 1
                and self.rule.continue_on_point
                and self.is_own_pointpit(idx)
                # I'm currently playing, but I'm out of tiles, so don't continue_turn, give it to your opponent.
                and (self.turn == 0 and not all(element == 0 for element in self.human_info[0:len(self.human_info) - 1]) or self.turn == 1 and not all(element == 0 for element in self.robot_info[0:len(self.robot_info) - 1]))
            ):
                continue_turn = True
            # Determining Whether to Capture an Opponent's Stone:If a player's last stone lands on an empty pit and there is a stone in the opposite pit (i.e., the opponent's stone can be captured), the capture action is performed, placing the stone from the opponent's pit, as well as his or her own last stone, into his or her scoring pit.
            if (
                self.hand == 1
                and self.rule.capture_opposite
                and self.is_own_fieldpit(idx)
                and board[idx] == 0
                and board[opposite_idx(idx)] > 0
            ):
                self.take_pit(opposite_idx(idx))
                self.fill_pit(self._active_player_point_index, self.hand)
                break
            # Stone Normal Distribution:If the above special condition does not hold, a stone is placed in the current pit idx.
            self.fill_pit(idx)
        # Turn Turnover:If the conditions for continuing the turn are not met (i.e. continue_turn is False or the game rules don't allow multi-lap allocation multi_lap), then the flip_turn method is called to replace the player and end the current player's turn.
        if not (continue_turn and self.rule.multi_lap):
            self.flip_turn()
        # It's the other team's turn, but they don't have a son.
        if (self.turn == 0 and all(element == 0 for element in self.human_info[0:len(self.human_info) - 1])
                or self.turn == 1 and all(element == 0 for element in self.robot_info[0:len(self.robot_info) - 1])):
            self.flip_turn()

    #Handle the action steps of the human player and the AI separately.
    def step_human(self, index: int):
        if self.end:
            return
        # Handling human player actions, prompting and taking human player actions
        self.show_actions()
        # if key_input == "q":
        #     sys.exit()
        idx = self.selection.index(str(index))
        assert idx >= 0
        if idx in self.filter_available_actions(self.get_sided_all_actions()):
            self.take_action(idx)
            num = [int(i) for i in board]
            self.human_info = num[0: len(num) // 2]
            self.robot_info = num[len(num) // 2: len(num)]
        else:
            raise Exception("Cannot pick from empty pit")
        self.judge_end_condition()

    # Handle the action steps of the human player and the AI separately.
    def step_ai(self):
        if self.end:
            return
        # Processes the actions of the AI player, randomly selecting from possible actions
        act = random.choice(self.filter_available_actions(self.get_sided_all_actions()))
        self.take_action(act)
        num = [int(i) for i in board]
        self.human_info = num[0: len(num) // 2]
        self.robot_info = num[len(num) // 2: len(num)]
        self.judge_end_condition()

    # Controls each step of the game, calling the step method according to the current turn of the player (human or AI).
    # def step(self):
    #     # Take a step forward in the game and deal with rotations between humans and artificial intelligence
    #     print("Board:", ["You", "AI"][self.turn])
    #     if self.turn == 0:
    #         self.step_human()
    #     else:
    #         self.step_ai()

    # Determine if the game is over and who the winner is.
    def judge_end_condition(self):
        # Determine if the game is over and announce the winner
        if (self.turn == 1 and all(element == 0 for element in self.robot_info[0: len(self.robot_info) - 1])
           or self.turn == 0 and all(element == 0 for element in self.human_info[0: len(self.human_info) - 1])):
            self.end = True
            human_score = self.human_info[len(self.human_info) - 1]
            robot_score = self.robot_info[len(self.robot_info) - 1]
            self.winner = 'The game ends in a tie' if human_score == robot_score else f'You ({self.human}) loss!' if human_score < robot_score else f'You ({self.human}) win!'

    #Control the entire flow of the game, from start to finish.
    # def play(self):
    #     # Controls the main game loop until the end condition is met
    #     while not self.end:
    #         self.render_cli()
    #         self.step()
    #         self.judge_end_condition()
    #     print("END GAME")
    #     self.render_cli()
