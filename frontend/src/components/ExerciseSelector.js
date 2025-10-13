import { useState, useEffect } from 'react';
import api from '../services/api';

// Componente per selezione esercizi dal backend
function ExerciseSelector({ onSelect }) {
  const [exercises, setExercises] = useState([]);
  const [selectedId, setSelectedId] = useState('');
  const [loading, setLoading] = useState(true);

  // Carica esercizi all'avvio
  useEffect(() => {
    const fetchExercises = async () => {
      try {
        setLoading(true);
        const response = await api.get('/exercises/');
        setExercises(response.data);
      } catch (error) {
        console.error('Errore nel recupero esercizi:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchExercises();
  }, []);

  // Gestisce selezione esercizio
  const handleChange = (event) => {
    const id = event.target.value;
    setSelectedId(id);

    const exercise = exercises.find(ex => ex.id.toString() === id);
    onSelect(exercise);
  };

  // Componente loading spinner
  const LoadingSpinner = () => (
    <div className="flex items-center justify-center py-8">
      <div className="flex items-center space-x-2 text-gray-600">
        <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Caricamento esercizi...</span>
      </div>
    </div>
  );

  // Componente messaggio nessun esercizio
  const NoExercisesMessage = () => (
    <div className="text-center py-8 text-gray-500">
      <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p className="mt-2">Nessun esercizio disponibile</p>
    </div>
  );

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="space-y-4">

      {/* Selezione esercizio */}
      <div className="form-group">
        <label htmlFor="exercise-select" className="form-label">
          Seleziona un esercizio
        </label>
        <select 
          id="exercise-select"
          value={selectedId} 
          onChange={handleChange}
          className="input-field"
        >
          <option value="">-- Scegli un esercizio --</option>
          {exercises.map(exercise => (
            <option key={exercise.id} value={exercise.id}>
              {exercise.name} ({exercise.return_type})
            </option>
          ))}
        </select>
      </div>
      
      {/* Messaggio nessun esercizio */}
      {exercises.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p className="mt-2">Nessun esercizio disponibile</p>
        </div>
      )}
    </div>
  );
}

export default ExerciseSelector;
