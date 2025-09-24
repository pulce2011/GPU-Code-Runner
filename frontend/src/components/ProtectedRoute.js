import { useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';

// Componente per proteggere route autenticate
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  // Redirect al login se non autenticato
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      window.location.href = '/login';
    }
  }, [isAuthenticated, loading]);

  // Loading durante controllo auth
  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}>Caricamento...</div>;
  }

  // Redirect in corso
  if (!isAuthenticated) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}>Reindirizzamento al login...</div>;
  }

  // Renderizza contenuto protetto
  return children;
}

export default ProtectedRoute;
