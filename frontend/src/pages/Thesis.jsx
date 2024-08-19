import React, { useState, useEffect } from "react";
import { Link, useParams, useNavigate  } from "react-router-dom";
import Header from "../components/Header";
import { Download } from 'phosphor-react';
import SideBar from "../components/SideBar";
import api from "../api";
import "../assets/css/criar.css";
import "../assets/css/geral/styles.css";
import "../assets/css/style.css";
import "./criar.css";
import "./modal.css";
import "../assets/css/progresso.css";
import "../assets/css/book.css";
import  LoadingAnimation from  "../components/LoadingAnimation";
function Thesis() {
  const { code } = useParams();
  const [thesis, setThesis] = useState([]);
  const [credentials, setCredentials] = useState({});
  const [modalMessage, setModalMessage] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); 
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCredentials = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/api/author/credentials/?code=${encodeURIComponent(code)}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setCredentials(response.data);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          navigate('/login');
      }
        console.error("Erro ao buscar credenciais do trabalho:", error);
      }
    };

    const fetchThesis = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(`/api/theses/?code=${encodeURIComponent(code)}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setThesis(response.data);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          navigate('/login');
      }
        console.error("Erro ao buscar tese:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCredentials();
    fetchThesis();
  }, [code]);

  const handleDownload = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.get(`/api/theses/gerar_documento/?code=${encodeURIComponent(code)}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: response.data.type });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${credentials.topic}.docx`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      let errorMessage;

      if (error.response) {
        switch (error.response.status) {
          case 404:
            errorMessage = 'Arquivo não encontrado: O documento solicitado não está disponível.';
            break;
          case 401:
            errorMessage = 'Não autorizado: Você não tem permissão para acessar este documento.';
            break;
          default:
            errorMessage = `Erro ao baixar documento: ${error.message || 'Erro desconhecido.'}`;
        }
      } else if (error.request) {
        errorMessage = 'Erro de rede: Verifique sua conexão com a internet.';
      } else {
        errorMessage = `Erro ao baixar documento: ${error.message || 'Erro desconhecido.'}`;
      }

      setModalMessage(errorMessage);
      setShowModal(true);
      console.error("Erro ao baixar documento", error);
    }
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="layout">
      <Header toggleSidebar={toggleSidebar} />
      <SideBar isSidebarOpen={isSidebarOpen} />
      <main className="main-content">
        <div className="views_info A4">
          {showModal && (
            <>
              <div className="modal" id="modal">
                <header className="mHeader">
                  <i className="fa fa-exclamation-triangle"></i>
                  <p>Token de acesso expirado</p>
                </header>
                <div className="mBody">
                  <p>{modalMessage}</p>
                </div>
                <footer>
                  <Link to="/logout">
                    <button>
                      <span className="txt-link">Iniciar Sessão Novamente</span>
                    </button>
                  </Link>
                </footer>
              </div>
              <div className="modalShadows" id="modalShadows" style={{ display: 'block' }}></div>
            </>
          )}
          <div className="papel">
            {!loading && (
              <div className="capax">
                <div className="conteiner content">
                  <div className="conteiner duble">
                    <h2>{credentials.institute}</h2>
                    <h2>Trabalho de {credentials.disciplina}</h2>
                    <h2>Tema: {credentials.topic}</h2>
                    <div>
                      <h2>Discente: {credentials.student}</h2>
                      <h2>Docente: {credentials.instructor}</h2>
                    </div>
                    <h2>{credentials.city}, {credentials.month} de {credentials.year}</h2>
                  </div>
                </div>
              </div>
            )}

            {loading ? (
              <div><LoadingAnimation/></div>
            ) : thesis.length > 0 ? (
              thesis.map((t) => (
                <div key={t.id} className="conteudo-wrapper">
                  <div className="papel-wrapper">
                    <div className="r">
                      <h3 className="text-2xl font-bold mb-4">{t.title}</h3>
                      <p className="text-gray-700 text-base mb-4" dangerouslySetInnerHTML={{ __html: t.text }}></p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-center text-gray-700">Nenhuma tese encontrada para este tópico.</p>
            )}

            <div className="text-center mt-6">
              <button onClick={handleDownload} className="downloadBtn">
                <span>
                   <Download weight="bold" size={28}/>
                </span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Thesis;
