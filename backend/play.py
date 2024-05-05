from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mancala import Match, HumanPlayer, ComputerRandomPlayer
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Move(BaseModel):
    player_num: int
    start_index: int

class ResetGame(BaseModel):
    pass

match = Match(player1_type=HumanPlayer, player2_type=ComputerRandomPlayer)

@app.post('/make_move')
async def make_move(move: Move):
    player_num = move.player_num
    start_index = move.start_index

    match.board.board, earned_free_move = match.board.makeMove(player_num, start_index)

    if earned_free_move:
        return {"message": "Move executed successfully, earned free move"}
    else:
        return {"message": "Move executed successfully"}

@app.get('/get_board')
async def get_board():
    board_state = match.board.board
    return {"board": board_state}

@app.post('/reset_game')
async def reset_game():
    match.board = Board()  # Reset the board
    return {"message": "Game reset successfully"}

@app.get('/check_winner')
async def check_winner():
    winner = match.checkForWinner()
    if winner:
        return {"winner": winner}
    else:
        return {"winner": None}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # print("Welcome to Mancala!")
    # match = Match(player1_type=HumanPlayer, player2_type=ComputerRandomPlayer)
    # match.checkMove()

if __name__ == '__main__':
    main()