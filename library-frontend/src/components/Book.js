// src/components/Books.js
import React, { useEffect, useState } from 'react';
import axiosInstance from '../api';  // Import de l'instance Axios

const Books = () => {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axiosInstance.get('/books/');  // Utilisation de l'instance Axios
        setBooks(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des livres:', error);
      }
    };

    fetchBooks();
  }, []);

  return (
    <div>
      <h1>Liste des livres</h1>
      <ul>
        {books.map(book => (
          <li key={book.id}>{book.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default Books;
