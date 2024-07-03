// SideBar.jsx
import React, { lazy } from 'react';
import { Link } from 'react-router-dom';
import '../assets/css/geral/styles.css'; 
import '../assets/css/style.css';  
import '../assets/css/base.css'; 
import '../assets/css/book.css';  
import '../assets/css/geral/card_olds.css';
import '../assets/css/geral/styles.css'; 

function SideBar() {
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
          <Link to="/my_works">
            <span className="icon">
              <i className="fa-solid fa-house" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Home</span>
          </Link>
        </li>
        <li className="item-menu">
          <Link to="/criar_trabalho">
            <span className="icon">
              <i className="fa-solid fa-gear" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Criar Trabalho</span>
          </Link>
        </li>
        <li className="item-menu">
          <Link to="/sobre">
            <span className="icon">
              <i className="fa-solid fa-user-circle" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Sobre Nós</span>
          </Link>
        </li>
        <li className="item-menu">
          <Link to="/login">
            <span className="icon">
              <i className="fa-solid fa-sign-in-alt" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Login</span>
          </Link>
        </li>
        <li className="item-menu">
          <Link to="/registro">
            <span className="icon">
              <i className="fa-solid fa-user-plus" style={{ fontSize: '25px' }}></i>
            </span>
            <span className="txt-link">Registrar</span>
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