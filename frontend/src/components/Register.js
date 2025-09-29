import { useState, useEffect } from 'react';
import api from '../services/api';

// Componente form di registrazione
function Register({ onRegister, onSwitchToLogin }) {
  const [email, setEmail] = useState('');
  const [matr, setMatr] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [courseId, setCourseId] = useState('');
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);

  // Carica lista corsi
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/courses/');
        setCourses(response.data);
      } catch (error) {
        console.error('Errore nel recupero corsi:', error);
      }
    };

    fetchCourses();
  }, []);

  // Gestisce registrazione
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
      onSwitchToLogin();
    } catch (error) {
      alert('Registrazione fallita');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h2 className="text-2xl font-bold text-center mb-6">Registrazione</h2>
      
      {/* Nome */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="form-group">
          <label htmlFor="firstName" className="form-label">
            Nome
          </label>
          <input
            id="firstName"
            type="text"
            placeholder="Inserisci il tuo nome"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="input-field"
            required
            disabled={loading}
          />
        </div>

        {/* Cognome */}
        <div className="form-group">
          <label htmlFor="lastName" className="form-label">
            Cognome
          </label>
          <input
            id="lastName"
            type="text"
            placeholder="Inserisci il tuo cognome"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className="input-field"
            required
            disabled={loading}
          />
        </div>
      </div>

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

      {/* Matricola */}
      <div className="form-group">
        <label htmlFor="matr" className="form-label">
          Matricola
        </label>
        <input
          id="matr"
          type="text"
          placeholder="Inserisci la tua matricola"
          value={matr}
          onChange={(e) => setMatr(e.target.value)}
          className="input-field"
          required
          disabled={loading}
        />
      </div>

      {/* Corso di laurea */}
      <div className="form-group">
        <label htmlFor="course" className="form-label">
          Corso di laurea
        </label>
        <select
          id="course"
          value={courseId}
          onChange={(e) => setCourseId(e.target.value)}
          className="input-field"
          required
          disabled={loading}
        >
          <option value="">Seleziona un corso</option>
          {courses.map(course => (
            <option key={course.id} value={course.id}>
              {course.name}
            </option>
          ))}
        </select>
      </div>

      {/* Password */}
      <div className="form-group">
        <label htmlFor="password" className="form-label">
          Password
        </label>
        <input
          id="password"
          type="password"
          placeholder="Inserisci una password sicura"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
          required
          disabled={loading}
        />
      </div>

      {/* Bottone registrazione */}
      <button
        onClick={handleRegister}
        className="btn-primary w-full"
        disabled={loading}
      >
        {loading ? 'Registrazione in corso...' : 'Registrati'}
      </button>
    </div>
  );
}

export default Register;