import React from "react"
function Modal() {
    return(
        <div>
            <div className="modal" id="modal">
              <header className="mHeader" id="mHeader">
                 
                <i className="fa fa-exclamation-triangle"></i>
                <p>Token de acesso expirado</p>
              </header>
              <div className="mBody" id="mBody"></div>
              <footer>
                <Link to="/logout">
                  <button>
                    <span className="txt-link" id="span-text-link">Iniciar Sessão Novamente</span>
                  </button>
                </Link>
              </footer>
            </div>
            <div className="modalShadows" id="modalShadows"></div>

        </div>
    );
}
export default Modal;