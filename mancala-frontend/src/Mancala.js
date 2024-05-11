import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./App.css";
import axios from "axios";

function MancalaBoard() {
  const [computerPits, setComputerPits] = useState([4, 4, 4, 4, 4, 4]);
  const [humanPits, setHumanPits] = useState([4, 4, 4, 4, 4, 4]);
  const [computerStore, setComputerStore] = useState([0]);
  const [humanStore, setHumanStore] = useState([0]);
  const [currentPlayer, setCurrentPlayer] = useState(0);
  const [isComputersTurn, setIsComputersTurn] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [earnedFreeMove, setEarnedFreeMove] = useState(false);
  const [earnedCapture, setEarnedCapture] = useState(false);
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const name = params.get("name");
  const computerPlayer = params.get("computerPlayer");
  const navigate = useNavigate();

  const winLoss = () => {
    navigate(
      `/winLoss?computerScore=${computerStore}&humanScore=${humanStore}`
    );
  };

  useEffect(() => {
    if (currentPlayer === 1) {
      setIsComputersTurn(true);
      setTimeout(() => {
        makeComputerMove();
      }, 5000);
    }
  }, [currentPlayer]);

  useEffect(() => {
    if (currentPlayer === 1 && earnedFreeMove) {
      makeComputerMove();
    }
  }, [currentPlayer, earnedFreeMove]);

  useEffect(() => {
    if (gameOver) {
      console.log("isgameover");
      console.log(computerStore);
      console.log(humanStore);
      winLoss();
    }
  }, [gameOver]);

  const makeComputerMove = () => {
    if (computerPlayer === "AI") {
      makeMove(100);
    } else {
      makeMove(10);
    }
    setIsComputersTurn(false);
  };

  const makeMove = (pitIndex) => {
    const moveData = {
      player_num: currentPlayer,
      start_index: pitIndex,
      curr_board: [computerPits, computerStore, humanPits, humanStore],
    };
    console.log(moveData);
    axios
      .post("http://localhost:8000/make_move", moveData)
      .then((response) => {
        console.log(response);
        const { board, earned_free_move, earned_capture, is_game_over } =
          response.data;
        setComputerPits(board[0]);
        setHumanPits(board[2]);
        setComputerStore(board[1]);
        setHumanStore(board[3]);
        setEarnedFreeMove(earned_free_move);
        setEarnedCapture(earned_capture);
        setGameOver(is_game_over);
        if (!earned_free_move) {
          setCurrentPlayer(1 - currentPlayer);
        }
      })
      .catch((error) => console.error("Error making move:", error));
  };

  return (
    <div>
      <br></br>
      <h1>Welcome to Our Mancala Game, {name}!</h1>
      <br></br>
      <br></br>
      <div className="mancala-board">
        {isComputersTurn && <div>Computer's Turn...</div>}{" "}
        {earnedFreeMove && <div>Earned a free move!</div>}
        {earnedCapture && <div>Earned capture!</div>}
        <div className="pits-row">
          {computerPits &&
            [...computerPits].reverse().map((stones, index) => (
              <div className="pit" key={index}>
                <div className="stones">{stones}</div>
              </div>
            ))}
        </div>
        <div className="stores-row">
          <div className="store-left">
            <div className="store-value">{computerStore}</div>
          </div>
          <div className="store-right">
            <div className="store-value">{humanStore}</div>
          </div>
        </div>
        <div className="pits-row">
          {humanPits &&
            humanPits.map((stones, index) => (
              <button
                className="pit"
                key={index}
                onClick={() => !isComputersTurn && makeMove(index)}
                disabled={isComputersTurn || stones === 0}
              >
                <div className="stones">{stones}</div>
              </button>
            ))}
        </div>
      </div>
    </div>
  );
}

export default MancalaBoard;
