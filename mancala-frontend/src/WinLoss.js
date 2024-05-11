import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

function WinLossPage() {
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const computerScore = params.get("computerScore");
  const humanScore = params.get("humanScore");

  return (
    <div>
      <h1>Game Result</h1>
      {humanScore > computerScore ? (
        <>
          <h2>Congratulations!</h2>
          <p>You won the game!</p>
          <p>Computer score: {computerScore}</p>
          <p>Your score: {humanScore}</p>
          <script>console.log(computerStore);</script>
        </>
      ) : (
        <>
          <h2>Oops!</h2>
          <p>You lost the game. Better luck next time!</p>
          <p>Computer score: {computerScore}</p>
          <p>Your score: {humanScore}</p>
          <p>Would you like to play again?</p>
        </>
      )}
      <Link to="/">Back to Home</Link>
    </div>
  );
}

export default WinLossPage;
