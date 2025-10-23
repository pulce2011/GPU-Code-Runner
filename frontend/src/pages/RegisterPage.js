import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

// Pagina di registrazione con selezione corso
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

  // Carica la lista dei corsi dal backend
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

  // Gestisce il submit del form di registrazione
  const handleRegister = async (event) => {
    event.preventDefault();
    
    // Validazione campi obbligatori
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
    } catch (error) {
      alert('Registrazione fallita');
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
          Crea il tuo account
        </h2>
      </div>

      {/* Form di registrazione */}
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="card">
          <form className="space-y-6" onSubmit={handleRegister}>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              {/* Nome */}
              <div className="form-group">
                <label htmlFor="firstName" className="form-label">
                  Nome
                </label>
                <input
                  id="firstName"
                  name="firstName"
                  type="text"
                  autoComplete="given-name"
                  required
                  className="input-field"
                  placeholder="Mario"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </div>

              {/* Cognome */}
              <div className="form-group">
                <label htmlFor="lastName" className="form-label">
                  Cognome
                </label>
                <input
                  id="lastName"
                  name="lastName"
                  type="text"
                  autoComplete="family-name"
                  required
                  className="input-field"
                  placeholder="Rossi"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </div>
            </div>

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
                placeholder="mario.rossi@studenti.unimore.it"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            {/* Matricola */}
            <div className="form-group">
              <label htmlFor="matr" className="form-label">
                Numero di matricola
              </label>
              <input
                id="matr"
                name="matr"
                type="text"
                required
                className="input-field"
                placeholder="123456"
                value={matr}
                onChange={(e) => setMatr(e.target.value)}
              />
            </div>

            {/* Corso di laurea */}
            <div className="form-group">
              <label htmlFor="course" className="form-label">
                Corso di laurea
              </label>
              <select
                id="course"
                name="course"
                required
                className="input-field"
                value={courseId}
                onChange={(e) => setCourseId(e.target.value)}
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
                name="password"
                type="password"
                autoComplete="new-password"
                required
                className="input-field"
                placeholder="Inserisci una password sicura"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            {/* Bottone registrazione */}
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
                    Registrazione in corso...
                  </>
                ) : (
                  'Registrati'
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

            {/* Link login */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Hai già un account?{' '}
                <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500 transition-colors">
                  Accedi
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
