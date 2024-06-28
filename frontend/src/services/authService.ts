import axios from "axios";
import { API_URL, TOKEN_KEY } from "../constants";

// Iniciar sesión y obtener el token
export const loginUser = async (email: string, password: string) => {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  if (response.data.token) {
    localStorage.setItem(TOKEN_KEY, JSON.stringify(response.data));
  }
  return response.data;
};

// Registrarse
export const registerUser = async (
  name: string,
  email: string,
  password: string
) => {
  const response = await axios.post(`${API_URL}/auth/register`, {
    name,
    email,
    password,
  });
  return response.data;
};

// Cerrar sesión
export const logoutUser = () => {
  localStorage.removeItem(TOKEN_KEY);
};

// Obtener el token actual
export const getCurrentToken = () => {
  const userStr = localStorage.getItem(TOKEN_KEY);
  if (userStr) {
    return JSON.parse(userStr).token;
  }
  return null;
};

// Obtener el usuario actual
export const getCurrentUser = () => {
  const userStr = localStorage.getItem(TOKEN_KEY);
  if (userStr) {
    return JSON.parse(userStr);
  }
  return null;
};
