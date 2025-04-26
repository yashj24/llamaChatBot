import { useState } from 'react';
import { Card, CardContent } from './components/ui/card.js';
import Input from  "./components/ui/input.js"; 

export default function LlamaChatApp() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    console.log("sesebfghesvf")
    
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
      setQuery('');
    } catch (err) {
      setChatHistory(prev => [...prev, { sender: 'bot', message: 'Error: Unable to get response.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-4">
      <h1 className="text-2xl font-bold mb-4">LLaMA Politics Chatbot</h1>
      <div className="space-y-2 max-h-[400px] overflow-y-auto mb-4">
        {chatHistory.map((entry, idx) => (
          <Card key={idx} className={entry.sender === 'user' ? 'bg-blue-100' : 'bg-gray-100'}>
            <CardContent className="p-3">
              <p><strong>{entry.sender === 'user' ? 'You' : 'Bot'}:</strong> {entry.message}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      <div className="flex gap-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a question about politics..."
        />
        <button onClick={handleSend} > Click Me  </button>
      </div>
    </div>
  );
}
