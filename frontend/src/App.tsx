import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Home from './components/Home';
import Scan from './components/Scan';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import Login from './components/Login';
import Register from './components/Register';
import { getCurrentUser } from './services/authService';
import styles from './styles/App.module.css';
import './App.css'; // Importa los estilos globales

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const user = getCurrentUser();
  return user ? children : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <div className="app"> {/* Aplica la clase 'app' para estilos globales */}
      <Router>
        <Header />
        <main className={styles['main-content']}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scan" element={<PrivateRoute><Scan /></PrivateRoute>} />
            <Route path="/questionnaire" element={<PrivateRoute><Questionnaire /></PrivateRoute>} />
            <Route path="/results" element={<PrivateRoute><Results /></PrivateRoute>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
      </Router>
    </div>
  );
};

export default App;