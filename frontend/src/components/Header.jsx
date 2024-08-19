import api from "../api";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Header({ toggleSidebar }) {
  const [user_info, setUserInfo] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState("Português"); // Default para português

  useEffect(() => {
    const fetchUserInfo = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get("/api/user/info/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUserInfo(response.data);
      } catch (error) {
        console.error("Erro ao obter dados do usuario:", error);
      }
    };

    // Carregar a preferência de idioma do localStorage
    const language = localStorage.getItem("language") || "Português";
    setSelectedLanguage(language);

    fetchUserInfo();
  }, []);

  useEffect(() => {
    // Atualizar a interface ou executar qualquer lógica adicional aqui
    console.log("Idioma selecionado:", selectedLanguage);
  }, [selectedLanguage]);

  const handleLanguageChange = (event) => {
    const newLanguage = event.target.value;
    setSelectedLanguage(newLanguage);
    localStorage.setItem("language", newLanguage);

    // Aqui você pode implementar a lógica para atualizar a interface com base no idioma selecionado
  };

  return (
    <header className="navbar">
      <div className="logo">
        <Link to="/" className="marca">
          <h1>ReprografIA</h1>
        </Link>
      </div>
      <div className="conteiner_list">
        <ul className="lists">
          <li className="list username" style={{ marginRight: "20px" }}>
            {user_info.username}
          </li>
          <li className="list logout">
            <Link to="/logout">
              <span className="txt-link">Sair</span>
              <span>
                <i
                  className="fa-solid fa-sign-out-alt"
                  style={{ fontSize: "25px" }}
                ></i>
              </span>
            </Link>
          </li>
          <li className="list language-selector">
            <select
              value={selectedLanguage}
              onChange={handleLanguageChange}
              style={{ fontSize: "16px", marginLeft: "20px" }}
            >
              <option value="Português">Português</option>
              <option value="Inglês">Inglês</option>
              <option value="Francês">Francês</option>
              <option value="Espanhol">Espanhol</option> 
              <option value="Alemão">Alemão</option>
              {/* Adicione outros idiomas conforme necessário */}
            </select>
          </li>
        </ul>
      </div>
      <div className="btn-expandir" onClick={toggleSidebar}>
        <i className="fa-solid fa-bars" id="btn-exp" style={{ fontSize: '29px' }}></i>
      </div>
    </header>
  );
}

export default Header;
