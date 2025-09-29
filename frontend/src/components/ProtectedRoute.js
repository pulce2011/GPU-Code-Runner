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

  // Componente loading
  const LoadingComponent = () => (
    <div className="flex items-center justify-center min-h-screen">
      <div className="flex items-center space-x-2 text-gray-600">
        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Caricamento...</span>
      </div>
    </div>
  );

  // Componente redirect
  const RedirectComponent = () => (
    <div className="flex items-center justify-center min-h-screen">
      <div className="flex items-center space-x-2 text-gray-600">
        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Reindirizzamento al login...</span>
      </div>
    </div>
  );

  if (loading) {
    return <LoadingComponent />;
  }

  if (!isAuthenticated) {
    return <RedirectComponent />;
  }

  return children;
}

export default ProtectedRoute;
