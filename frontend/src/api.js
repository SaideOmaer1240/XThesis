import axios from "axios";
import { ACCESS_TOKEN } from "./constants"; 
const apiUrl = "http://backend:8000"; 
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

// Interceptor para adicionar o token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para lidar com erros de resposta
api.interceptors.response.use(
  (response) => response,
  (error) => {
     
    return Promise.reject(error);
  }
);

export default api;


