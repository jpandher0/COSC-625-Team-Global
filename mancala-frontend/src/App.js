import React, { useState } from 'react';
import './App.css';

function MancalaBoard() {
    // Initialize the game state with 4 stones in each pit
    const initialPits = Array(12).fill(4);
    const [pits, setPits] = useState(initialPits);
    const [stores, setStores] = useState([0, 0]); // Stores for each player
    const [currentPlayer, setCurrentPlayer] = useState(0); // 0 for player 1, 1 for player 2

    const play = (pitIndex) => {
        let stones = pits[pitIndex];
        if (stones === 0 || currentPlayer !== Math.floor(pitIndex / 6)) return; // Check if pit is empty or not the player's turn

        // Clear the selected pit
        const newPits = [...pits];
        newPits[pitIndex] = 0;

        // Distribute the stones
        let currentIndex = pitIndex;
        while (stones > 0) {
            currentIndex = (currentIndex + 1) % 12;
            newPits[currentIndex]++;
            stones--;
        }

        // Check for capture
        if (newPits[currentIndex] === 1 && Math.floor(currentIndex / 6) === currentPlayer) {
            const oppositeIndex = 11 - currentIndex;
            const captured = newPits[oppositeIndex];
            newPits[oppositeIndex] = 0; // Clear the opposite pit
            const newStores = [...stores];
            newStores[currentPlayer] += captured + 1;
            newPits[currentIndex] = 0; // Clear the landing pit
            setStores(newStores);
        }

        setPits(newPits);
        setCurrentPlayer(1 - currentPlayer); // Switch turns
    };

    return (
        <div className="board">
            <div className="store">{stores[1]}</div>
            <div className="pits">
                {pits.slice(6).map((stones, index) => (
                    <button key={index + 6} onClick={() => play(index + 6)}>{stones}</button>
                ))}
                {pits.slice(0, 6).reverse().map((stones, index) => (
                    <button key={5 - index} onClick={() => play(5 - index)}>{stones}</button>
                ))}
            </div>
            <div className="store">{stores[0]}</div>
        </div>
    );
}

export default MancalaBoard;
