import { useState, useEffect } from 'react';
import api from '../services/api';

function ExerciseSelector({ onSelect }) {
  const [exercises, setExercises] = useState([]);
  const [selectedId, setSelectedId] = useState('');

  // Recupera la lista degli esercizi all'avvio del componente
  useEffect(() => {
    const fetchExercises = async () => {
      try {
        const res = await api.get('/exercises/'); // GET protetta con access token
        setExercises(res.data);
      } catch (err) {
        console.error('Errore nel recupero esercizi:', err);
      }
    };

    fetchExercises();
  }, []);

  // Quando l'utente seleziona un esercizio
  const handleChange = (e) => {
    const id = e.target.value;
    setSelectedId(id);

    const exercise = exercises.find(ex => ex.id.toString() === id);
    onSelect(exercise); // passa l'esercizio selezionato al parent
  };

  return (
    <div>
      <label>Seleziona esercizio: </label>
      <select value={selectedId} onChange={handleChange}>
        <option value="">-- Scegli un esercizio --</option>
        {exercises.map(ex => (
          <option key={ex.id} value={ex.id}>
            {ex.name} ({ex.return_type})
          </option>
        ))}
      </select>
    </div>
  );
}

export default ExerciseSelector;
