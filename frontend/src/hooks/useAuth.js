import { useState, useEffect, useCallback } from 'react';
import { setTokens } from '../services/api';

// Hook personalizzato per gestione autenticazione JWT
export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Verifica la validità di un token
  const isValidToken = (token) => {
    return token && token !== 'null' && token.trim() !== '';
  };

  // Verifica lo stato di autenticazione
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

  // Pulisce tutti i token salvati
  const clearTokens = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setTokens(null, null);
    setIsAuthenticated(false);
  };

  // Effettua il login dell'utente
  const login = (accessToken, refreshToken) => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    setTokens(accessToken, refreshToken);
    setIsAuthenticated(true);
  };

  // Effettua il logout dell'utente
  const logout = () => {
    clearTokens();
  };

  // Controlla l'autenticazione all'avvio
  useEffect(() => {
    const t = setTimeout(checkAuth, 100);
    return () => clearTimeout(t);
  }, [checkAuth]);

  return { isAuthenticated, loading, login, logout };
}
