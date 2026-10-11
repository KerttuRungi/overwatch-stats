import { Route, Routes } from "react-router-dom";
import "./App.css";
import HomePage from "./pages/HomePage";
import ComparePage from "./pages/ComparePage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/compare" element={<ComparePage />} />
    </Routes>
  );
}

export default App;
