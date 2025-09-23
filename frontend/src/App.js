import { useState, useEffect } from 'react';
import Login from './components/Login';
import ExerciseSelector from './components/ExerciseSelector';
import CodeEditor from './components/CodeEditor';
import RunButton from './components/RunButton';
import { setTokens } from './services/api';

function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('accessToken'));
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [selectedCode, setSelectedCode] = useState('');

  // Persistenza token: al mount controlla localStorage
  useEffect(() => {
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    if (access && refresh) setTokens(access, refresh);
  }, []);

  // Login handler
  const handleLoginSuccess = (access, refresh) => {
    setTokens(access, refresh);
    setLoggedIn(true);
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setTokens(null, null);

    setLoggedIn(false);
    setSelectedExercise(null);
    setSelectedCode('');
  };

  return (
    <div style={{ padding: '20px' }}>
      {!loggedIn ? (
        <Login onLogin={handleLoginSuccess} />
      ) : (
        <div>
          <button onClick={handleLogout} style={{ marginBottom: '20px' }}>
            Logout
          </button>

          <h2>Benvenuto! Seleziona un esercizio</h2>
          <ExerciseSelector onSelect={setSelectedExercise} />

          {selectedExercise && (
            <div style={{ marginTop: '20px' }}>
              <p>
                Hai selezionato: <strong>{selectedExercise.name}</strong>
              </p>

              <CodeEditor
                exercise={selectedExercise}
                onCodeChange={setSelectedCode}
              />

              <RunButton code={selectedCode} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
