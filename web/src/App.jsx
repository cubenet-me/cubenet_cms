import React from "react";

// Header
const Header = () => (
  <header className="header">
    <div className="container">
      <h1 className="logo">MyApp</h1>
    </div>
  </header>
);

// Footer
const Footer = () => (
  <footer className="footer">
    <div className="container">
      <p>&copy; {new Date().getFullYear()} MyApp. Все права защищены.</p>
    </div>
  </footer>
);

// Контент страницы
const PageContent = () => (
  <div className="page-content">
    <h2>Главная страница</h2>
    <p>Добро пожаловать! Здесь можно разместить любой контент.</p>
  </div>
);

function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <PageContent />
      </main>
      <Footer />
    </div>
  );
}

export default App;
