import React from "react";

function Header() {
  const buttons = [
    "Главная",
    "Правила",
    "Сервера",
    "Донат",
    "Форум",
    "Начать играть",
    "Остальное",
  ];

  return (
    <header
      style={{
        backgroundColor: "#222",
        color: "#fff",
        padding: "10px 0",
      }}
    >
      <nav style={{ textAlign: "center" }}>
        {buttons.map((btn) => (
          <button
            key={btn}
            style={{
              margin: "0 8px",
              padding: "8px 16px",
              cursor: "pointer",
              borderRadius: "5px",
              border: "none",
              backgroundColor: "#555",
              color: "#fff",
            }}
          >
            {btn}
          </button>
        ))}
      </nav>
    </header>
  );
}

export default Header;
