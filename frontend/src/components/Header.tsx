import React from "react";
import { Link } from "react-router-dom";
import styles from "../styles/Header.module.css";
import logo from "../assets/tunito.png";
import { useAuth } from "../context/useAuth";

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  return (
    <header className={styles.header}>
      <Link className={styles.linkLogo} to="/">
        <img src={logo} alt="logo" />
      </Link>
      <nav className={styles.navLinks}>
        <Link to="/">Home</Link>
        {isAuthenticated ? (
          <>
            <Link to="/scan">Scan</Link>
            <Link to="/questionnaire">Questionnaire</Link>
            <Link to="/results">Results</Link>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
