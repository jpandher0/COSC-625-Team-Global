import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Welcome() {
  const [name, setName] = useState("");
  const navigate = useNavigate();

  const enterGame = (e) => {
    e.preventDefault();
    if (name.trim() !== "") {
      navigate(`/welcome?name=${encodeURIComponent(name)}`);
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
      <br></br>
      <br></br>
      <h1>Welcome to Our Mancala Game</h1>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
      <div class="welcomebuttons">
        <form onSubmit={enterGame}>
          <label htmlFor="name">Enter your name: </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <button type="submit">Enter</button>
        </form>
        <button type="button" onClick={instructionsPage}>
          Instructions
        </button>
      </div>
    </div>
  );
}

export default Welcome;
