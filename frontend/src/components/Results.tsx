import React from "react";
import styles from "../styles/Results.module.css";

const Results: React.FC = () => {
  return (
    <div className={styles.results}>
      <h1 className={styles.titleResults}>Resultados</h1>
  
      <p>El porcentaje estimado de TEA es: 75%</p>
      <p>Información sobre hospitales:</p>
      <ul>
        <li>Hospital A</li>
        <li>Hospital B</li>
        <li>Hospital C</li>
      </ul>
    </div>
  );
};

export default Results;