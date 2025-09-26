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
  const [taskDetails, setTaskDetails] = useState(null);
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
    // Se c'è un nuovo output, nascondi i dettagli del task precedente
    if (output) {
      setTaskDetails(null);
    }
  };

  // Gestisce i dettagli del task
  const handleTaskDetails = (details) => {
    setTaskDetails(details);
  };

  // Gestisce aggiornamento crediti
  const handleCreditsUpdate = (newCredits) => {
    setUserInfo(prev => ({
      ...prev,
      credits: newCredits
    }));
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
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-3xl font-semibold text-gray-900 mb-2">
                    Benvenuto, {userInfo.last_name} {userInfo.first_name} <span style={{ fontSize: '14px' }}>[MATR. {userInfo.matr}]</span>
                    {userInfo.is_superuser || userInfo.is_staff ? (
                      <span className="block text-sm text-gray-500 mt-1">
                        Utente amministratore
                      </span>
                    ) : userInfo.course_name && (
                      <span className="block text-sm text-gray-500 mt-1">
                        Corso: {userInfo.course_name}
                      </span>
                    )}
                  </h2>
                </div>
                <div className="bg-gradient-to-r from-slate-50 to-gray-50 border border-slate-200 rounded-xl px-6 py-4 shadow-sm">
                  <div className="flex items-center space-x-3">
                    <div className="bg-slate-100 p-2 rounded-lg">
                      <svg className="w-6 h-6 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                      </svg>
                    </div>
                    <div>
                      <div className="text-xs text-slate-600 font-semibold uppercase tracking-wide">Crediti</div>
                      <div className="text-2xl font-bold text-slate-800">
                        {userInfo.is_superuser || userInfo.is_staff ? (
                          <span className="bg-gradient-to-r from-slate-400 to-gray-400 bg-clip-text text-transparent">
                            ∞
                          </span>
                        ) : (
                          <span className="bg-gradient-to-r from-slate-600 to-gray-600 bg-clip-text text-transparent">
                            {userInfo.credits}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
              <RunButton 
                code={selectedCode} 
                onOutputChange={handleExecutionOutput}
                onTaskDetails={handleTaskDetails}
                onCreditsUpdate={handleCreditsUpdate}
                exerciseId={selectedExercise?.id}
              />
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

              {/* Dettagli Task */}
              {taskDetails && (
                <div>
                  <div className="flex items-center mb-2">
                    <div className="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                    <h4 className="text-sm font-medium text-gray-700">Dettagli Esecuzione</h4>
                  </div>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium text-blue-800">Task ID:</span>
                        <span className="ml-2 text-blue-700">{taskDetails.id}</span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">Stato:</span>
                        <span className={`ml-2 px-2 py-1 rounded text-xs font-medium ${
                          taskDetails.status === 'completed' ? 'bg-green-100 text-green-800' :
                          taskDetails.status === 'failed' ? 'bg-red-100 text-red-800' :
                          taskDetails.status === 'interrupted' ? 'bg-yellow-100 text-yellow-800' :
                          taskDetails.status === 'running' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {taskDetails.status === 'completed' ? 'Completato' :
                            taskDetails.status === 'failed' ? 'Fallito' :
                            taskDetails.status === 'interrupted' ? 'Interrotto' :
                            taskDetails.status === 'running' ? 'In esecuzione' :
                            'In attesa'}
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">Crediti utilizzati:</span>
                        <span className="ml-2 text-blue-700">{taskDetails.credits_cost}</span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">Tempo totale:</span>
                        <span className="ml-2 text-blue-700">
                          {taskDetails.total_execution_time ? 
                            (() => {
                              // Converte la stringa duration in secondi:millisecondi
                              const duration = taskDetails.total_execution_time;
                              if (typeof duration === 'string') {
                                // Formato: "0:00:01.123456" o "0:00:01"
                                const parts = duration.split(':');
                                if (parts.length === 3) {
                                  const hours = parseInt(parts[0]) || 0;
                                  const minutes = parseInt(parts[1]) || 0;
                                  const seconds = parseFloat(parts[2]) || 0;
                                  const totalSeconds = hours * 3600 + minutes * 60 + seconds;
                                  const secs = Math.floor(totalSeconds);
                                  const millisecs = Math.floor((totalSeconds - secs) * 1000);
                                  return `${secs}:${millisecs.toString().padStart(3, '0')}`;
                                }
                              }
                              return 'N/A';
                            })() :
                            'N/A'
                          }
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">Avviato:</span>
                        <span className="ml-2 text-blue-700">
                          {taskDetails.started_at ? 
                            new Date(taskDetails.started_at).toLocaleString('it-IT') : 
                            'N/A'
                          }
                        </span>
                      </div>
                      <div>
                        <span className="font-medium text-blue-800">Completato:</span>
                        <span className="ml-2 text-blue-700">
                          {taskDetails.finished_at ? 
                            new Date(taskDetails.finished_at).toLocaleString('it-IT') : 
                            'N/A'
                          }
                        </span>
                      </div>
                    </div>
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
