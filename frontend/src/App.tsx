import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Home from './components/Home';
import Scan from './components/Scan';
import Questionnaire from './components/Questionnaire';
import Results from './components/Results';
import Login from './components/Login';
import Register from './components/Register';
import { AuthProvider} from './context/authContext';
import { HOME_ROUTE, LOGIN_ROUTE, REGISTER_ROUTE, SCAN_ROUTE, QUESTIONNAIRE_ROUTE, RESULTS_ROUTE } from './constants';
import styles from './styles/App.module.css';
import { useAuth } from './context/useAuth';

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to={LOGIN_ROUTE} />;
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Header />
        <main className={styles['main-content']}>
          <Routes>
            <Route path={HOME_ROUTE} element={<Home />} />
            <Route path={SCAN_ROUTE} element={<PrivateRoute><Scan /></PrivateRoute>} />
            <Route path={QUESTIONNAIRE_ROUTE} element={<PrivateRoute><Questionnaire /></PrivateRoute>} />
            <Route path={RESULTS_ROUTE} element={<PrivateRoute><Results /></PrivateRoute>} />
            <Route path={LOGIN_ROUTE} element={<Login />} />
            <Route path={REGISTER_ROUTE} element={<Register />} />
          </Routes>
        </main>
      </Router>
    </AuthProvider>
  );
};

export default App;
