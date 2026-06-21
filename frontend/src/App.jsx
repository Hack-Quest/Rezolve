import "./App.css";
import React from "react";
import { Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Pipeline from "./components/Pipeline";
import Page from "./components/page";
import Strategy from "./components/Startegy";

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      {/* Dynamic page content injects here */}
      <main className="flex-grow pt-[72px]">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/pipeline" element={<Pipeline />} />
          <Route path="/demo" element={<Page />} />
          <Route path="/strategy" element={<Strategy />} />
          {/* Add your other paths here */}
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;
