from fastapi import FastAPI, HTTPException
from typing import List
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
    curr_board: List[List[int]]

# match = Match(player1_type=HumanPlayer, player2_type=ComputerRandomPlayer)

@app.post('/make_move')
async def make_move(move: Move):
    player_num = move.player_num
    start_index = move.start_index
    curr_board = move.curr_board
    match = Match(curr_board)
    # # Make the move on the board
    # match.board.board, earned_free_move = match.board.makeMove(player_num, start_index)
    # # Return the updated board state
    board, earned_free_move, is_game_over = match.checkMove(player_num, start_index, curr_board)
    return {"board": board, "earned_free_move": earned_free_move, "is_game_over": is_game_over}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()