import React, { useState, useRef, useEffect } from 'react';
import { Mic, Send, Bot, User, Volume2, Globe } from 'lucide-react';
import apiClient from '../api/client';

export default function Assistant() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am Agri, your AI agronomist. How can I help you with your farm today?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState('en');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    try {
      const res = await apiClient.post('/ai-assistant/chat', { 
        message: userMsg.text, 
        language 
      });
      
      if (res.data && res.data.reply) {
        setMessages(prev => [...prev, { sender: 'bot', text: res.data.reply }]);
      } else {
        console.error("AI Assistant Error: no reply field");
        setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I got an unexpected response.' }]);
      }
    } catch (err) {
      console.error("Fetch Error:", err);
      setMessages(prev => [...prev, { sender: 'bot', text: err.response?.data?.detail || 'Sorry, a network error occurred.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  const recognitionRef = useRef(null);

  const toggleListen = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Your browser does not support speech recognition.');
      return;
    }

    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = language === 'hi' ? 'hi-IN' : language === 'mr' ? 'mr-IN' : 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  return (
    <div className="assistant-container">
      <div className="assistant-header">
        <div className="assistant-title-group">
          <div className="bot-avatar header-avatar">
            <Bot size={28} />
          </div>
          <div>
            <h2>Agri AI</h2>
            <p>Your Personal Agronomist</p>
          </div>
        </div>
        
        <div className="language-selector">
          <Globe size={18} />
          <select value={language} onChange={e => setLanguage(e.target.value)}>
            <option value="en">English</option>
            <option value="hi">हिंदी (Hindi)</option>
            <option value="mr">मराठी (Marathi)</option>
          </select>
        </div>
      </div>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.sender}`}>
            <div className={`chat-bubble ${msg.sender}`}>
              {msg.sender === 'bot' && <Volume2 size={16} className="tts-icon" />}
              <p>{msg.text}</p>
            </div>
            {msg.sender === 'user' ? (
              <div className="user-avatar"><User size={20} /></div>
            ) : null}
          </div>
        ))}
        
        {isTyping && (
          <div className="chat-message bot">
            <div className="chat-bubble bot typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <button 
          className={`mic-btn ${isListening ? 'listening' : ''}`}
          onClick={toggleListen}
          title="Speak to Agri"
        >
          <Mic size={24} />
        </button>
        <input 
          type="text" 
          placeholder="Ask about your crops, soil, or pests..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button className="send-btn" onClick={handleSend} disabled={!input.trim()}>
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
