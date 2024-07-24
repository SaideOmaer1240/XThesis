import api from "../api";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Header({ toggleSidebar }) {
  const [user_info, setUserInfo] = useState([]); 

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
    fetchUserInfo();
  }, []);

  return (
    <header className="navbar">
      <div className="logo">
        <Link to="/" className="marca">
          <h1>GPT4 Academic Job</h1>
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
        </ul>
      </div>
      <div className="btn-expandir" onClick={toggleSidebar}>
        <i className="fa-solid fa-bars" id="btn-exp" style={{ fontSize: '29px' }}></i>
      </div>
    </header>
  );
}

export default Header;



