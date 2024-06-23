import React from 'react';
import styles from '../styles/Results.module.css';

const Results: React.FC = () => {
  return (
    <div className={styles.results}>
      <h1>Resultados</h1>
      <p>El porcentaje estimado de TEA es: {/* Mostrar resultado aquí */}</p>
      <p>Información sobre hospitales:</p>
      {/* Mostrar lista de hospitales aquí */}
    </div>
  );
};

export default Results;
