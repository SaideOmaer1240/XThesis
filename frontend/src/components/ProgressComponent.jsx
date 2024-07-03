// ProgressComponent.js
import React, { useState, useEffect } from 'react';

const ProgressComponent = ({ tema }) => {
  const [progress, setProgress] = useState([]);
  const [error, setError] = useState(null);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    if (tema && ws) {
      ws.send(JSON.stringify({ tema }));
    }
  }, [tema, ws]);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws/progress/');
    setWs(websocket);

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress((prevProgress) => [...prevProgress, data.message]);
    };

    websocket.onerror = (error) => {
      setError('WebSocket error');
    };

    websocket.onclose = () => {
      console.log('WebSocket closed');
    };

    return () => {
      websocket.close();
    };
  }, []);

  return (
    <div className="progress-component">
      {progress.map((message, index) => (
        <div key={index} className="progress-message">
          {message}
        </div>
      ))}
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default ProgressComponent;
