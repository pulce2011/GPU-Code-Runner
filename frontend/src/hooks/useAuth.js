import { useState, useEffect } from 'react';
import { setTokens } from '../services/api';

export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkAuth = () => {
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    
    // Controlla che i token esistano, non siano 'null', e non siano stringhe vuote
    const isValidAccess = access && access !== 'null' && access.trim() !== '';
    const isValidRefresh = refresh && refresh !== 'null' && refresh.trim() !== '';
    
    if (isValidAccess && isValidRefresh) {
      setTokens(access, refresh);
      setIsAuthenticated(true);
    } else {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      setTokens(null, null);
      setIsAuthenticated(false);
    }
    setLoading(false);
  };

  const login = (accessToken, refreshToken) => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    setTokens(accessToken, refreshToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setTokens(null, null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    // Piccolo delay per assicurarsi che il componente sia montato
    setTimeout(() => {
      checkAuth();
    }, 100);
  }, []);

  return { isAuthenticated, loading, login, logout };
}
