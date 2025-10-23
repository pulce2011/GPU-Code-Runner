import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';

// Pagina di login con autenticazione JWT
function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  // Gestisce il submit del form di login
  const handleLogin = async (event) => {
    event.preventDefault();
    
    // Validazione campi obbligatori
    if (!email || !password) {
      alert('Compila tutti i campi');
      return;
    }

    // Avvia stato di caricamento
    setLoading(true);
    try {
      const response = await api.post('/token/', { email, password });
      login(response.data.access, response.data.refresh);
      navigate('/dashboard');
    } catch (error) {
      alert('Login fallito');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">GPU Code Runner</h1>
        </div>
        <h2 className="mt-6 text-center text-2xl font-semibold text-gray-900">
          Accedi al tuo account
        </h2>
      </div>

      {/* Form login */}
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="card">
          <form className="space-y-6" onSubmit={handleLogin}>
            {/* Email */}
            <div className="form-group">
              <label htmlFor="email" className="form-label">
                Indirizzo email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="input-field"
                placeholder="306627@studenti.unimore.it"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Password */}
            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="input-field"
                placeholder="Inserisci la tua password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Bottone login */}
            <div>
              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full flex justify-center py-3 px-4 text-sm font-medium"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Accesso in corso...
                  </>
                ) : (
                  'Accedi'
                )}
              </button>
            </div>
          </form>

          {/* Divisore */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Oppure</span>
              </div>
            </div>

            {/* Link registrazione */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Non hai un account?{' '}
                <Link to="/register" className="font-medium text-primary-600 hover:text-primary-500 transition-colors">
                  Registrati
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
