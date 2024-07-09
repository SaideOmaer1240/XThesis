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

  return (
    <div className="layout">
      <Header />
      <SideBar />
      <main className="main-content">
        <div className="conteiner-topic papel">
          <div className="conteiner-cards">
            {topics.map((topic) => (
              <div key={topic.id} className="card">
                <div className="visualize">
                  <div className="mb-8">
                    <h3 className="titulo topic">{topic.topic}</h3>
                    <p className=" data text-gray-700 text-base">
                      {" "}
                      <br></br> Adicionado em:{" "}
                      {new Date(topic.date_added).toLocaleDateString()}
                    </p>
                  </div>
                  <button
                    onClick={() => handleViewThesis(topic.topic)}
                    className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
                  >
                    Visualizar
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default TopicList;
