import { useState } from 'react';
import api, { setTokens } from '../services/api';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault(); // previene il refresh della pagina
    try {
      // POST al backend /api/token/
      const res = await api.post('/token/', { email, password });

      // Salva token in api.js e localStorage
      setTokens(res.data.access, res.data.refresh);

      // Notifica App.js con i token
      onLogin(res.data.access, res.data.refresh);
    } catch (err) {
      alert('Login fallito: controlla email/password');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleLogin} style={{ maxWidth: '300px', margin: 'auto' }}>
      <h2>Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />

      <button
        type="submit"
      >
        Login
      </button>
    </form>
  );
}

export default Login;
