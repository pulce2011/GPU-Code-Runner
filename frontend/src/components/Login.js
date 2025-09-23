import { useState } from 'react';
import api, { setTokens } from '../services/api';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      // Invio POST al backend /api/token/
      const res = await api.post('/token/', { email, password });

      // Salva token per le richieste future
      setTokens(res.data.access, res.data.refresh);

      // Notifica App che login è avvenuto
      onLogin();
    } catch (err) {
      alert('Login fallito');
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;
