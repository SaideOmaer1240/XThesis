import React from 'react';
import Modal from './Modal'; // Você precisa implementar ou importar um componente de modal, como Modal from 'react-modal';

const ThesisDetailsModal = ({ thesis, onClose }) => {
  return (
    <Modal isOpen={true} onRequestClose={onClose}>
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-4">{thesis.title}</h2>
        <p className="mb-4">{thesis.text}</p>
        <button onClick={onClose} className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center mr-2">
          Fechar
        </button>
      </div>
    </Modal>
  );
};

export default ThesisDetailsModal;
