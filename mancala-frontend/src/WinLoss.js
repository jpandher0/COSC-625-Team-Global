// WinLossPage.js

import React from "react";
import { Link } from "react-router-dom";

function WinLossPage({ computerStore, humanStore }) {
  return (
    <div>
      <h1>Game Result</h1>
      {humanStore > computerStore ? (
        <>
          <h2>Congratulations!</h2>
          <p>You won the game!</p>
          <p>Computer score: {computerStore}</p>
          <p>Your score: {humanStore}</p>
          <script>console.log(computerStore);</script>
        </>
      ) : (
        <>
          <h2>Oops!</h2>
          <p>You lost the game. Better luck next time!</p>
          <p>Computer score: {computerStore}</p>
          <p>Your score: {humanStore}</p>
          <p>Would you like to play again?</p>
        </>
      )}
      <Link to="/">Back to Home</Link>
    </div>
  );
}

export default WinLossPage;
