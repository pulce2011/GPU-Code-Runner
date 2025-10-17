import { useState, useEffect, useCallback } from 'react';
import { setTokens } from '../services/api';

// Hook personalizzato per gestione autenticazione JWT
export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Verifica validità token
  const isValidToken = (token) => {
    return token && token !== 'null' && token.trim() !== '';
  };

  // Verifica autenticazione
  const checkAuth = useCallback(() => {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');
    
    if (isValidToken(accessToken) && isValidToken(refreshToken)) {
      setTokens(accessToken, refreshToken);
      setIsAuthenticated(true);
    } else {
      clearTokens();
    }
    setLoading(false);
  }, []);

  // Pulisce token
  const clearTokens = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setTokens(null, null);
    setIsAuthenticated(false);
  };

  // Login
  const login = (accessToken, refreshToken) => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    setTokens(accessToken, refreshToken);
    setIsAuthenticated(true);
  };

  // Logout
  const logout = () => {
    clearTokens();
  };

  // Controlla auth all'avvio
  useEffect(() => {
    const t = setTimeout(checkAuth, 100);
    return () => clearTimeout(t);
  }, [checkAuth]);

  return { isAuthenticated, loading, login, logout };
}
