import { useState } from 'react';
import axios from 'axios';

interface Message {
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

export function ChatBox() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSend = async () => {
    if (!query.trim()) return;

    const userMessage: Message = {
      type: 'user',
      content: query,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    
    try {
      const res = await axios.post('http://localhost:8000/chat', { query });
      
      const botMessage: Message = {
        type: 'bot',
        content: res.data.response,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
      setQuery('');
    } catch (err) {
      setError('Failed to get response. Make sure the backend is running on port 8000.');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={{ 
      maxWidth: '800px', 
      margin: '0 auto', 
      padding: '20px',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Chat Messages */}
      <div style={{
        border: '1px solid #ddd',
        borderRadius: '8px',
        height: '400px',
        overflowY: 'auto',
        padding: '10px',
        marginBottom: '20px',
        backgroundColor: '#f9f9f9'
      }}>
        {messages.length === 0 ? (
          <div style={{ color: '#666', textAlign: 'center', marginTop: '150px' }}>
            Ask a question about the RTI Act
          </div>
        ) : (
          messages.map((message, index) => (
            <div 
              key={index}
              style={{
                marginBottom: '15px',
                padding: '10px',
                borderRadius: '8px',
                backgroundColor: message.type === 'user' ? '#007bff' : '#fff',
                color: message.type === 'user' ? 'white' : '#333',
                marginLeft: message.type === 'user' ? '20%' : '0',
                marginRight: message.type === 'user' ? '0' : '20%',
                border: message.type === 'bot' ? '1px solid #ddd' : 'none'
              }}
            >
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                {message.type === 'user' ? 'You' : 'Legal Assistant'}
              </div>
              <div style={{ whiteSpace: 'pre-wrap' }}>{message.content}</div>
              <div style={{ 
                fontSize: '12px', 
                opacity: 0.7, 
                marginTop: '5px' 
              }}>
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div style={{ textAlign: 'center', color: '#666' }}>
            <div>Legal Assistant is typing...</div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div style={{
          backgroundColor: '#f8d7da',
          color: '#721c24',
          padding: '10px',
          borderRadius: '4px',
          marginBottom: '10px',
          border: '1px solid #f5c6cb'
        }}>
          {error}
        </div>
      )}

      {/* Input Section */}
      <div style={{ display: 'flex', gap: '10px' }}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the RTI Act..."
          disabled={isLoading}
          style={{
            flex: 1,
            minHeight: '60px',
            padding: '10px',
            borderRadius: '4px',
            border: '1px solid #ddd',
            fontSize: '14px',
            resize: 'vertical'
          }}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !query.trim()}
          style={{
            padding: '10px 20px',
            backgroundColor: isLoading || !query.trim() ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading || !query.trim() ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            height: 'fit-content'
          }}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
