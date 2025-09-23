import { useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      window.location.href = '/login';
    }
  }, [isAuthenticated, loading]);

  // Mostra loading mentre controlla l'autenticazione
  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}>Caricamento...</div>;
  }

  // Se non autenticato, mostra nulla (il redirect è gestito da useEffect)
  if (!isAuthenticated) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}>Reindirizzamento al login...</div>;
  }

  // Se autenticato, mostra il contenuto protetto
  return children;
}

export default ProtectedRoute;
