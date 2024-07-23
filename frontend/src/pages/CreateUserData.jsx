import React, { useState } from 'react';
import api from '../api';

const CreateUserData = () => {
    const [formData, setFormData] = useState({
        professor: '',
        aluno: '',
        instituto: '',
        cidade: '',
        disciplina: ''
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try { 
            const response = await api.post('/api/create/user-data/', formData);
            if (response.status === 201) {
                alert('Dados do usuário criados com sucesso!');
            }
        } catch (error) {
            console.error('Erro ao criar dados do usuário', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" id='professor' name="professor" placeholder="Professor" value={formData.professor} onChange={handleChange} />
            <input type="text" id='aluno' name="aluno" placeholder="Aluno" value={formData.aluno} onChange={handleChange} />
            <input type="text" id='instituto' name="instituto" placeholder="Instituto" value={formData.instituto} onChange={handleChange} />
            <input type="text" id='cidade' name="cidade" placeholder="Cidade" value={formData.cidade} onChange={handleChange} />
            <input type="text" id='disciplina' name="disciplina" placeholder="Disciplina" value={formData.disciplina} onChange={handleChange} />
            <button type="submit">Criar Dados</button>
        </form>
    );
};

export default CreateUserData;
