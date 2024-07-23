import React, { useState, useEffect } from 'react';
import api from '../api';

const UpdateUserData = () => {
    const [formData, setFormData] = useState({
        professor: '',
        aluno: '',
        instituto: '',
        cidade: '',
        disciplina: ''
    });

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await api.get('/api/view/user-data/');
                setFormData(response.data);
            } catch (error) {
                console.error('Erro ao buscar dados do usuário', error);
            }
        };
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.put('/api/update/user-data/', formData);
            if (response.status === 200) {
                alert('Dados do usuário atualizados com sucesso!');
            }
        } catch (error) {
            console.error('Erro ao atualizar dados do usuário', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" id='professor' name="professor" placeholder="Professor" value={formData.professor} onChange={handleChange} />
            <input type="text" id='aluno' name="aluno" placeholder="Aluno" value={formData.aluno} onChange={handleChange} />
            <input type="text" id='instituto' name="instituto" placeholder="Instituto" value={formData.instituto} onChange={handleChange} />
            <input type="text" id='cidade' name="cidade" placeholder="Cidade" value={formData.cidade} onChange={handleChange} />
            <input type="text" id='disciplina' name="disciplina" placeholder="Disciplina" value={formData.disciplina} onChange={handleChange} />
            <button type="submit">Atualizar Dados</button>
        </form>
    );
};

export default UpdateUserData;
