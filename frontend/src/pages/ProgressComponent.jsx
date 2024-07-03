import React, { useEffect, useState } from 'react';
import '../assets/css/progress.css';  // Importando o arquivo de estilo

const ProgressComponent = ({tema}) => {
    const [progressMessages, setProgressMessages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const socket = new WebSocket('ws://127.0.0.1:8000/ws/progress/');

        socket.onopen = () => {
            console.log('WebSocket connected');
            socket.send(JSON.stringify({ tema}));
            setLoading(false);
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setProgressMessages((prevMessages) => [...prevMessages, data.message]);
        };

        socket.onerror = (err) => {
            console.error('WebSocket error:', err);
            setError('Erro na conexão com o WebSocket');
            setLoading(false);
        };

        socket.onclose = () => {
            console.log('WebSocket disconnected');
        };

        return () => socket.close();
    }, [tema]);

    return (
        <div className="progress-container">
            <h2>Atualizações de Progresso</h2>
            {loading && <p>Conectando ao WebSocket...</p>}
            {error && <div className="error-message">{error}</div>}
            <ul>
                {progressMessages.map((message, index) => (
                    <li key={index}>{message}</li>
                ))}
            </ul>
        </div>
    );
};

export default ProgressComponent;
