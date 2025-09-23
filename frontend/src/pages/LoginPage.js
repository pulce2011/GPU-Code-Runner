import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../hooks/useAuth';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async () => {
    if (!email || !password) {
      alert('Compila tutti i campi');
      return;
    }

    setLoading(true);
    try {
      const res = await api.post('/token/', { email, password });
      login(res.data.access, res.data.refresh);
      
      // Reindirizza alla dashboard
      navigate('/dashboard');
    } catch (err) {
      alert('Login fallito');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      maxWidth: '400px', 
      margin: '50px auto', 
      padding: '20px',
      border: '1px solid #ddd',
      borderRadius: '8px'
    }}>
      <h2>Login</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={e => setEmail(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={e => setPassword(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
      </div>

      <button 
        onClick={handleLogin} 
        disabled={loading}
        style={{ 
          width: '100%', 
          padding: '10px', 
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Caricamento...' : 'Login'}
      </button>

      <p style={{ textAlign: 'center', marginTop: '15px' }}>
        Non hai un account? <Link to="/register">Registrati</Link>
      </p>
    </div>
  );
}

export default LoginPage;
