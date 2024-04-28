import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Welcome from "./Welcome";
import Mancala from "./Mancala";
import InstructionsPage from "./Instructions";
import axios from "axios";

function App() {
  const [boardData, setBoardData] = useState(null);

  useEffect(() => {
    axios
      .get("/api/board")
      .then((response) => {
        setBoardData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching board data:", error);
      });
  }, []); // Fetch data only once when the component mounts

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/welcome" element={<Mancala board={boardData} />} />{" "}
        {/* Pass board data to Mancala component */}
        <Route path="/instructions" element={<InstructionsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
