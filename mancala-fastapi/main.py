from typing import List
from fastapi import FastAPI, Query

from mancala import Mancala
from model import Player, MancalaStatus

app = FastAPI()
game = None


# Launch the game
@app.post("/start")
async def start(items: List[str]):
    global game
    game = Mancala(items)
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])

    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)
    mancala = MancalaStatus("", False)

<<<<<<< HEAD
    if game.turn == 0:  # Waiting for the players to step up
=======
    if game.turn == 0:  # Waiting for players 
>>>>>>> dabc83d022d2749a68af43e74d0c0d9bbfecce7f
        return {
            "players": [human, robot],
            "gameStatus": mancala
        }
    # TODO
    # game.step_ai() # The AI strikes first and returns the result to the player afterwards
    # game.render_cli()
    # print("Board:", ["Player", "AI"][game.turn])
    return {
        "players": [human, robot],
        "gameStatus": mancala
    }


<<<<<<< HEAD
# The player's move, updating the game state and returning the result of the move, e.g. whether it's the opponent's turn or not, whether the game is over or not.
@app.get("/move")
async def move(index: int):
    global game
    game.step_human(index)  # Returns the result to the player after the player has taken a shot, followed by a front-end call to status to get the current status
=======
# Players move, updating the state of the game and returning the results of the move, such as whether it is the opponent's turn or not, whether the game is over or not, and so on.
@app.get("/move")
async def move(index: int):
    global game
    game.step_human(index)  # The player takes a shot and returns the result to the player, followed by a front-end call to status to get the current status
>>>>>>> dabc83d022d2749a68af43e74d0c0d9bbfecce7f
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])

    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)

    return {
        "players": [human, robot],
        "gameStatus": MancalaStatus(game.winner, game.end)
    }


<<<<<<< HEAD
# Returns the current state of the game, including information on how many stones are in the pits on either side and whose turn it is currently
=======
# Returns the current state of the game, including information such as how many stones are in the pits on either side and whose turn it is currently
>>>>>>> dabc83d022d2749a68af43e74d0c0d9bbfecce7f
@app.get("/status")
async def status():
    game.render_cli()
    print("Board:", ["Player", "AI"][game.turn])
    if game.turn == 1:
        game.step_ai()  # Before returning the current state to the front end, the AI strikes first and returns the result to the player
        game.render_cli()
        print("Board:", ["Player", "AI"][game.turn])
    human = Player(game.human, game.turn == 0, game.human_info)
    robot = Player(game.robot, game.turn == 1, game.robot_info)
    return {
        "players": [human, robot],
        "gameStatus": MancalaStatus(game.winner, game.end)
    }
