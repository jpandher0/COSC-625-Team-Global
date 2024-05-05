import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./App.css";
import axios from "axios";

function MancalaBoard() {
  const [pits, setPits] = useState([]);
  const [stores, setStores] = useState([0, 0]);
  const [currentPlayer, setCurrentPlayer] = useState(0);
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const name = params.get("name");

  useEffect(() => {
    axios
      .get("http://localhost:8000/get_board")
      .then((response) => {
        const { board } = response.data;
        setPits(board.slice(0, 2));
        setStores(board.slice(2));
      })
      .catch((error) => console.error("Error fetching board data:", error));
  }, []);

  const makeMove = (pitIndex) => {
    const moveData = {
      player_num: currentPlayer + 1,
      start_index: pitIndex,
    };

    axios
      .post("http://localhost:8000/make_move", moveData)
      .then((response) => {
        const { message } = response.data;
        console.log(message);
        // Update the board after making the move
        axios
          .get("http://localhost:8000/get_board")
          .then((response) => {
            const { board } = response.data;
            setPits(board.slice(0, 2));
            setStores(board.slice(2));
          })
          .catch((error) => console.error("Error fetching board data:", error));
      })
      .catch((error) =>
        console.error("There was a problem with your axios request:", error)
      );
  };

  const play = (pitIndex) => {
    let stones = pits[pitIndex];
    if (stones === 0 || currentPlayer !== Math.floor(pitIndex / 6)) return;

    const newPits = [...pits];
    newPits[pitIndex] = 0;

    let currentIndex = pitIndex;
    while (stones > 0) {
      currentIndex = (currentIndex + 1) % 12;
      newPits[currentIndex]++;
      stones--;
    }

    if (
      newPits[currentIndex] === 1 &&
      Math.floor(currentIndex / 6) === currentPlayer
    ) {
      const oppositeIndex = 11 - currentIndex;
      const captured = newPits[oppositeIndex];
      newPits[oppositeIndex] = 0;
      const newStores = [...stores];
      newStores[currentPlayer] += captured + 1;
      newPits[currentIndex] = 0;
      setStores(newStores);
    }

    setPits(newPits);
    setCurrentPlayer(1 - currentPlayer);
    makeMove(pitIndex); // Make API call after local move
  };

  //   return (
  //     <div>
  //       <h1>Welcome to Our Mancala Game, {name}!</h1>
  //       <div className="board">
  //         <div className="pits">
  //           <div className="store">{stores[1]}</div>
  //           {pits.slice(6).map((stones, index) => (
  //             <button
  //               className="stones"
  //               key={index + 6}
  //               onClick={() => play(index + 6)}
  //             >
  //               {stones}
  //             </button>
  //           ))}
  //           <div className="store">{stores[0]}</div>
  //         </div>
  //       </div>
  //       <div className="board">
  //         <div className="pits">
  //           {pits
  //             .slice(0, 6)
  //             .reverse()
  //             .map((stones, index) => (
  //               <button
  //                 className="stones"
  //                 key={5 - index}
  //                 onClick={() => play(5 - index)}
  //               >
  //                 {stones}
  //               </button>
  //             ))}
  //         </div>
  //       </div>
  //       <h3>Your Score: {stores[1]}</h3>
  //       <h3>Computer Score: {stores[0]}</h3>
  //     </div>
  //   );
  return (
    <div>
      <h1>Welcome to Our Mancala Game, {name}!</h1>
      {/* Render the board */}
      <div className="board">{/* Render pits */}</div>
      <h3>Your Score: {stores[1]}</h3>
      <h3>Computer Score: {stores[0]}</h3>
    </div>
  );
}

export default MancalaBoard;
