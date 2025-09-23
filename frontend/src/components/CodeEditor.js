import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

function CodeEditor({ exercise, onCodeChange }) {
  const [code, setCode] = useState('');

  // Aggiorna il codice quando cambia l'esercizio selezionato
  useEffect(() => {
    if (exercise) {
      // Inserisce la firma della funzione + commento (da backend)
      setCode(exercise.signature || '');
    }
  }, [exercise]);

  const handleEditorChange = (value) => {
    setCode(value);
    onCodeChange(value); // notifica il parent
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <Editor
        height="400px"
        language="cpp"
        value={code}
        onChange={handleEditorChange}
        options={{
          fontSize: 14,
          minimap: { enabled: false },
          automaticLayout: true,
        }}
      />
    </div>
  );
}

export default CodeEditor;
