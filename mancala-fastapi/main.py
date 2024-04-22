from typing import List
from fastapi import FastAPI, Query

from mancala import Mancala
from model import Player, MancalaStatus

app = FastAPI()
game = None


# 启动游戏
@app.post("/start")
async def start(items: List[str]):
    global game
    game = Mancala(items)
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])

    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)
    mancala = MancalaStatus("", False)

    if game.turn == 0:  # 等待玩家出手
        return {
            "players": [human, robot],
            "gameStatus": mancala
        }
    # TODO
    # game.step_ai() # AI先出手，之后将结果返回给玩家
    # game.render_cli()
    # print("Board:", ["Player", "AI"][game.turn])
    return {
        "players": [human, robot],
        "gameStatus": mancala
    }


# 玩家的移动，更新游戏状态，返回移动后的结果，比如是否轮到对方，游戏是否结束等。
@app.get("/move")
async def move(index: int):
    global game
    game.step_human(index)  # 玩家出手后将结果返回给玩家，随后前端调用status获取当前状态
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])

    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)

    return {
        "players": [human, robot],
        "gameStatus": MancalaStatus(game.winner, game.end)
    }


# 返回当前游戏的状态，包括两边的坑里有多少石子，当前轮到谁等信息
@app.get("/status")
async def status():
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])
    if game.turn == 1:
        game.step_ai()  # 将当前状态返回给前端前，AI先出手，将结果返回给玩家
        game.render_cli()
        print("Board:", ["Player", "AI"][game.turn])
    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)
    return {
        "players": [human, robot],
        "gameStatus": MancalaStatus(game.winner, game.end)
    }