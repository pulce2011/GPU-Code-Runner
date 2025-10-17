import { useState } from 'react';
import PropTypes from 'prop-types';
import api from '../services/api';

// Componente pulsante per esecuzione codice
function RunButton({ code, onOutputChange, onTaskDetails, onCreditsUpdate, onResetResults, exerciseId }) {
  const [loading, setLoading] = useState(false);

  // Esegue codice sul backend
  const handleRun = async () => {
    if (!code || !exerciseId) return;

    // Reset risultati precedenti
    onResetResults?.();

    setLoading(true);
    try {
      const response = await api.post('/run/', { 
        code, 
        exercise_id: exerciseId 
      });
      
      if (response.data.task_id) {
        // Non mostrare output, solo dettagli task
        onOutputChange?.(null);
        
        // Mostra dettagli task in pending
        onTaskDetails?.({
          id: response.data.task_id,
          status: 'pending',
          message: 'Task in attesa di esecuzione...'
        });
        
        // Avvia WebSocket per aggiornamenti realtime
        try {
          startTaskWebSocket(response.data.task_id);
        } catch (e) {
          console.error('WebSocket init error:', e);
        }
      } else {
        // Risposta legacy
        onOutputChange?.({
          stdout: response.data.stdout,
          stderr: response.data.stderr
        });
      }
    } catch (error) {
      if (error.response?.status === 402) {
        // Crediti insufficienti - mostra messaggio dedicato
        onOutputChange?.(null);
        onTaskDetails?.({
          id: null,
          status: 'insufficient_credits',
          message: 'Crediti esauriti'
        });
      } else {
        // Altri errori
        const errorMessage = error.message;
        onOutputChange?.({ stdout: '', stderr: errorMessage });
      }
    } finally {
      setLoading(false);
    }
  };

  // WebSocket realtime per risultati task
  const startTaskWebSocket = (taskId) => {
    const base = 'ws://127.0.0.1:8000';
    const socket = new WebSocket(`${base}/ws/tasks/${taskId}/`);

    let closedOrErrored = false;

    socket.onopen = () => {
      // Nessuna azione necessaria all'apertura
    };

    socket.onmessage = async (event) => {
      try {
        const task = JSON.parse(event.data);

        // Task completato
        if ([ 'completed', 'failed', 'interrupted' ].includes(task.status)) {
          onOutputChange?.({
            stdout: task.stdout || '',
            stderr: task.stderr || ''
          });
          onTaskDetails?.(task);

          // Aggiorna crediti
          if (onCreditsUpdate) {
            try {
              const userResponse = await api.get('/user/');
              onCreditsUpdate(userResponse.data.credits);
            } catch (error) {
              console.error('Errore aggiornamento crediti:', error);
            }
          }
          socket.close();
          return;
        }

        // Task in esecuzione/pending - aggiorna dettagli e output incrementale
        if (task.status === 'running' || task.status === 'pending') {
          onOutputChange?.({
            stdout: task.stdout || '',
            stderr: task.stderr || ''
          });
          onTaskDetails?.(task);
        }
      } catch (e) {
        console.error('WebSocket parse error:', e);
      }
    };

    socket.onerror = (err) => {
      closedOrErrored = true;
      console.error('WebSocket error:', err);
      if (socket && socket.readyState !== WebSocket.CLOSED) {
        socket.close();
      }
    };

    socket.onclose = () => {
      if (!closedOrErrored) closedOrErrored = true;
    };
  };

  return (
    <button 
      onClick={handleRun} 
      disabled={loading || !code.trim()}
      className="btn-primary flex items-center px-6 py-3 text-sm font-medium"
    >
      {loading ? (
        <>
          {/* Bottone in esecuzione */}
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Esecuzione in corso...
        </>
      ) : (
        <>
          {/* Bottone esegui codice */}
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Esegui Codice
        </>
      )}
    </button>
  );
}

export default RunButton;

RunButton.propTypes = {
  code: PropTypes.string.isRequired,
  exerciseId: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  onOutputChange: PropTypes.func,
  onTaskDetails: PropTypes.func,
  onCreditsUpdate: PropTypes.func,
  onResetResults: PropTypes.func,
};