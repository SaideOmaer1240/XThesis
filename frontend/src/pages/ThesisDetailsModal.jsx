import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import Header from "../components/Header";
import SideBar from "../components/SideBar";
import "../assets/css/criar.css";
import "../assets/css/geral/styles.css";
import "../assets/css/style.css";
import "./criar.css";
import "../assets/css/progresso.css";
import "../assets/css/cards.css";
import "../assets/css/book.css";
function TopicList() {
  const [topics, setTopics] = useState([]);
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); 

  useEffect(() => {
    const fetchTopics = async () => {
      const token = localStorage.getItem("token");
      try {
        const response = await api.get("/api/topics/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTopics(response.data);
      } catch (error) {
        console.error("Erro ao buscar tópicos:", error);
      }
    };

    fetchTopics();
  }, []);

  const handleViewThesis = (topicId) => {
    navigate(`/thesis/${topicId}`);
  };

  const destroyThesis = (topicId) => {
    navigate(`/delete/${topicId}`);
  };
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
};

  return (
    <div className="layout">
      <div className="confirmar-exclusao">
        <h2 className="se-confir-exlusao">Deseja realimente excluir esse trabalho?</h2>
        <p className="confirmo-sim">Essa decisão resultará na perda total do trabalho com esse tema.</p>
        <div className="conter-btn">
                  <button 
                    className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
                  >
                    Cancelar
                  
                  </button>
                  <button className="destroy" >Confirmar</button>
                  </div>
      </div>
      <Header toggleSidebar={toggleSidebar} />
      <SideBar isSidebarOpen={isSidebarOpen} />
      <main className="main-content">
        <div className="conteiner-topic papel">
           
        </div>
      </main>
    </div>
  );
}

export default TopicList;
