import { useState, useEffect } from 'react';
import { setTokens } from '../services/api';

// Hook personalizzato per gestione autenticazione JWT
export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Verifica validità token salvati
  const checkAuth = () => {
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    
    // Controlla esistenza e validità token
    const isValidAccess = access && access !== 'null' && access.trim() !== '';
    const isValidRefresh = refresh && refresh !== 'null' && refresh.trim() !== '';
    
    if (isValidAccess && isValidRefresh) {
      setTokens(access, refresh);
      setIsAuthenticated(true);
    } else {
      // Pulisce token non validi
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setTokens(null, null);
      setIsAuthenticated(false);
    }
    setLoading(false);
  };

  // Salva token dopo login
  const login = (accessToken, refreshToken) => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    setTokens(accessToken, refreshToken);
    setIsAuthenticated(true);
  };

  // Rimuove token e logout
  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setTokens(null, null);
    setIsAuthenticated(false);
  };

  // Controlla auth all'avvio
  useEffect(() => {
    // Delay per assicurare montaggio componente
    setTimeout(() => {
      checkAuth();
    }, 100);
  }, []);

  return { isAuthenticated, loading, login, logout };
}
