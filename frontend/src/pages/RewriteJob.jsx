import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import SideBar from '../components/SideBar';
import api from '../api';
import '../assets/css/criar.css';
import '../assets/css/geral/styles.css';
import '../assets/css/style.css';
import './criar.css'; 
import '../assets/css/progresso.css';

const Rewrite = () => {
    const [title, setTitle] = useState('' );
    const [content, setContent] = useState('');
    const [tema, setTema] = useState('');
    const [temaEnviado, setTemaEnviado] = useState('');
    const [socket, setSocket] = useState(null);
    const [loading, setLoading] = useState(false);
    const [userId, setUserId] = useState(null);
    const [progress, setProgress] = useState(0);
    const [showInputs, setShowInputs] = useState(true);
    const [institute, setInstitute] = useState('');
    const [disciplina, setDisciplina] = useState('');
    const [student, setStudent] = useState('');
    const [instructor, setInstructor] = useState('');
    const [cidade, setCidade] = useState('');

    // useEffect para obter informações do usuário ao carregar o componente
    useEffect(() => {
        const getUserInfo = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await api.get('/api/user/info/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.data;
                setUserId(data.id);
            } catch (error) {
                console.error('Erro ao buscar informações do usuário:', error);
            }
        };

        getUserInfo();
    }, []);

    // useEffect para configurar a conexão WebSocket ao carregar o componente
    useEffect(() => {
        const ws = new WebSocket('ws://127.0.0.1:8000/ws/scrib/');
        setSocket(ws);

        ws.onopen = () => {
            console.log('WebSocket connection opened');
        };

        ws.onmessage = function(event) {
            console.log('Message received:', event.data);
            const data = JSON.parse(event.data);

            if (data.title) {
                setTitle(data.title);
                setLoading(false);  // Para o carregamento quando recebe o título
            }
            if (data.content){
                setContent(data.content);
                setLoading(false);
            }

            if (data.progress) {
                setProgress(data.progress);  // Atualiza o progresso
            }
        };
         
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setLoading(false);  // Para o carregamento em caso de erro
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };

        // Limpa a conexão WebSocket quando o componente é desmontado
        return () => {
            ws.close();
        };
    }, []);

    // Função para lidar com o envio do formulário
    const handleSubmit = (event) => {
        event.preventDefault();
        if (socket && socket.readyState === WebSocket.OPEN) {
            setLoading(true);  // Mostra que está carregando
            setProgress(0);  // Reseta o progresso ao enviar um novo tema
            setTemaEnviado(tema);  // Armazena o tema enviado
            setTema('');  // Reseta o input do tema
            setShowInputs(false);  // Esconde os outros inputs
    
            socket.send(JSON.stringify({
                tema,
                user_id: userId,
                institute,
                disciplina,
                student,
                instructor,
                cidade
            }));
        }
    };
    

    return (
        <div className="layout">
            <Header />
            <SideBar />
            <main className="main-content">
                <div className="adicionar-tema">
                    {/* Mantém o tema enviado no título */}
                    <h2>{temaEnviado ? temaEnviado : 'Adicione o Tema da Monografia'}</h2>
                    <div className="views_info">
                        <div className="progress-container">
                            {/* Barra de progresso */}
                            <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                            <p>{`Progresso: ${progress.toFixed(2)}%`}</p>
                        </div>
                        <div className="SSEMessage">
                            {/* Mensagem de carregamento ou título recebido */}
                            {loading ? <p>Carregando...</p> : <h3>{title}</h3>}
                        </div>
                        <div>
                        {loading ? <p>Carregando...</p> : <h3>{content}</h3>}
                        </div>
                    </div>
                    <form onSubmit={handleSubmit} className="form">
                        {showInputs && (
                            <>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        value={institute}
                                        onChange={(e) => setInstitute(e.target.value)}
                                        placeholder="Instituto"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        value={disciplina}
                                        onChange={(e) => setDisciplina(e.target.value)}
                                        placeholder="Disciplina"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        value={student}
                                        onChange={(e) => setStudent(e.target.value)}
                                        placeholder="Aluno"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        value={instructor}
                                        onChange={(e) => setInstructor(e.target.value)}
                                        placeholder="Orientador"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <input
                                        type="text"
                                        value={cidade}
                                        onChange={(e) => setCidade(e.target.value)}
                                        placeholder="Cidade"
                                        required
                                    />
                                </div>
                            </>
                        )}
                        <div className="form-group">
                            <input
                                type="text"
                                id="tema"
                                value={tema}
                                onChange={(e) => setTema(e.target.value)}
                                placeholder="Digite o tema da monografia"
                                required
                            />
                        </div>
                        <button type="submit">Enviar</button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default Rewrite;
