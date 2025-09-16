import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="header">
      <div className="container">
        <h1 className="logo">MyApp</h1>
        <nav>
          <ul className="nav-list">
            <li><Link to="/">Launcher</Link></li>
            <li><Link to="/example">Example</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;
