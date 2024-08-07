import React, { useState, useEffect, useRef } from 'react';
import Sidebar from '../layouts/Sidebar';
import Navbar from '../layouts/Navbar';
import SearchInput from "../layouts/Search";
import api from '../../api';
import Message from './Message';
import '../../styles/styles/Global.scss';
import { TransitionGroup, CSSTransition } from 'react-transition-group'; // Importe os componentes para animação

const Home = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [sessionId, setSessionId] = useState(null);
    const [sessions, setSessions] = useState([]); 
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
  
    useEffect(() => {
      fetchSessions();
      const savedSessionId = localStorage.getItem('sessionId');
      if (savedSessionId) {
        setSessionId(savedSessionId);
        fetchMessages(savedSessionId);
      }
    }, []);
  
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
        console.error('Error fetching messages:', error);
      }
    };
  
    const fetchSessions = async () => {
      try {
        const response = await api.get('/api/chat/get_sessions/');
        setSessions(response.data.sessions);
      } catch (error) {
        console.error('Error fetching sessions:', error);
      }
    };
  
    const handleSend = async () => {
      const newMessages = [...messages, { text: input, is_user: true }];
      setMessages(newMessages);
      setInput('');
      setIsLoading(true);
  
      try {
        const currentSessionId = sessionId || localStorage.getItem('sessionId') || null;
        const response = await api.post('/api/chat/chatbot/', { message: input, session_id: currentSessionId });
        setSessionId(response.data.session_id);
        localStorage.setItem('sessionId', response.data.session_id);
        setIsLoading(false);
        setMessages((prevMessages) => [...prevMessages, { text: response.data.response, is_user: false }]);
        fetchSessions();
      } catch (error) {
        console.error('Error sending message:', error);
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
        console.error('Error starting new conversation:', error);
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
                startNewConversation={startNewConversation} />
        <div className='home-styled'>
            <Navbar/>
            <div className='content' >
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
                placeholder="Ingresa una instrucción aqui"
            />
        </div>

      </div>
        
    )
}

export default Home;
