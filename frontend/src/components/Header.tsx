import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/Header.module.css';
import logo from '../assets/tunito.png';

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      <Link className={styles.linkLogo} to="/">
        <img src={logo} alt="logo" />
      </Link>
      <nav className={styles.navLinks}>
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
      </nav>
    </header>
  );
};

export default Header;
