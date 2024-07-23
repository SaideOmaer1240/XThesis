import React from 'react';
import api from '../api';

const DeleteUserData = () => {
    const handleDelete = async () => {
        try {
            const response = await api.delete('/api/delete/user-data/');
            if (response.status === 204) {
                alert('Dados do usuário deletados com sucesso!');
            }
        } catch (error) {
            console.error('Erro ao deletar dados do usuário', error);
        }
    };

    return (
        <button onClick={handleDelete}>Deletar Dados</button>
    );
};

export default DeleteUserData;
