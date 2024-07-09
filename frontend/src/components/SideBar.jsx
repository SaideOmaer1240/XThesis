// SideBar.jsx 
import { Link } from 'react-router-dom';
//import '../assets/css/geral/styles.css'; 
//import '../assets/css/style.css';  
//import '../assets/css/base.css'; 
//import '../assets/css/book.css';  
//import '../assets/css/geral/card_olds.css';
//import '../assets/css/geral/styles.css'; 
import api from '../api';
import React, { useState, useEffect } from 'react';

function SideBar() {
  
  const [user_info, setUserInfo] = useState([]);
  useEffect(()=>{
    const fetchUserInfo = async() => {
      const token = localStorage.getItem('token');
      try {
        const response = await api.get('/api/user/info/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUserInfo(response.data);
      } catch (error){
        console.error('Erro ao obter dados do usuario:', error);
      }
    };
    fetchUserInfo();
  }, []);

  const toggleSidebar = () => {
    // Adicione a lógica de expandir/retrair sidebar aqui
  };


  return (
    <aside className="sidebar">
      <div className="btn-expandir" onClick={toggleSidebar}>
        <i className="fa-solid fa-bars" id="btn-exp" style={{ fontSize: '29px' }}></i>
      </div>
      <ul>
        <li className="item-menu">
          <Link to="/topic">
            <span className="icon">
              <i className="fa-solid fa-book" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Trabalhos</span>
          </Link>
        </li>
         
        <li className="item-menu">
          <Link to="/rewrite">
            <span className="icon">
              <i className="fa-solid fa-pen" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Escrever</span>
          </Link>
        </li> 
      </ul>
    </aside>
  );
}

export default SideBar;
document.querySelectorAll(".item-menu").forEach((item) => {
  item.addEventListener("click", function () {
    document
      .querySelectorAll(".item-menu")
      .forEach((i) => i.classList.remove("ativo"));
    this.classList.add("ativo");
  });
});