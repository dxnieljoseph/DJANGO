import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/'; // L'URL de votre backend Django

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',  // URL du backend Django
  timeout: 5000,  // Temps d'attente en millisecondes (facultatif)
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;

export const getBooks = async () => {
  try {
    const response = await axios.get(`${API_URL}books/`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des livres:', error);
    throw error;
  }
};

export const deleteBook = async (bookId) => {
  try {
    await axios.delete(`${API_URL}books/${bookId}/`);
  } catch (error) {
    console.error('Erreur lors de la suppression du livre:', error);
    throw error;
  }
};

export const addBook = async (book) => {
  try {
    const response = await axios.post(`${API_URL}books/`, book);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de l\'ajout du livre:', error);
    throw error;
  }
};

export const getUsers = async () => {
  try {
    const response = await axios.get(`${API_URL}users/`);
    return response.data;
  } catch (error) {
    console.error('Erreur lors de la récupération des utilisateurs:', error);
    throw error;
  }
};

export const deleteUser = async (userId) => {
  try {
    await axios.delete(`${API_URL}users/${userId}/`);
  } catch (error) {
    console.error('Erreur lors de la suppression de l\'utilisateur:', error);
    throw error;
  }
};
