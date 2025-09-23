import { useState } from 'react';
import api from '../services/api';

function RunButton({ code }) {
  const [output, setOutput] = useState({ stdout: '', stderr: '' });
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    if (!code) return;

    setLoading(true);
    try {
      const res = await api.post('/run/', { code }); // invia il codice al backend
      setOutput({
        stdout: res.data.stdout,
        stderr: res.data.stderr,
      });
    } catch (err) {
      console.error(err);
      setOutput({ stdout: '', stderr: err.message });
    }
    setLoading(false);
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <button onClick={handleRun} disabled={loading}>
        {loading ? 'Esecuzione...' : 'RUN'}
      </button>

      <div style={{ marginTop: '10px' }}>
        <h4>Output:</h4>
        <pre>{output.stdout}</pre>
        {output.stderr && (
          <>
            <h4>Errori:</h4>
            <pre style={{ color: 'red' }}>{output.stderr}</pre>
          </>
        )}
      </div>
    </div>
  );
}

export default RunButton;
