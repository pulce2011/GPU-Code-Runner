import { useState } from 'react';
import api, { setTokens } from '../services/api';

// Componente form di login
function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // Gestisce il submit del form di login
  const handleLogin = async (event) => {
    event.preventDefault();
    
    if (!email || !password) {
      alert('Compila tutti i campi');
      return;
    }

    // Avvia loading
    setLoading(true);
    try {
      const response = await api.post('/token/', { email, password });
      // Salva i token e notifica il login
      setTokens(response.data.access, response.data.refresh);
      onLogin(response.data.access, response.data.refresh);
    } catch (error) {
      alert('Login fallito: controlla email/password');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleLogin} className="max-w-sm mx-auto space-y-4">
      <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

      {/* Email */}
      <div className="form-group">
        <label htmlFor="email" className="form-label">
          Email
        </label>
        <input
          id="email"
          type="email"
          placeholder="Inserisci la tua email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="input-field"
          required
          disabled={loading}
        />
      </div>

      {/* Password */}
      <div className="form-group">
        <label htmlFor="password" className="form-label">
          Password
        </label>
        <input
          id="password"
          type="password"
          placeholder="Inserisci la tua password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
          required
          disabled={loading}
        />
      </div>

      {/* Bottone login */}
      <button
        type="submit"
        className="btn-primary w-full"
        disabled={loading}
      >
        {loading ? 'Accesso in corso...' : 'Accedi'}
      </button>
    </form>
  );
}

export default Login;
