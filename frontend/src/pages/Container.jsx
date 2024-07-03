
import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import '../assets/css/confirmar.css';
import '../assets/css/style.css';
import '../assets/css/criar.css';
import '../assets/css/header.css';
import '../assets/css/base.css';
import '../assets/css/livros.css';
import '../assets/css/book.css';  
import '../assets/css/geral/card_olds.css';
import '../assets/css/geral/styles.css';

function Home() {
    const [isExpanded, setIsExpanded] = useState(false);
    const navigate = useNavigate();
    const location = useLocation(); 
    const toggleSidebar = () => {
      setIsExpanded(!isExpanded);
    };
   
  
    const isRootPath = location.pathname === '/';
  
    if (isRootPath) {
      return null;
    }
  //<div className={`layout ${isExpanded ? 'expandir' : ''}`}>
    return (
      <div>
        
        
      
      </div>
        
    );
  }  
export default Home;

