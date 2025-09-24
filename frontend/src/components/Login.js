import { useState } from 'react';
import api, { setTokens } from '../services/api';

// Componente form di login
function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Gestisce submit form
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Autenticazione JWT
      const res = await api.post('/token/', { email, password });

      // Salva token e notifica padre
      setTokens(res.data.access, res.data.refresh);
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
