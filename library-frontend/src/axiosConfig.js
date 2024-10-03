import axios from 'axios';

// Récupérer le token depuis localStorage
const token = localStorage.getItem('access_token');

// Configurer Axios pour inclure le token dans l'en-tête Authorization
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    Authorization: token ? `Bearer ${token}` : null,  // Ajoute le token si présent
  },
});
  
export default axiosInstance;
