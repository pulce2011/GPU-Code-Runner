import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [matr, setMatr] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [courseId, setCourseId] = useState('');
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Recupera corsi dal backend
  useEffect(() => {
    api.get('/courses/')
      .then(res => setCourses(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleRegister = async () => {
    if (!email || !matr || !firstName || !lastName || !password || !courseId) {
      alert('Compila tutti i campi');
      return;
    }

    setLoading(true);
    try {
      await api.post('/register/', {
        email,
        matr,
        first_name: firstName,
        last_name: lastName,
        password,
        course: courseId ? parseInt(courseId) : null
      });

      alert('Registrazione completata! Ora puoi effettuare il login.');
      navigate('/login');
    } catch (err) {
      alert('Registrazione fallita');
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
      <h2>Registrazione</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={e => setEmail(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input 
          type="text" 
          placeholder="Matricola" 
          value={matr} 
          onChange={e => setMatr(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input 
          type="text" 
          placeholder="Nome" 
          value={firstName} 
          onChange={e => setFirstName(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input 
          type="text" 
          placeholder="Cognome" 
          value={lastName} 
          onChange={e => setLastName(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={e => setPassword(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />

        <select 
          value={courseId} 
          onChange={e => setCourseId(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        >
          <option value="">Seleziona corso</option>
          {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </div>

      <button 
        onClick={handleRegister} 
        disabled={loading}
        style={{ 
          width: '100%', 
          padding: '10px', 
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Caricamento...' : 'Registrati'}
      </button>

      <p style={{ textAlign: 'center', marginTop: '15px' }}>
        Hai già un account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default RegisterPage;
