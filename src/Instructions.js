// Instructions.js

import React from "react";
import { Link } from "react-router-dom";

function InstructionsPage() {
  return (
    <div>
      <h1>Instructions</h1>
      <h2>Object:</h2>
      <br></br>
      <p>
        The object of the game is to collect the most pieces by the end of the
        game.
      </p>
      <br></br>
      <h2>Game Play: </h2>
      <br></br>
      <p>
        1. The game begins with one player picking up all of the pieces in any
        one of the pockets on his/her side.{" "}
      </p>
      <p>
        2. Moving counter-clockwise, the player deposits one of the stones in
        each pocket until the stones run out.{" "}
      </p>
      <p>
        3. If you run into your own Mancala (store), deposit one piece in it. If
        you run into your opponent's Mancala, skip it and continue moving to the
        next pocket.{" "}
      </p>
      <p>
        4. If the last piece you drop is in your own Mancala, you take another
        turn.{" "}
      </p>
      <p>
        5. If the last piece you drop is in an empty pocket on your side, you
        capture that piece and any pieces in the pocket directly opposite.{" "}
      </p>
      <p>6. Always place all captured pieces in your Mancala (store). </p>
      <p>
        7. The game ends when all six pockets on one side of the Mancala board
        are empty.{" "}
      </p>
      <p>
        8. The player who still has pieces on his/her side of the board when the
        game ends captures all of those pieces.{" "}
      </p>
      <p>
        9. Count all the pieces in each Mancala. The winner is the player with
        the most pieces.
      </p>
      <Link to="/">Back to Home</Link>
    </div>
  );
}

export default InstructionsPage;
