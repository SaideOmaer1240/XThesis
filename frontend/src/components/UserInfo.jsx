import React, { useState, useEffect } from 'react';
function UserInfo(){
    const [userId, setUserId] = useState(null);
    useEffect(() => {
        const getUserInfo = async () => {
            try {
                const token = localStorage.getItem('token'); // Supondo que o token esteja armazenado no localStorage
                const response = await api.get('/api/user/info/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                setUserId(data.id);
            } catch (error) {
                console.error('Erro ao buscar informações do usuário:', error);
            }
        };

        getUserInfo();
    }, []);

}