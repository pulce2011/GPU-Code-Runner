import { useState } from 'react';
import Login from './components/Login';
import ExerciseSelector from './components/ExerciseSelector';
import CodeEditor from './components/CodeEditor';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);              // Stato login
  const [selectedExercise, setSelectedExercise] = useState(null); // Esercizio selezionato

  // Chiamata da Login.js quando login va a buon fine
  const handleLoginSuccess = () => {
    console.log('Utente loggato!');
    setLoggedIn(true);
  };

  return (
    <div style={{ padding: '20px' }}>
      {!loggedIn ? (
        // Mostra Login se non loggato
        <Login onLogin={handleLoginSuccess} />
      ) : (
        // Mostra ExerciseSelector + CodeEditor se loggato
        <div>
          <h2>Benvenuto! Seleziona un esercizio</h2>
          <ExerciseSelector onSelect={setSelectedExercise} />

          {selectedExercise && (
            <div style={{ marginTop: '20px' }}>
              <p>Hai selezionato: <strong>{selectedExercise.name}</strong></p>
              <CodeEditor
                exercise={selectedExercise} // Deve contenere `signature` dal backend
                onCodeChange={(code) => console.log('Codice aggiornato:', code)}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
