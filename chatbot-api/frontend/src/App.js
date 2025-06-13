import React from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow.js';
import MoodSelector from './components/MoodSelector.js';

function App() {
  return (
    <div className="App">
      <h1>Chatbot App</h1>
      <MoodSelector />
      <ChatWindow />
    </div>
  );
}

export default App;