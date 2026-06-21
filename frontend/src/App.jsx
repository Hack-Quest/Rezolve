import { Routes, Route } from "react-router-dom";

import LandingPage from "./components/LandingPage";
import Page from "./components/page";

function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/demo" element={<Page />} />
    </Routes>
  );
}

export default App;
