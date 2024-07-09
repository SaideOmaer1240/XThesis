// Login.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Form from '../components/FormLogin';

function Login() {
  const navigate = useNavigate();

  const handleSuccess = () => {
    navigate('/rewrite'); // Redirecionar para a rota /rewrite após login bem-sucedido
  };

  return <Form route="/api/token/" method="login" onSuccess={handleSuccess} />;
}

export default Login;
