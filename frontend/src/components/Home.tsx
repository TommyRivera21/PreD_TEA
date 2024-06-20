import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div>
      <h1>Sistema de Predicción del TEA</h1>
      <Link to="/scan"><button>Realizar Escaneo</button></Link>
      <Link to="/questionnaire"><button>Cuestionario</button></Link>
    </div>
  );
};

export default Home;
