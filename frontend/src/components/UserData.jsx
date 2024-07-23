import api from "../api";
import React, { useState, useEffect } from "react";

function UserData() {
  const [user_data, setUserData] = useState([]);
  useEffect(() => {
    // Buscar (fetch) dados do usuario
    const fetch = async () => {
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
    fetch();
  }, []);
  return(
    <div>  
        <p>{user_data.id} </p>
        <p>{user_data.aluno} </p>
        <p>{user_data.professor} </p>
        <p>{user_data.instituto} </p>
        <p>{user_data.cidade} </p>
        <p>{user_data.disciplina} </p>
    </div>
  )
}

export default UserData;
