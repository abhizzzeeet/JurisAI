import React from 'react';
import './App.css';
import { ChatBox } from './components/ChatBox';

function App() {
  return (
    <div style={{ 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      padding: '20px 0'
    }}>
      <header style={{
        textAlign: 'center',
        marginBottom: '30px',
        padding: '20px'
      }}>
        <h1 style={{
          color: '#333',
          fontSize: '2.5rem',
          marginBottom: '10px'
        }}>
          Legal Query Chatbot
        </h1>
        <p style={{
          color: '#666',
          fontSize: '1.1rem'
        }}>
          Ask questions about the Right to Information (RTI) Act
        </p>
      </header>
      <ChatBox />
    </div>
  );
}

export default App;
