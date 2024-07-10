import React, { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import Header from "../components/Header";
import SideBar from "../components/SideBar";
import api from "../api";
import "../assets/css/criar.css";
import "../assets/css/geral/styles.css";
import "../assets/css/style.css";
import "./criar.css";
import "./modal.css";
import "../assets/css/progresso.css";
import "../assets/css/book.css"; 
function Thesis() {
  const { topicName } = useParams();
  const [thesis, setThesis] = useState([]);
  const [credentials, setCredentials] = useState([]);

  useEffect(() => {
    const fechCredentials = async() =>{
      /* Obter token de acesso */
      const token = localStorage.getItem('token');
      /* Tentar receber uma resposta */
      try{
        const response = await api.get(
          `/api/author/credentials/?topic_name=${encodeURIComponent(topicName)}`,{
            headers:{
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setCredentials(response.data);
      } catch(error){
        console.error("Erro ao buscar credencias do trabalho:", error);
      }
    };
    fechCredentials();
    const fetchThesis = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get(
          `/api/theses/?topic_name=${encodeURIComponent(topicName)}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setThesis(response.data);
      } catch (error) {
        console.error("Erro ao buscar tese:", error);
      }
    };

    fetchThesis();
  }, [topicName]);

  const handleDownload = async () => {
    const token = localStorage.getItem("token");
    try {
      const response = await api.get(
        `/api/theses/gerar_documento/?topic_name=${encodeURIComponent(
          topicName
        )}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const { file_url } = response.data;
      window.open(file_url); // Abre o link em uma nova aba para download
    } catch (error) {
      const modal = document.getElementById("modal");
      const mbody = document.getElementById("mBody");
      const modalShadows = document.getElementById("modalShadows");
      
      modal.style.display = "flex";
      modalShadows.style.display = "block";
      mbody.innerHTML = `<p>Erro ao baixar documento:${error}</p>`;

      console.error("Erro ao baixar documento", error);
    }
  };

  return (
    <div className="layout">
      <Header />
      <SideBar />
      <main className="main-content">
         
          <div className="views_info A4"> 
            <div className="modal" id="modal">
              <header className="mHeader" id="mHeader">
                 
                <i className="fa fa-exclamation-triangle"></i>
                <p>Token de acesso expirado</p>
              </header>
              <div className="mBody" id="mBody"></div>
              <footer>
                <Link to="/logout">
                  <button>
                    <span className="txt-link">Iniciar Sessão Novamente</span>
                  </button>
                </Link>
              </footer>
            </div>
            <div className="modalShadows" id="modalShadows"></div>
            <div className="papel">
               
              <div className="capax">
                  <div className="conteiner content">
                  <div className="conteiner duble">
                      <h2> {credentials.institute} </h2> 
                      <h2>Trabalho de {credentials.disciplina} </h2>  
                      <h2>Tema: {credentials.topic} </h2>  
                      <div>
                      <h2>Discente: {credentials.student} </h2>
                      <h2>Docente: {credentials.instructor} </h2>
                      </div>
                      <h2>{credentials.city}, {credentials.month} de {credentials.year}</h2>
                  </div>
                  </div>
                </div>
              
                
                {thesis.length > 0 ? (
                  thesis.map((t) => (
                    <div className="conteudo-wrapper">

                      <div className="papel-wrapper">
                    <div key={t.id} className="r">
                      <h3 className="text-2xl font-bold mb-4">{t.title}</h3>
                      <p
                        className="text-gray-700 text-base mb-4"
                        dangerouslySetInnerHTML={{ __html: t.text }}
                      ></p>
                    </div>
                    </div>

                    </div>
                  ))
                ) : (
                  <p className="text-center text-gray-700">
                    Nenhuma tese encontrada para este tópico.
                  </p>
                )}
              

              <div className="text-center mt-6">
                <button onClick={handleDownload} className="downloadBtn">
                  <span>
                    <i
                      className="fa-solid fa-download"
                      style={{ fontSize: "25px" }}
                    ></i>
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
