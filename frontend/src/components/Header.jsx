
// Header.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import '../assets/css/header.css';  
 function Header(){ 

  return (
    <header className="navbar">
      <div className="logo">
        <Link to="/" className="marca">
          <h1>Mindjob</h1>
        </Link>
      </div>
      <div className="conteiner_list">
        <ul className="lists">
          <li className="list" style={{ marginRight: '20px' }}>
            Seja bem-vindo, {/* Substitua por lógica de autenticação */}
          </li>
          <li className="logout">
          <Link to="/logout"> 
            <span className="txt-link">Sair</span>
          </Link>
        </li>
        </ul> 
         
              
      </div>
    </header>
  );
}

export default Header;
