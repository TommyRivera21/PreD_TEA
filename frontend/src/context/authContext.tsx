import React, { createContext, useState, ReactNode } from "react";
import { getCurrentUser, loginUser, logoutUser } from "../services/authService";

export interface AuthContextType {
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(
    !!getCurrentUser()
  );

  const login = async (email: string, password: string) => {
    try {
      await loginUser(email, password);
      setIsAuthenticated(true);
    } catch (error) {
      console.error("Failed to login:", error);
    }
  };

  const logout = () => {
    logoutUser();
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};