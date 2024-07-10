import { Link } from "react-router-dom";
import Header from "./Header";
import SideBar from "./SideBar";
import "../assets/css/plan.css"; 
import React, { useState, useEffect } from "react";
function Plan() {
  return (
    <div className="layout">
      <Header />
      <SideBar />
      <main className="main-content">
        <div className="plan conteiner papel">
          <div className=" plan general free">
            <header className="plan title">
              <p>Plano gratuito</p>
            </header>
            <div className="plan body">
              <p>Vitalício</p>
              <p>Acesso a ChatPDF</p>
              <p>Acesso a escritor de trablho academico</p>
              <p>Acesso de escritor de Monografia</p>
              <p>Baixar trabalho em formato Word .docx</p>
              <p>Copiar texto da tela</p>
            </div>
            <footer className="plan footer">
            <h2>Preço: 0.00 Mt</h2>
            <button className="btn" id="btn">Acessar</button>
            </footer>
          </div>
          <div className=" plan monthly">
            <header className="plan title">
              <p>Plano Mensal</p>
            </header>
            <div className="plan body">
              <p>Vitalício</p>
              <p>Acesso a ChatPDF</p>
              <p>Acesso a escritor de trablho academico</p>
              <p>Acesso de escritor de Monografia</p>
              <p>Baixar trabalho em formato Word .docx</p>
              <p>Copiar texto da tela</p>
            </div>
            <footer className="plan footer">
            <h2>Preço: 100.00 Mt</h2>
            <button className="btn" id="btn">Assinar</button>
            </footer>
          </div>
          <div className=" plan pro">
            <header className="plan title">
              <p>Plano Profissional</p>
            </header>
            <div className="plan body">
              <p>Vitalício</p>
              <p>Acesso a ChatPDF</p>
              <p>Acesso a escritor de trablho academico</p>
              <p>Acesso de escritor de Monografia</p>
              <p>Baixar trabalho em formato Word .docx</p>
              <p>Copiar texto da tela</p>
            </div>
            <footer className="plan footer">
              <h2>Preço: 10,000.00 Mt</h2>
              <button className="btn" id="btn">Assinar</button>
            </footer>
          </div>
        </div>
      </main>
    </div>
  );
}
export default Plan;
