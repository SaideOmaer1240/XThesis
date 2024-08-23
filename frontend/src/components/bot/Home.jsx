import React, { useState, useEffect, useRef } from 'react';
import Sidebar from '../layouts/Sidebar';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../layouts/Navbar';
import SearchInput from "../layouts/Search";
import api from '../../api';
import Message from './Message';
import '../../styles/styles/Global.scss';
import { TransitionGroup, CSSTransition } from 'react-transition-group';

const Home = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId') || null);
  const [sessions, setSessions] = useState([]); 
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState(null);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await api.get('/api/user/info/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const data = response.data;
        setUserId(data.id);
      } catch (error) {
        console.error('Erro ao buscar informações do usuário:', error);
        if (error.response && error.response.status === 401) {
          navigate('/login');
        }
      }
    };

    getUserInfo();
  }, [navigate]);

  useEffect(() => {
    fetchSessions();
    if (sessionId) {
      fetchMessages(sessionId);
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchMessages = async (sessionId) => {
    try {
      const response = await api.post('/api/chat/get_messages/', { session_id: sessionId });
      setMessages(response.data.messages);
    } catch (error) {
      handleApiError(error);
    }
  };

  const fetchSessions = async () => {
    try {
      const response = await api.get('/api/chat/get_sessions/');
      setSessions(response.data.sessions);
    } catch (error) {
      handleApiError(error);
    }
  };

  const handleApiError = (error) => {
    if (error.response && error.response.status === 401) {
      navigate('/login');
    }
    console.error('Error:', error);
  };

  const handleSend = async (text, image, audio) => {
    const newMessages = [...messages, { text, is_user: true }];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    const formData = new FormData();
    formData.append('userId', userId);
    formData.append('message', text);
    if (image) formData.append('image', image);
    if (audio) formData.append('audio', audio, 'recording.webm');
    
    const currentSessionId = sessionId || localStorage.getItem('sessionId') || null;
    if (currentSessionId) formData.append('session_id', currentSessionId);

    try {
      const response = await api.post('/api/chat/chatbot/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSessionId(response.data.session_id);
      localStorage.setItem('sessionId', response.data.session_id);
      setIsLoading(false);
      setMessages((prevMessages) => [
        ...prevMessages, 
        { text: response.data.response, is_user: false }
      ]);
      fetchSessions();
    } catch (error) {
      handleApiError(error);
      setIsLoading(false);
    }
  };

  const startNewConversation = async () => {
    try {
      const response = await api.post('/api/chat/start_new_session/');
      const newSessionId = response.data.session_id;
      setMessages([]);
      setSessionId(newSessionId);
      localStorage.setItem('sessionId', newSessionId);
      fetchSessions();
    } catch (error) {
      handleApiError(error);
    }
  };

  const selectSession = (session_id) => {
    setSessionId(session_id);
    fetchMessages(session_id);
  };

  return (
    <div className='app-styled'>
      <Sidebar   
        sessions={sessions}
        selectSession={selectSession}
        startNewConversation={startNewConversation}
      />
      <div className='home-styled'>
        <Navbar/>
        <div className='content'>
          <div className='chat papel'>
            <div className="chat-container">
              <TransitionGroup>
                {messages.map((msg, index) => (
                  <CSSTransition
                    key={index}
                    timeout={500}
                    classNames="fade"
                  >
                    <Message 
                      text={msg.text} 
                      isUser={msg.is_user}
                    />
                  </CSSTransition>
                ))}
                {isLoading && (
                  <CSSTransition
                    timeout={500}
                    classNames="fade"
                  >
                    <Message 
                      text="Carregando..." 
                      isUser={false}
                    />
                  </CSSTransition>
                )}
              </TransitionGroup>
              <div ref={messagesEndRef}/>
            </div>  
          </div>
        </div>
        <SearchInput
          inputValue={input}
          onInputChange={setInput}
          onSend={handleSend}
          placeholder="Insira uma instrução aqui"
        />
      </div>
    </div>
  );
};

export default Home;
