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
              <h1 className="landingpage">GPT4 Academic Job</h1>
            </Link>
          </div>
          <ul className="menu-itens landingpage"> 
            
            <li className="itens landingpage">
              <Link to="/login" className="item-content login landingpage">Login</Link>
            </li>
            <li className="itens landingpage">
              <Link to="/register" className="item-content registo landingpage">Registar</Link>
            </li>
          </ul> 
        </nav>
        <div className="banner landingpage papel">
          <div className="banner-content landingpage">
            <h1 className="headline landingpage">
              <span className="heading__2 landingpage">Crie trabalhos acadêmicos em pouco tempo</span>
            </h1>
            <p className="ds landingpage" style={{color: 'white'}}>
              Utilizando algoritmos de última geração, 'GPT for Academic Job' é capaz de analisar dados, pesquisar informações relevantes e gerar conteúdo acadêmico de alta qualidade em questão de minutos.
            </p> 
            <li className="itens landingpage">
              <Link to="/rewrite" className="item-content landingpage">Testar de graça</Link>
            </li> 
          </div>
          <div className="banner-image landingpage">
            <img src={banner1} alt="Banner 1" className="imagem1 landingpage" />
            <img src={banner2} alt="Banner 2" className="imagem2 landingpage" />
          </div>
        </div>
      </header> 
    </div> 
    
   
  );
};

export default LandingPage;
