import numpy as np
import random
from dataclasses import dataclass
from typing import List


board = None

#计算下一个索引位置，处理循环过界的情况
def next_idx(idx: int):
    # 计算移动棋子的下一个分度值，手柄在棋盘末端绕一圈
    nidx = idx + 1
    if nidx > 13:
        return 0
    return nidx

#计算对面口袋的索引，用于游戏中的"capture"操作。
def opposite_idx(idx: int):
    # 计算与给定索引直接相对的索引，用于捕捉石块
    assert idx <= 12
    return 12 - idx


@dataclass
class Rule:
    # 存储游戏规则的数据类

    # #这个属性决定了在一次行动中，玩家是否可以多次环绕整个游戏板。
    # 如果设为True，当玩家在一次行动中有足够的石头继续从板的开始处再次分配时，他们可以继续分配石头直到手中的石头分完。如果设为False，玩家的行动会在达到板的末端时结束，即使手中还有石头
    multi_lap: bool = True

    # 这个属性决定了玩家是否可以捕获对面玩家的石头。
    # 当设为 True，如果玩家的最后一颗石头落在自己空的口袋中，他们可以将这个口袋对面（对手一侧的对应口袋）的所有石头（如果有的话）捕获到自己的得分区。如果设为 False，则不允许此类捕获动作。
    capture_opposite: bool = True

    # 这个属性决定了玩家在自己的得分口袋（也称为“得分孔”或“得分点”）放置最后一颗石头时是否可以继续行动。
    # 如果设为 True，当玩家的最后一颗石头落在自己的得分口袋中时，他们可以再进行一次行动；如果设为 False，即使最后一颗石头落在得分口袋中，玩家的回合也会结束。
    continue_on_point: bool = True


class Mancala:
    #初始化卡拉曼加游戏的实例。设置口袋的数量、每个口袋的初始石头数以及游戏规则。
    def __init__(self, players, pockets: int = 6, initial_stones: int = 4, rule: Rule = Rule()):
        # 用指定的口袋、每个口袋的初始棋子和规则初始化Mancala棋盘
        self.__pockets = pockets
        self.__initial_stones = initial_stones
        self.rule = rule
        self.human = players[0]
        self.robot = players[1]
        self.init_board()
        num = [int(i) for i in board]
        self.human_info = num[0: len(num) // 2]
        self.robot_info = num[len(num) // 2: len(num)]
        self.hand = 0
        self.selection = [str(i) for i in range(1, self.__pockets + 1)]
        # TODO
        self.turn = 0 # random.randint(0, 1)  # player: 0, ai: 1
        self.end = False
        self.winner = ""

    #初始化游戏板，根据口袋数量和初始石头数来设置板上的石头。
    def init_board(self):
        # 初始化棋盘，在每个口袋中放入初始棋子(每个口袋默认是4颗棋子)
        global board
        board = np.zeros(((self.__pockets + 1) * 2,), dtype=np.int)
        # Player 1 方
        for i in range(0, self.__pockets):
            board[i] = self.__initial_stones
        # Player 2 方
        for i in range(self.__pockets + 1, self.__pockets * 2 + 1):
            board[i] = self.__initial_stones

    #从选定的口袋中取出所有石头，并设置该口袋为空。
    def take_pocket(self, idx: int):
        # 从指定的口袋中取出所有石头，使该口袋变空
        """
        idx: 操纵的口袋
        num:
        """
        # 操作逻辑:
        # self.hand += self.board[idx]：这一行将选定口袋中的石头数加到 self.hand 变量中。self.hand 代表玩家当前手中持有的石头数量，这是进行下一步分配石头时的基础。
        # self.board[idx] = 0：这一行将选定口袋的石头数设置为 0，即清空该口袋。这是因为所有的石头都已被取出，放入玩家的手中。
        global board
        self.hand += int(board[idx])
        board[idx] = 0

    #在进行移动时，将石头放入指定的口袋。
    def fill_pocket(self, idx: int, num: int = 1):
        # 将石块放入指定的口袋，减少手中的石块
        assert self.hand > 0 and num <= self.hand
        global board
        board[idx] += num
        self.hand -= int(num)

    @property
    def _player0_field_range(self):
        # 代表场上 0 号球员一方的指数范围
        return range(0, self.__pockets)

    @property
    def _player1_field_range(self):
        # 代表 1 号球员一方的指数范围
        return range(self.__pockets + 1, self.__pockets * 2 + 1)

    @property
    def _player0_point_index(self):
        # 0 号球员得分袋的索引
        return self.__pockets

    @property
    def _player1_point_index(self):
        # 1 号球员得分袋的索引
        return self.__pockets * 2 + 1

    @property
    def _active_player_point_index(self):
        # 当前在役球员得分袋的索引
        return (
            self._player0_point_index if self.turn == 0 else self._player1_point_index
        )

    def is_own_pointpocket(self, idx: int):
        # 确定给定索引是否是当前玩家的得分(得分口袋)
        if self.turn == 0:
            return idx == 6
        else:
            return idx == 13

    def is_own_fieldpocket(self, idx: int):
        # 确定给定索引是否在当前球员的场地（非计分）范围内
        if self.turn == 0:
            return 0 <= idx < 6
        else:
            return 7 <= idx < 13

    def render_cli(self):
        # 在命令行界面渲染游戏棋盘
        # 打印顶部边界:这一行打印出棋盘的顶部边界。"====" 是用来表示边界的字符序列，重复的次数由口袋的数量加一决定（加一是为了包括得分口袋）
        global board
        print("\n" + "====" * (self.__pockets + 1))
        # AI 方
        # 渲染 AI 玩家的棋子分布:这段代码首先打印 AI 玩家的得分口袋中的石头数量（位于棋盘的一端），然后遍历 AI 玩家控制的口袋，从右到左（因为 [::-1] 是反向迭代）打印每个口袋中的石头数量。end=" " 确保打印在同一行。
        print(f"[{board[self._player1_point_index]:>2}]", end=" ")
        for i in self._player1_field_range[::-1]:
            print(f"{board[i]:>2}", end=" ")
        #打印分隔线:这行打印一个分隔线，用来在 AI 玩家和玩家方之间提供视觉上的区分。
        print("\n" + "----" * (self.__pockets + 1))
        # 球员方
        # 渲染玩家的棋子分布:这几行代码打印玩家的棋子分布。首先用四个空格偏移，以对齐与 AI 玩家的得分口袋，然后从左到右打印玩家每个口袋中的石头数量，最后打印玩家的得分口袋。
        print(" " * 4, end=" ")
        for i in self._player0_field_range:
            print(f"{board[i]:>2}", end=" ")
        print(f"[{board[self._player0_point_index]:>2}]", end=" ")
        # 打印底部边界:和顶部边界相同，这行代码打印出棋盘的底部边界
        print("\n" + "====" * (self.__pockets + 1))

    def show_actions(self):
        # 显示当前玩家的可用操作
        # 打印缩进:这行代码的作用是在打印操作前添加四个空格的缩进，end=" " 参数确保后续打印的内容在同一行。这个缩进可以帮助视觉上区分不同的输出部分，使得界面更加整洁。
        print(" " * 4, end=" ")
        # 循环打印操作:这个循环遍历 self.selection 列表，其中包含了代表每个可选操作的字符。{char:>2} 是一个格式化字符串，>2 表示每个字符占用至少两个字符宽的空间，且右对齐。这样做确保了即使在字符宽度不一的情况下，输出也能保持对齐。end=" " 参数再次用来确保所有字符在同一行输出，并且字符之间有空格分隔。
        for char in self.selection:
            print(f"{char:>2}", end=" ")
        print()

    def get_sided_all_actions(self):
        # 根据当前棋手在场上的位置，获取其可能采取的所有行动
        if self.turn == 0:
            return list(self._player0_field_range)
        else:
            return list(self._player1_field_range)

    def filter_available_actions(self, actions: List[int]) -> List[int]:
        # 过滤出所有可能的行动。此方法检查每个行动对应的口袋中是否还有石头，只有非空口袋的索引会被返回。
        return [i for i in actions if board[i] > 0]

    # def get_player_action(self):
    #     # 从命令行输入中获取玩家操作，进行验证，并处理退出操作
    #     while True:
    #         # 输入请求:这行代码显示提示 "You throw..... > "，并等待玩家输入。玩家的输入将存储在变量 key_input 中。
    #         key_input = input("You throw..... > ")
    #         # 退出检查:如果玩家输入的是 "q"，则 sys.exit() 被调用，这将导致程序立即退出，是一种紧急停止程序的方式。
    #         if key_input == "q":
    #             sys.exit()
    #         #输入验证:这里尝试从 self.selection（一个包含有效选择的列表）中找到玩家输入对应的索引，并将其存储在 idx 中。assert idx >= 0 确保 idx 是一个有效的索引，这通常是冗余的，因为如果 key_input 不在 self.selection 中，.index() 方法会抛出一个异常
    #         idx = self.selection.index(key_input)
    #         assert idx >= 0
    #         # 行动有效性检查: 这行代码调用 filter_available_actions 方法（该方法返回所有可能的、有效的行动列表）来检查 idx 是否是一个有效的行动。如果是，该方法返回 idx，表示玩家选择的行动有效，且程序继续执行。
    #         if idx in self.filter_available_actions(self.get_sided_all_actions()):
    #             return idx
    #         # 错误反馈:如果玩家选择的口袋是空的（即 idx 不在返回的有效行动列表中），则打印 "Cannot pick from empty pocket"，提醒玩家必须选择一个非空的口袋。
    #         else:
    #             print("Cannot pick from empty pocket")

    def flip_turn(self):
        # 轮到另一位玩家
        self.turn = 1 if self.turn == 0 else 0
        self.judge_end_condition()

    #执行一个动作，根据当前的手中石头数和游戏规则来决定下一步如何操作。
    def take_action(self, idx: int):
        # 根据所选口袋的索引执行操作；在移动石子时处理游戏规则
        # 取出石头:首先调用 take_pocket 方法从玩家指定的口袋 idx 中取出所有的石头，并将该口袋清空。
        self.take_pocket(idx)
        # 初始化继续轮次的标志:设置 continue_turn 标志为 False。这个标志用来确定玩家是否可以继续下一个动作（如游戏规则允许的情况下）。
        continue_turn = False
        # 分配石头:通过一个循环，根据玩家手中的石头数量（self.hand），在棋盘上逐个口袋地分配这些石头。每次循环都调用 next_idx 函数计算下一个口袋的索引 idx。
        for _ in range(self.hand):
            idx = next_idx(idx)
            # 判断是否继续轮次:如果手中最后一颗石头落在了自己的得分口袋中，并且游戏规则 continue_on_point 允许继续行动，则设置 continue_turn 为 True
            if (
                self.hand == 1
                and self.rule.continue_on_point
                and self.is_own_pointpocket(idx)
                # 当前我在玩，但我没子了，就不要continue_turn，要让给对方
                and (self.turn == 0 and not all(element == 0 for element in self.human_info[0:len(self.human_info) - 1]) or self.turn == 1 and not all(element == 0 for element in self.robot_info[0:len(self.robot_info) - 1]))
            ):
                continue_turn = True
            #判断是否捕获对方石头:如果玩家的最后一颗石头落在一个空口袋上，并且对面口袋有石头（即可以捕获对方的石头），则执行捕获动作，将对方口袋的石头以及自己的最后一颗石头放入自己的得分口袋。
            if (
                self.hand == 1
                and self.rule.capture_opposite
                and self.is_own_fieldpocket(idx)
                and board[idx] == 0
                and board[opposite_idx(idx)] > 0
            ):
                self.take_pocket(opposite_idx(idx))
                self.fill_pocket(self._active_player_point_index, self.hand)
                break
            # 石头正常分配:如果上述特殊条件不成立，就将一颗石头放入当前的口袋 idx 中。
            self.fill_pocket(idx)
        #轮次更替:如果不满足继续轮次的条件（即 continue_turn 为 False 或游戏规则不允许多圈分配 multi_lap），则调用 flip_turn 方法更换玩家，结束当前玩家的轮次。
        if not (continue_turn and self.rule.multi_lap):
            self.flip_turn()
        # 轮到对方但是对方没子
        if (self.turn == 0 and all(element == 0 for element in self.human_info[0:len(self.human_info) - 1])
                or self.turn == 1 and all(element == 0 for element in self.robot_info[0:len(self.robot_info) - 1])):
            self.flip_turn()

    #分别处理人类玩家和AI的行动步骤。
    def step_human(self, index: int):
        if self.end:
            return
        # 处理人类玩家的操作，提示并采取人类玩家的操作
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
            raise Exception("Cannot pick from empty pocket")
        self.judge_end_condition()

    #分别处理人类玩家和AI的行动步骤。
    def step_ai(self):
        if self.end:
            return
        # 处理 AI 玩家的行动，从可能的行动中随机选择
        act = random.choice(self.filter_available_actions(self.get_sided_all_actions()))
        self.take_action(act)
        num = [int(i) for i in board]
        self.human_info = num[0: len(num) // 2]
        self.robot_info = num[len(num) // 2: len(num)]
        self.judge_end_condition()

    #控制游戏的每一步，根据当前轮到的玩家（人类或AI）调用相应的 step 方法。
    # def step(self):
    #     # 在游戏中前进一步，处理人类和人工智能之间的轮换
    #     print("Board:", ["You", "AI"][self.turn])
    #     if self.turn == 0:
    #         self.step_human()
    #     else:
    #         self.step_ai()

    #判断游戏是否结束，以及谁是赢家。
    def judge_end_condition(self):
        # 确定游戏是否结束并宣布获胜者
        if (self.turn == 1 and all(element == 0 for element in self.robot_info[0: len(self.robot_info) - 1])
           or self.turn == 0 and all(element == 0 for element in self.human_info[0: len(self.human_info) - 1])):
            self.end = True
            human_score = self.human_info[len(self.human_info) - 1]
            robot_score = self.robot_info[len(self.robot_info) - 1]
            self.winner = 'The game ends in a tie' if human_score == robot_score else f'You ({self.human}) loss!' if human_score < robot_score else f'You ({self.human}) win!'

    #控制整个游戏流程，从开始到结束。
    # def play(self):
    #     # 控制主游戏循环，直至满足结束条件
    #     while not self.end:
    #         self.render_cli()
    #         self.step()
    #         self.judge_end_condition()
    #     print("END GAME")
    #     self.render_cli()
