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
        <Link to="/">Inicio</Link>
        {isAuthenticated ? (
          <>
            <Link to="/scan">Diagnostico</Link>
            <button onClick={logout} className={styles.btnLogout}>Cerrar sesion</button>
          </>
        ) : (
          <>
            <Link to="/login">Inicia sesion</Link>
            <Link to="/register">Registrate</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;
