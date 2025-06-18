import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/chat/mood';
const MoodSelector = () => {
  const [mood, setMood] = useState('');
  const [message, setMessage] = useState('');

  const moods = ['happy', 'sad', 'stressed', 'excited'];

  
  const handleMoodSubmit = async () => {
    if (!mood) {
        console.log("Entered MoodSelector component");
      setMessage('Please select a mood.');
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/chat/mood`, { mood });
      setMessage(`Mood recorded: ${response.data.mood}`);
    } catch (error) {
      console.error('Error recording mood:', error);
      setMessage('Error: Could not record mood');
    }
  };

  return (
    <div style={styles.container}>
      <h3>Select Your Mood</h3>
      <select
        value={mood}
        onChange={(e) => setMood(e.target.value)}
        style={styles.select}
      >
        <option value="">-- Select Mood --</option>
        {moods.map((m) => (
          <option key={m} value={m}>
            {m.charAt(0).toUpperCase() + m.slice(1)}
          </option>
        ))}
      </select>
      <button onClick={handleMoodSubmit} style={styles.button}>
        Submit Mood
      </button>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

const styles = {
  container: {
    margin: '20px 0',
    padding: '10px',
    border: '1px solid #ccc',
    borderRadius: '8px',
  },
  select: {
    padding: '8px',
    marginRight: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  message: {
    marginTop: '10px',
    color: '#333',
  },
};

export default MoodSelector;