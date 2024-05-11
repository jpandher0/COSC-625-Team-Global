import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Welcome() {
  const [name, setName] = useState("");
  const [computerPlayer, setComputerPlayer] = useState("");
  const navigate = useNavigate();

  const enterGame = (e) => {
    e.preventDefault();
    if (name.trim() !== "" && computerPlayer.trim() != "") {
      navigate(
        `/welcome?name=${encodeURIComponent(
          name
        )}&computerPlayer=${computerPlayer}`
      );
    }
  };

  const instructionsPage = (e) => {
    navigate(`/instructions`);
  };

  return (
    <div>
      <br></br>
      <br></br>
      <br></br>
      <h1>Welcome to Our Mancala Game</h1>
      <br></br>
      <div className="welcomebuttons">
        <div className="instructionsbutton">
          <button type="button" onClick={instructionsPage}>
            Instructions
          </button>
          <br></br>
          <br></br>
          <br></br>
          <form onSubmit={enterGame}>
            <label htmlFor="name">Enter your name: </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <br></br>
            <br></br>
            <button onClick={(e) => setComputerPlayer("Default")} type="submit">
              Play with Default Player
            </button>
            <button onClick={(e) => setComputerPlayer("AI")} type="submit">
              Play with AI Player
            </button>
          </form>
          <br></br>
          <br></br>
          <br></br>
          <br></br>
        </div>
      </div>
    </div>
  );
}

export default Welcome;
