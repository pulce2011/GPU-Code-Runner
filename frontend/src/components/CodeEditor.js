import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

// Componente editor Monaco per codice C/C++
function CodeEditor({ exercise, onCodeChange }) {
  const [code, setCode] = useState('');

  // Carica template funzione quando cambia esercizio
  useEffect(() => {
    if (exercise) {
      setCode(exercise.signature || '');
    }
  }, [exercise]);

  // Notifica cambiamenti codice al componente padre
  const handleEditorChange = (value) => {
    setCode(value);
    onCodeChange(value);
  };

  // Configurazione editor Monaco
  const editorOptions = {
    fontSize: 14,
    minimap: { enabled: false },
    automaticLayout: true,
    lineNumbers: 'on',
    wordWrap: 'on',
    scrollBeyondLastLine: false,
    padding: { top: 16, bottom: 16 },
    fontFamily: "'Fira Code', 'Consolas', 'Monaco', monospace",
    fontLigatures: true,
  };

  return (
    <div className="space-y-4">

      {/* Consegna esercizio */}
      {exercise?.comment && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-blue-800 mb-1">Consegna</h4>
              <p className="text-sm text-blue-700 whitespace-pre-wrap">{exercise.comment}</p>
            </div>
          </div>
        </div>
      )}

      {/* Informazioni editor */}
      <div className="border border-gray-300 rounded-lg overflow-hidden">
        <div className="bg-gray-50 px-4 py-2 border-b border-gray-300">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <svg className="h-4 w-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              <span className="text-sm font-medium text-gray-700">Editor C/C++</span>
            </div>
            <div className="flex items-center space-x-4 text-xs text-gray-500">
              <span>Monaco Editor</span>
              <span>•</span>
              <span>Syntax Highlighting</span>
            </div>
          </div>
        </div>

        {/* Editor Monaco */}
        <div className="bg-white">
          <Editor
            height="400px"
            language="cpp"
            value={code}
            onChange={handleEditorChange}
            theme="vs-light"
            options={editorOptions}
          />
        </div>
      </div>

      {/* Informazioni codice */}
      <div className="flex items-center justify-between text-sm text-gray-600">
        <div className="flex items-center space-x-4">
          <span className="flex items-center">
            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Linguaggio: C/C++
          </span>
          <span className="flex items-center">
            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Compilazione: GCC
          </span>
        </div>
        <div className="text-xs text-gray-500">
          {code.split('\n').length} righe
        </div>
      </div>
    </div>
  );
}

export default CodeEditor;
