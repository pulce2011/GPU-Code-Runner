import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ExerciseSelector from '../components/ExerciseSelector';
import CodeEditor from '../components/CodeEditor';
import RunButton from '../components/RunButton';
import { useAuth } from '../hooks/useAuth';
import api from '../services/api';

// Pagina principale dashboard con editor e esecuzione codice
function DashboardPage() {
  const [selectedExercise, setSelectedExercise] = useState(null);
  const [selectedCode, setSelectedCode] = useState('');
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [executionOutput, setExecutionOutput] = useState(null);
  const navigate = useNavigate();
  const { logout } = useAuth();

  // Carica informazioni utente all'avvio
  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await api.get('/user/');
        setUserInfo(response.data);
      } catch (error) {
        console.error('Errore nel recupero informazioni utente:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, []);

  // Gestisce logout e redirect
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Gestisce output esecuzione codice
  const handleExecutionOutput = (output) => {
    setExecutionOutput(output);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header con logout */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">GPU Code Runner</h1>
            </div>
            <button 
              onClick={handleLogout}
              className="btn-danger flex items-center"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          {loading ? (
            <div className="flex items-center space-x-2">
              <svg className="animate-spin h-5 w-5 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span className="text-gray-600">Caricamento...</span>
            </div>
          ) : userInfo ? (
            <>
              <h2 className="text-3xl font-semibold text-gray-900 mb-2">
                Benvenuto, {userInfo.last_name} {userInfo.first_name} <span style={{ fontSize: '14px' }}>[MATR. {userInfo.matr}]</span>
                {userInfo.is_superuser ? (
                  <span className="block text-sm text-gray-500 mt-1">
                    Utente amministratore
                  </span>
                ) : userInfo.course_name && (
                  <span className="block text-sm text-gray-500 mt-1">
                    Corso: {userInfo.course_name}
                  </span>
                )}
              </h2>
            </>
          ) : (
            <>
              <h2 className="text-3xl font-semibold text-gray-900 mb-2">Benvenuto!</h2>
              <p className="text-lg text-gray-600">Seleziona un esercizio di programmazione per iniziare</p>
            </>
          )}
        </div>

        {/* Selezione esercizi */}
        <div className="mb-8">
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Seleziona Esercizio</h3>
            <ExerciseSelector onSelect={setSelectedExercise} />
          </div>
        </div>

        {/* Editor e esecuzione */}
        {selectedExercise && (
          <>
            {/* Editor Monaco */}
            <div className="card mb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Editor di Codice</h3>
              <CodeEditor
                exercise={selectedExercise}
                onCodeChange={setSelectedCode}
              />
            </div>

            {/* Pulsante esecuzione */}
            <div className="flex justify-end mb-8">
              <RunButton code={selectedCode} onOutputChange={handleExecutionOutput} />
            </div>
          </>
        )}

        {/* Risultati esecuzione */}
        {executionOutput && (executionOutput.stdout || executionOutput.stderr) && (
          <div className="card">
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Risultato Esecuzione
            </h3>
            
            <div className="space-y-4">
              {/* Output standard */}
              {executionOutput.stdout && (
                <div>
                  <div className="flex items-center mb-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                    <h4 className="text-sm font-medium text-gray-700">Output</h4>
                  </div>
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono">{executionOutput.stdout}</pre>
                  </div>
                </div>
              )}

              {/* Output errori */}
              {executionOutput.stderr && (
                <div>
                  <div className="flex items-center mb-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                    <h4 className="text-sm font-medium text-gray-700">Errori</h4>
                  </div>
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                    <pre className="text-sm text-red-800 whitespace-pre-wrap font-mono">{executionOutput.stderr}</pre>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default DashboardPage;
