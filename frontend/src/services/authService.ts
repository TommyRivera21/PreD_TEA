import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Reemplaza con la URL de tu backend

// Iniciar sesión y obtener el token
export const login = async (email: string, password: string) => {
  const response = await axios.post(`${API_URL}/login`, { email, password });
  if (response.data.token) {
    localStorage.setItem('user', JSON.stringify(response.data));
  }
  return response.data;
};

// Registrarse
export const register = async (name: string, email: string, password: string) => {
  const response = await axios.post(`${API_URL}/register`, { name, email, password });
  return response.data;
};

// Cerrar sesión
export const logout = () => {
  localStorage.removeItem('user');
};

// Obtener el token actual
export const getCurrentToken = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    return JSON.parse(userStr).token;
  }
  return null;
};

// Obtener el usuario actual
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    return JSON.parse(userStr);
  }
  return null;
};
