import React from "react";
import Header from "./Header.jsx";
import Footer from "./Footer.jsx";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <Header />
      <main>
        <div>
          <h1>Добро пожаловать на CubeNet!</h1>
          <p>Выберите раздел, чтобы начать.</p>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
