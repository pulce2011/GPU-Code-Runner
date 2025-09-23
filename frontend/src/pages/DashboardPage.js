import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ExerciseSelector from '../components/ExerciseSelector';
import CodeEditor from '../components/CodeEditor';
import RunButton from '../components/RunButton';
import { setTokens } from '../services/api';

function DashboardPage() {
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [selectedCode, setSelectedCode] = useState('');
  const navigate = useNavigate();

  const handleLogout = () => {
    // Rimuovi completamente i token dal localStorage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    
    // Pulisci anche eventuali token residui
    localStorage.clear();
    
    // Reset stato
    setTokens(null, null);
    setSelectedExercise(null);
    setSelectedCode('');
    
    // Reindirizza al login
    navigate('/login');
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px',
        paddingBottom: '10px',
        borderBottom: '1px solid #ddd'
      }}>
        <h1>GPU Code Runner</h1>
        <button 
          onClick={handleLogout}
          style={{
            padding: '8px 16px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>

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
  );
}

export default DashboardPage;
