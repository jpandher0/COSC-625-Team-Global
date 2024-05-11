import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Welcome from "./Welcome";
import MancalaBoard from "./Mancala";
import InstructionsPage from "./Instructions";
import WinLossPage from "./WinLoss";
import axios from "axios";
import "./App.css";
import "./App.css";

function App() {
  const [boardData, setBoardData] = useState(null);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/welcome" element={<MancalaBoard />} />{" "}
        <Route path="/instructions" element={<InstructionsPage />} />
        <Route path="/winLoss" element={<WinLossPage />} />
      </Routes>
    </Router>
  );
}

export default App;
