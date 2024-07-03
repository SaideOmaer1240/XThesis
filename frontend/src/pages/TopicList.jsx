import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

function TopicList() {
  const [topics, setTopics] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTopics = async () => {
      const token = localStorage.getItem('token');
      try {
        const response = await api.get('/api/topics/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTopics(response.data);
      } catch (error) {
        console.error('Erro ao buscar tópicos:', error);
      }
    };

    fetchTopics();
  }, []);

  const handleViewThesis = (topicId) => {
    navigate(`/thesis/${topicId}`);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <h2 className="text-2xl font-bold mb-6 text-center">Meus Tópicos</h2>
      <div className="flex flex-wrap justify-center gap-6">
        {topics.map((topic) => (
          <div key={topic.id} className="max-w-sm w-full lg:max-w-full lg:flex">
            <div className="border border-gray-400 bg-white rounded-lg shadow-md p-6 flex flex-col justify-between leading-normal">
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-900 mb-2">{topic.topic}</h3>
                <p className="text-gray-700 text-base">Autor: {topic.author}</p>
                <p className="text-gray-700 text-base">Adicionado em: {new Date(topic.date_added).toLocaleDateString()}</p>
              </div>
              <button
                onClick={() => handleViewThesis(topic.topic)}
                className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
              >
                Ver Tese
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TopicList;
