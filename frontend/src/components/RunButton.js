import { useState } from 'react';
import api from '../services/api';

function RunButton({ code, onOutputChange }) {
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    if (!code) return;

    setLoading(true);
    try {
      const res = await api.post('/run/', { code });
      const newOutput = {
        stdout: res.data.stdout,
        stderr: res.data.stderr,
      };
      // Notifica il parent dei risultati
      if (onOutputChange) {
        onOutputChange(newOutput);
      }
    } catch (err) {
      console.error(err);
      const errorOutput = { stdout: '', stderr: err.message };
      if (onOutputChange) {
        onOutputChange(errorOutput);
      }
    }
    setLoading(false);
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
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Esegui Codice
        </>
      )}
    </button>
  );
}

export default RunButton;
