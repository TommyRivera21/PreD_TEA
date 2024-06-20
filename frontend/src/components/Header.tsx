import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header>
      <nav>
        <Link to="/">Inicio</Link>
        <Link to="/scan">Escanear</Link>
        <Link to="/questionnaire">Cuestionario</Link>
      </nav>
    </header>
  );
};

export default Header;