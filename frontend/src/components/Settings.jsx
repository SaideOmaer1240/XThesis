import { Link } from "react-router-dom";
import SideBar from "./SideBar";
import Header from "./Header";
import React, { useState, useEffect } from "react";
import api from "../api";
import "../assets/css/settings.css";
function Settings() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [user_info, setUserInfo] = useState(false);
  const [user_data, setUserData] = useState([]);
  useEffect(() => {
    const fetchUser = async () => {
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
    fetchUser();

    const fetchAthor = async () => {
        // Tente obter resposta
        try {
          const response = await api.get("/api/view/user-data/");
          setUserData(response.data);
        } catch (error) {
          // Pegar (catch) o erro, caso falhe na tentativa de obter a resposta
          console.log("Erro ao obter a resposta: ", error);
        }
      };
      // Inicializar a função
      fetchAthor();
  }, []);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  return (
    <div className="layout">
      <Header toggleSidebar={toggleSidebar} />
      <SideBar isSidebarOpen={isSidebarOpen} />

      <main className="main-content">
        <div className="setting conteiner papel">
          <div className="conteiner-settings">
            <div className="settings user data">
              <h2>Predefinir dados de Autor do trabalho</h2>
              <p>
                {" "}
                <strong>Administrador da conta: </strong>
                {user_info.username}{" "}
              </p>
              <footer>
                <li>
                  <Link to={"/create/user/data"}>
                    <span className="text-link">Predefinir</span>
                  </Link>
                </li>
              </footer>
            </div>

            <div className="settings user plan">
              <h2>Precificação</h2>
              <p>
                {" "}
                <strong>Plano atual: </strong>Gratis
              </p>
              <footer>
                <li>
                  <Link to={"/user/data"}>
                    <span className="text-link">Atualizar</span>
                  </Link>
                </li>
              </footer>
            </div>

            <div className="settings  user update-data">
              <h2>Atualizar dados de Autor do trabalho</h2>
              <p>
                {" "}
                <strong>Autor: </strong>
                {user_data.aluno}
              </p>
              <footer>
                <li>
                  <Link to={"/edit/user/data"}>
                    <span className="text-link">Atualizar</span>
                  </Link>
                </li>
              </footer>
            </div>

            <div className="settings user data right">
              <h2>Trabalhos Total</h2>
              <p>
                {" "}
                <strong>Total: </strong>
                {user_data.amount} 
              </p>
              <footer>
                <li>
                  <Link to={"/topic"}>
                    <span className="text-link">Visualizar</span>
                  </Link>
                </li>
              </footer>
            </div>
          </div>
          <div className="user-data-info papel">
            <div className="data-info papel">
              <p><strong>Nome de usuario: </strong>{user_info.username}</p>
              <p><strong>E-mail: </strong>{user_info.email}</p>
              <p><strong>Nome predefinido: </strong>{user_data.aluno}</p>
              <p><strong>Nome do professor predefinido: </strong>{user_data.professor}</p> 
              <p><strong>Nome da Disciplina predefinida: </strong>{user_data.disciplina}</p>
              <p><strong>Instituto: </strong>{user_data.instituto}</p>
              <p><strong>Cidade: </strong>{user_data.cidade}</p>
              <p><strong>Data de adessão: </strong>{user_info.enjoined}</p> 
            </div>
            <div className="total thessis"></div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Settings;
