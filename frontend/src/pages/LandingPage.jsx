import React, {Suspense} from 'react';
import { Link } from 'react-router-dom';
import banner1 from '../assets/img/banner1.jfif';
import banner2 from '../assets/img/banner2.jfif'; 
import '../assets/css/header.css';
import '../assets/css/style.css';
import './LandingPage.css'

const LandingPage = () => {
  return (
     
      <div className="landingpage" >
      
      <header className="landingpage">
        <nav className="navbar landingpage">
          <div className="logo landingpage" > 
            <Link to="/" className="marca landingpage">
              <h1 className="landingpage">Mindjob</h1>
            </Link>
          </div>
          <ul className="menu-itens landingpage"> 
            <li className="itens landingpage">
              <Link to="/rewrite" className="item-content landingpage">Criar trabalho</Link>
            </li>
            <li className="itens landingpage">
              <Link to="/sobre" className="item-content landingpage">Sobre nós</Link>
            </li>
            <li className="itens landingpage">
              <Link to="/login" className="item-content login landingpage">Login</Link>
            </li>
            <li className="itens landingpage">
              <Link to="/register" className="item-content registo landingpage">Registar</Link>
            </li>
          </ul>
          <button id="mobile_btn" className="landingpage">
            <i className="fa-solid fa-bars landingpage"></i>
          </button>
        </nav>
        <div className="banner landingpage">
          <div className="banner-content landingpage">
            <h1 className="headline landingpage">
              <span className="heading__2 landingpage">Crie trabalhos acadêmicos em menos de 3 minutos</span>
            </h1>
            <p className="ds landingpage">
              Utilizando algoritmos de última geração, Aeternum é capaz de analisar dados, pesquisar informações relevantes e gerar conteúdo acadêmico de alta qualidade em questão de minutos.
            </p> 
          </div>
          <div className="banner-image landingpage">
            <img src={banner1} alt="Banner 1" className="imagem1 landingpage" />
            <img src={banner2} alt="Banner 2" className="imagem2 landingpage" />
          </div>
        </div>
      </header>
      <ul className="menu-itens-mobile landingpage">
        <li className="itens-mobile landingpage">
          <Link to="/painel_administrativo" className="item-content-mobile landingpage">Painel Administrativo</Link>
        </li>
        <li className="itens-mobile landingpage">
          <Link to="/rewrite" className="item-content-mobile landingpage">Criar trabalho</Link>
        </li>
        <li className="itens-mobile landingpage">
          <Link to="/sobre" className="item-content-mobile landingpage">Sobre nós</Link>
        </li>
        <li className="itens-mobile landingpage">
          <Link to="/login" className="item-content-mobile login landingpage">Login</Link>
        </li>
        <li className="itens-mobile landingpage">
          <Link to="/register" className="item-content-mobile registo landingpage">Registar</Link>
        </li>
      </ul>
    </div> 
    
   
  );
};

export default LandingPage;
