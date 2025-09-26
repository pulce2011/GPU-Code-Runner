import { useState } from 'react';
import api from '../services/api';

// Componente pulsante per esecuzione codice
function RunButton({ code, onOutputChange, onTaskDetails, onCreditsUpdate, exerciseId }) {
  const [loading, setLoading] = useState(false);

  // Esegue codice sul backend
  const handleRun = async () => {
    if (!code || !exerciseId) return;

    setLoading(true);
    try {
      const res = await api.post('/run/', { 
        code: code,
        exercise_id: exerciseId 
      });
      
      // Gestisce la nuova risposta con task_id
      if (res.data.task_id) {
        // Lavoro avviato con successo
        const newOutput = { 
          stdout: `Lavoro avviato con successo!\nTask ID: ${res.data.task_id}\nStatus: ${res.data.status}`,
          stderr: '',
        };
        
        // Notifica risultati al padre
        if (onOutputChange) {
          onOutputChange(newOutput);
        }
        
        // Polling per ottenere i risultati del task (con delay per permettere al backend di salvare)
        setTimeout(() => {
          pollTaskStatus(res.data.task_id);
        }, 1000);
      } else {
        // Risposta legacy (per compatibilità)
        const newOutput = {
          stdout: res.data.stdout,
          stderr: res.data.stderr,
        };
        if (onOutputChange) {
          onOutputChange(newOutput);
        }
      }
    } catch (err) {
      console.error(err);
      let errorMessage = err.message;
      
      // Gestisce errori specifici per crediti insufficienti
      if (err.response?.status === 402) {
        errorMessage = `Crediti insufficienti! Crediti disponibili: ${err.response.data.credits_available}`;
      }
      
      const errorOutput = { stdout: '', stderr: errorMessage };
      if (onOutputChange) {
        onOutputChange(errorOutput);
      }
    }
    setLoading(false);
  };

  // Polling per ottenere i risultati del task
  const pollTaskStatus = async (taskId) => {
    const maxAttempts = 30; // 30 tentativi (30 secondi)
    let attempts = 0;
    
    const poll = async () => {
      try {
        const res = await api.get(`/tasks/${taskId}/`);
        const task = res.data;
        
        if (task.status === 'completed' || task.status === 'failed' || task.status === 'interrupted') {
          // Task completato
          const newOutput = {
            stdout: task.stdout || '',
            stderr: task.stderr || '',
          };
          if (onOutputChange) {
            onOutputChange(newOutput);
          }
          if (onTaskDetails) {
            onTaskDetails(task);
          }
          return;
        }
        
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(poll, 1000); // Riprova dopo 1 secondo
        } else {
          // Timeout
          const timeoutOutput = {
            stdout: '',
            stderr: 'Timeout: impossibile ottenere i risultati del lavoro',
          };
          if (onOutputChange) {
            onOutputChange(timeoutOutput);
          }
        }
      } catch (err) {
        console.error('Errore nel polling del task:', err);
        const errorOutput = {
          stdout: '',
          stderr: 'Errore nel recupero dei risultati del lavoro',
        };
        if (onOutputChange) {
          onOutputChange(errorOutput);
        }
      }
    };
    
    // Inizia il polling dopo 1 secondo
    setTimeout(poll, 1000);
  };

  return (
    <button 
      onClick={handleRun} 
      disabled={loading || !code.trim()}
      className="btn-primary flex items-center px-6 py-3 text-sm font-medium"
    >
      {loading ? (
        <>
          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Esecuzione in corso...
        </>
      ) : (
        <>
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
