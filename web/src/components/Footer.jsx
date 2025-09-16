import React from "react";

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; {new Date().getFullYear()} MyApp. Все права защищены.</p>
      </div>
    </footer>
  );
}

export default Footer;
