import React, { useState, useEffect } from 'react';
import api from '../api'

const EditUserData = ({ id }) => {
    const [formData, setFormData] = useState({
        professor: '',
        aluno: '',
        instituto: '',
        cidade: '',
        disciplina: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            try { 
                const response = await api.get(`/api/edit/user-data/${id}/`,
                     
                );
                setFormData(response.data);
            } catch (error) {
                console.error('Erro ao buscar dados do usuário', error);
            }
        };

        fetchData();
    }, [id]);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.put(`/api/userdata/${id}/`, formData);
            if (response.status === 200) {
                alert('Dados do usuário atualizados com sucesso!');
            }
        } catch (error) {
            console.error('Erro ao atualizar dados do usuário', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" name="professor" placeholder="Professor" value={formData.professor} onChange={handleChange} />
            <input type="text" name="aluno" placeholder="Aluno" value={formData.aluno} onChange={handleChange} />
            <input type="text" name="instituto" placeholder="Instituto" value={formData.instituto} onChange={handleChange} />
            <input type="text" name="cidade" placeholder="Cidade" value={formData.cidade} onChange={handleChange} />
            <input type="text" name="disciplina" placeholder="Disciplina" value={formData.disciplina} onChange={handleChange} />
            <button type="submit">Atualizar Dados</button>
        </form>
    );
};

export default EditUserData;
