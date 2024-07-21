import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"; 
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [usernameMessage, setUsernameMessage] = useState("");
    const [emailMessage, setEmailMessage] = useState("");
    const [isUsernameAvailable, setIsUsernameAvailable] = useState(true);
    const [isEmailAvailable, setIsEmailAvailable] = useState(true);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Não permitir submissão se o email ou nome de usuário não estiver disponível
        if (!isUsernameAvailable || !isEmailAvailable) {
            alert("Por favor, corrija os erros antes de enviar o formulário.");
            return;
        }

        setLoading(true);

        try {
            const res = await api.post(route, { username, email, password });
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/rewrite");
            } else {
                navigate("/login");
            }
        } catch (error) {
            alert("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.");
        } finally {
            setLoading(false);
        }
    };

    const checkAvailability = async (type, value) => {
        try {
            const res = await api.get(`/api/check-availability/?${type}=${value}`);
            if (res.data[type]) {
                if (type === "email") {
                    setEmailMessage(res.data[type]);
                    setIsEmailAvailable(false);
                } else {
                    setUsernameMessage(res.data[type]);
                    setIsUsernameAvailable(false);
                }
            } else {
                if (type === "email") {
                    setEmailMessage("");
                    setIsEmailAvailable(true);
                } else {
                    setUsernameMessage("");
                    setIsUsernameAvailable(true);
                }
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => {
                    setUsername(e.target.value);
                    checkAvailability("username", e.target.value);
                }}
                placeholder="Username"
            />
            <div id="usernameMessage" className="availability-message">{usernameMessage}</div>
            {method === "register" && (
                <>
                    <input
                        className="form-input"
                        type="email"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                            checkAvailability("email", e.target.value);
                        }}
                        placeholder="E-mail"
                    />
                    <div id="emailMessage" className="availability-message">{emailMessage}</div>
                </>
            )}
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit" disabled={!isUsernameAvailable || !isEmailAvailable}>
                {name}
            </button>
        </form>
    );
}

export default Form;
