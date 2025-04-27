import { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from './components/ui/card.js';
import Input from "./components/ui/input.js"; 
import './App.css'; // 👈 Make sure the updated CSS is imported

export default function LlamaChatApp() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null); // 👈 Create a reference to the bottom of chat

  const handleSend = async () => {
    if (!query.trim()) return;
    setQuery('');
    const userMessage = { sender: 'user', message: query };
    setChatHistory(prev => [...prev, userMessage]);
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const data = await res.json();
      const botMessage = { sender: 'bot', message: data.response };
      setChatHistory(prev => [...prev, botMessage]);
    } catch (err) {
      setChatHistory(prev => [...prev, { sender: 'bot', message: 'Error: Unable to get response.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handlechange = (e) => {
    e.preventDefault();
    setQuery(e.target.value);
  };

  // 👇 Auto scroll to bottom when chatHistory or loading changes
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, loading]);

  return (
    <div className="chat-app">

<div className="chat-header-container">
  <h1 className="chat-header">Llama ChatBot</h1>
  <h3 className="chat-tagline">By Group F</h3>
</div>
      <div className="chat-history">
        {chatHistory.map((entry, idx) => (
          <div key={idx} className={`chat-message ${entry.sender}`}>
            <div className="chat-card">
              <div className="chat-card-content">
                <p><strong>{entry.sender === 'user' ? 'You' : 'Bot'}:</strong> {entry.message}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-message bot">
            <div className="chat-card">
              <div className="chat-card-content">
                <div className="loading-dots">
                  <span>.</span>
                  <span>.</span>
                  <span>.</span>
                </div>
              </div>
            </div>
          </div>
        )}
        {/* 👇 Always scrolls to here */}
        <div ref={chatEndRef} />
      </div>

      <div className="chat-input-area">
        <input
          value={query}
          onChange={handlechange}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about politics..."
          className="chat-input"
        />
        <button onClick={handleSend} className="chat-send-button">
          Send
        </button>
      </div>
    </div>
  );
}
