import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./styles/main.css"; // Подключаем глобальные стили

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
