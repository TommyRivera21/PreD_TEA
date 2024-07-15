import axios from "axios";
import { API_URL, TOKEN_KEY, REFRESH_TOKEN_KEY } from "../constants";

// Iniciar sesión y obtener el token
export const loginUser = async (email: string, password: string) => {
  const response = await axios.post(`${API_URL}/auth/login`, {
    email,
    password,
  });
  if (response.data.token) {
    localStorage.setItem(TOKEN_KEY, JSON.stringify(response.data));
    localStorage.setItem(REFRESH_TOKEN_KEY, response.data.refreshToken);
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
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

// Obtener el token actual
export const getCurrentToken = () => {
  const userStr = localStorage.getItem(TOKEN_KEY);
  if (userStr) {
    return JSON.parse(userStr).token;
  }
  return null;
};

// Obtener el token de refresco actual
export const getCurrentRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

// Obtener el usuario actual
export const getCurrentUser = () => {
  const userStr = localStorage.getItem(TOKEN_KEY);
  if (userStr) {
    return JSON.parse(userStr);
  }
  return null;
};

// Refescar el token
export const refreshToken = async () => {
  const refreshToken = getCurrentRefreshToken();
  if (!refreshToken) throw new Error("No refresh token found");

  try {
    const response = await axios.post(`${API_URL}/auth/refresh`, {
      refreshToken,
    });
    const { token } = response.data;
    localStorage.setItem(TOKEN_KEY, JSON.stringify({ token }));
    return token;
  } catch (error) {
    // Si el refresh token es inválido, cerramos la sesión
    logoutUser();
    throw new Error("Invalid refresh token");
  }
};
