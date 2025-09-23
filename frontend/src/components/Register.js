import { useState, useEffect } from 'react';
import api, { setTokens } from '../services/api';

function Register({ onRegister, onSwitchToLogin }) {
  const [email, setEmail] = useState('');
  const [matr, setMatr] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [courseId, setCourseId] = useState('');
  const [courses, setCourses] = useState([]);

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

    try {
      // Registrazione utente
      await api.post('/register/', {
        email,
        matr,
        first_name: firstName,
        last_name: lastName,
        password,
        course: courseId ? parseInt(courseId) : null
      });

      // Registrazione riuscita - reindirizza al login
      alert('Registrazione completata! Ora puoi effettuare il login.');
      onSwitchToLogin();

    } catch (err) {
      alert('Registrazione fallita');
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '0 auto' }}>
      <h2>Registrazione</h2>
      <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="text" placeholder="Matricola" value={matr} onChange={e => setMatr(e.target.value)} />
      <input type="text" placeholder="Nome" value={firstName} onChange={e => setFirstName(e.target.value)} />
      <input type="text" placeholder="Cognome" value={lastName} onChange={e => setLastName(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />

      <select value={courseId} onChange={e => setCourseId(e.target.value)}>
        <option value="">Seleziona corso</option>
        {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
      </select>

      <button onClick={handleRegister}>Registrati</button>
    </div>
  );
}

export default Register;