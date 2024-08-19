import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import SideBar from '../components/SideBar';
import api from '../api';
import '../assets/css/criar.css';
import '../assets/css/geral/styles.css';
import '../assets/css/style.css';
import './criar.css';
import '../assets/css/progresso.css';

const Rewrite = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [tema, setTema] = useState('');
    const [temaEnviado, setTemaEnviado] = useState('');
    const [socket, setSocket] = useState(null);
    const [loading, setLoading] = useState(false);
    const [userId, setUserId] = useState(null);
    const [progress, setProgress] = useState(0);
    const [showInputs, setShowInputs] = useState(true);
    const [currentStep, setCurrentStep] = useState(0);
    const [formData, setFormData] = useState({
        institute: '',
        disciplina: '',
        student: '',
        instructor: '',
        cidade: '',
        idioma: localStorage.getItem('language') || 'Português'
    });
    const [inputValue, setInputValue] = useState('');
    const [texto, setTexto] = useState('');
    const [code, setCode] = useState('');
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [messages, setMessages] = useState([]); // Lista de mensagens
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

    const redirecionar = (code) => {
        navigate(`/thesis/${code}`);
    };

    useEffect(() => {
        const ws = new WebSocket('ws://127.0.0.1:8000/ws/scrib/');
        setSocket(ws);

        ws.onopen = () => {
            console.log('WebSocket connection opened');
        };

        ws.onmessage = function (event) {
            console.log('Message received:', event.data);
            const data = JSON.parse(event.data);

            setMessages((prevMessages) => [...prevMessages, event.data]); // Adiciona a mensagem recebida

            if (data.title) {
                setTitle(data.title);
                setLoading(false);
            }
            if (data.content) {
                setContent(data.content);
                setLoading(false);

                const regex = /<div>([\s\S]*?)<\/div>/;
                const match = data.content.match(regex);
                if (match) {
                    setTexto(match[0]);
                } else {
                    console.log('Div não encontrada.');
                }
            }

            if (data.progress) {
                setProgress(data.progress);
            }
            if (data.code) {
                setCode(data.code);
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setLoading(false);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };

        return () => {
            ws.close();
        };
    }, []);

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleNextStep = () => {
        const stepFields = ['institute', 'disciplina', 'student', 'instructor', 'cidade'];
        const currentField = stepFields[currentStep];

        setFormData({
            ...formData,
            [currentField]: inputValue
        });
        setInputValue('');
        setCurrentStep(currentStep + 1);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        if (tema.trim() === '') {
            alert('Por favor, preencha o campo do Tema.');
            return;
        }

        if (socket && socket.readyState === WebSocket.OPEN) {
            setLoading(true);
            setProgress(0);
            setTemaEnviado(tema);
            setTema('');
            setShowInputs(false);

            const nonEmptyFormData = Object.fromEntries(
                Object.entries(formData).filter(([_, value]) => value.trim() !== '')
            );

            // Inclua o idioma ao enviar os dados
            socket.send(JSON.stringify({
                tema,
                user_id: userId,
                ...nonEmptyFormData
            }));
        }
    };

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    if (progress === 100.00) {
        redirecionar(code);
    }

    return (
        <div className="layout">
            <Header toggleSidebar={toggleSidebar} />
            <SideBar isSidebarOpen={isSidebarOpen} />
            <main className="main-content">
                <div className="adicionar-tema">
                    <div className="progress-container" style={{ display: progress === 0.00 ? 'none' : 'block' }}>
                        <div className="progress-bar" style={{ width: `${progress}%` }}>
                            <p>{`${progress.toFixed(2)}%`}</p>
                        </div>
                    </div>
                    <div className='papel writer'>
                        <div className="capax">
                            <div></div>
                            <div className="SSEMessage">
                                {loading ? <p>Carregando...</p> : <h3>{title}</h3>}
                            </div>
                            <div>
                                <p dangerouslySetInnerHTML={{ __html: texto }}></p>
                            </div>
                        </div>
                    </div>
                    <form onSubmit={handleSubmit} className="form">
                        {showInputs && (
                            <>
                                {currentStep < 5 ? (
                                    <div className="form-group">
                                        <input
                                            type="text"
                                            value={inputValue}
                                            onChange={handleInputChange}
                                            placeholder={['Instituto Medio de Ensino a Distancia', 'Insira nome da Disciplina', 'Insira nome do Aluno', 'Insira nome do Professor', 'Insira nome da sua cidade atual' ][currentStep]}
                                        />
                                        <button type="button" onClick={handleNextStep}>Próximo</button>
                                    </div>
                                ) : (
                                    <div className="form-group">
                                        <input
                                            type="text"
                                            id="tema"
                                            value={tema}
                                            onChange={(e) => setTema(e.target.value)}
                                            placeholder="Digite o tema do trabalho"
                                            required
                                        />
                                        <button type="submit">Enviar</button>
                                    </div>
                                )}
                            </>
                        )}
                    </form>
                    <div className="messages-container">
                        {messages.map((message, index) => (
                            <div key={index} className="message">
                                <p>{message}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Rewrite;
