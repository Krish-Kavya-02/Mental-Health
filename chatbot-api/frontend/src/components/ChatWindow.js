import { useState } from 'react';
import axios from 'axios';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to the chat
    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);

    try {
      // Send message to the backend
      const response = await axios.post('http://localhost:3000/api/chat', { message: input });
      const botMessage = { sender: 'bot', text: response.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { sender: 'bot', text: 'Error: Could not get response' };
      setMessages((prev) => [...prev, errorMessage]);
    }

    // Clear input
    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div style={styles.chatContainer}>
      <div style={styles.messageContainer}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              textAlign: msg.sender === 'user' ? 'right' : 'left',
              color: msg.sender === 'user' ? '#007bff' : '#333',
            }}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          style={styles.input}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '10px',
    height: '400px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    marginTop: '20px',
  },
  messageContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '10px',
  },
  message: {
    margin: '5px 0',
    padding: '8px',
    borderRadius: '5px',
    backgroundColor: '#f0f0f0',
    maxWidth: '70%',
    display: 'inline-block',
  },
  inputContainer: {
    display: 'flex',
    gap: '10px',
    padding: '10px',
  },
  input: {
    flex: 1,
    padding: '8px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '8px 16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default ChatWindow;