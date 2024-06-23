import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/Home.module.css';

const Home: React.FC = () => {
  return (
    <div className={styles.home}>
      <h1 className={styles.titleOne}>Tunito</h1>
      <p className={styles.description}>Sistema de predicción para el diagnóstico preliminar del Trastorno del Espectro Autista en niños,mediante la aplicación de redes neuronales artificiales</p>
      <Link className={styles.btnHome} to="/scan">Realizar diagnostico</Link>
    </div>
  );
};

export default Home;
