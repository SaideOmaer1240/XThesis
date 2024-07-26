import React, {useState} from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

import Header from "../components/Header";
import SideBar from "../components/SideBar";

const DestroyThesis = () => {
  const { code } = useParams();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); 
  const navigate = useNavigate();

  const regressar = () => {
    navigate(`/topic`);
  };
  const destroy = async () => {
    try {
      const response = await api.delete(
        `/api/delete/one/thesis/?code=${encodeURIComponent(code)}`
      );

      if (response.status === 204) {
        regressar()
      }
    } catch (error) {
      console.error("Erro ao eliminar o trabalho");
    }
  };
  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
};
  return (
    <div className="layout">
      <div className="confirmar-exclusao">
        <h2 className="se-confir-exlusao">
          Deseja realimente excluir esse trabalho?
        </h2>
        <p className="confirmo-sim">
          Essa decisão resultará na perda total do trabalho com esse tema.
        </p>
        <div className="conter-btn">
          <button className="bg-blue-500 text-white font-bold py-2 px-4 rounded" onClick={regressar}>
            Cancelar
          </button>
          <button className="destroy" onClick={destroy}>
            Confirmar
          </button>
        </div>
      </div>
      <Header toggleSidebar={toggleSidebar} />
      <SideBar isSidebarOpen={isSidebarOpen} />
      <main className="main-content">
        <div className="conteiner-topic papel"></div>
      </main>
    </div>
  );
};

export default DestroyThesis;
