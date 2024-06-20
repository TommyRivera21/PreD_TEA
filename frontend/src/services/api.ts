import axios from 'axios';
import { getCurrentToken } from './authService';

const API_URL = 'http://localhost:5000'; // Reemplaza con la URL de tu backend

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = getCurrentToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
