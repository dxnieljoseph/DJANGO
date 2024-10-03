import React, { useState, useEffect } from 'react';
import { deleteBook, addBook } from './api';
import axiosInstance from './axiosConfig';  // Importez axiosInstance

function BooksList() {
  const [books, setBooks] = useState([]);  // Déclaration de l'état pour les livres
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    genre: '',
    available: true, // Disponible par défaut
  });

  // Fonction pour récupérer la liste des livres
  const fetchBooks = async () => {
    try {
      const response = await axiosInstance.get('/books/');
      setBooks(response.data);
    } catch (error) {
      console.error('Erreur lors de la récupération des livres:', error);
    }
  };

  // Fonction pour ajouter un livre
  const handleAddBook = async (e) => {
    e.preventDefault(); // Empêche la soumission du formulaire de rafraîchir la page
    try {
      const response = await axiosInstance.post('/books/', newBook);
      setBooks([...books, response.data]); // Ajouter le nouveau livre à la liste
      setNewBook({ title: '', author: '', genre: '', available: true }); // Réinitialiser le formulaire
    } catch (error) {
      console.error('Erreur lors de l\'ajout du livre:', error);
    }
  };

  // Charger les livres au montage du composant
  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div>
      <h1>Liste des Livres</h1>

      {/* Formulaire pour ajouter un nouveau livre */}
      <form onSubmit={handleAddBook}>
        <input
          type="text"
          placeholder="Titre"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Auteur"
          value={newBook.author}
          onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Genre"
          value={newBook.genre}
          onChange={(e) => setNewBook({ ...newBook, genre: e.target.value })}
          required
        />
        <button type="submit">Ajouter un livre</button>
      </form>

      {/* Liste des livres */}
      <ul>
        {books.length > 0 ? (
          books.map((book) => (
            <li key={book.id}>
              {book.title} par {book.author} - {book.genre}
            </li>
          ))
        ) : (
          <li>Aucun livre disponible</li>
        )}
      </ul>
    </div>
  );
}
  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axiosInstance.get('/books/');  // Appel à l'API pour récupérer les livres
        console.log(response.data);  // Vérifiez ce qui est retourné par l'API dans la console du navigateur
        setBooks(response.data);  // Stockez les données dans l'état
      } catch (error) {
        console.error('Erreur lors de la récupération des livres:', error);
      }
    };

    fetchBooks();  // Appel de la fonction pour récupérer les livres
  }, []);  // Le tableau vide signifie que l'effet est exécuté une seule fois, au montage du composant

  const handleDelete = async (bookId) => {
    try {
      await deleteBook(bookId);  // Suppression d'un livre via l'API
      setBooks(books.filter((book) => book.id !== bookId));  // Mise à jour de l'état sans le livre supprimé
    } catch (error) {
      console.error('Erreur lors de la suppression du livre:', error);
    }
  };

  const handleAddBook = async () => {
    const newBook = { title: 'Nouveau Livre', author: 'Auteur Inconnu', genre: 'Fiction', available: true };
    try {
      const addedBook = await addBook(newBook);  // Ajout d'un livre via l'API
      setBooks([...books, addedBook]);  // Mise à jour de l'état avec le nouveau livre ajouté
    } catch (error) {
      console.error('Erreur lors de l\'ajout du livre:', error);
    }
  };

  return (
    <div>
      <h1>Liste des Livres</h1>
      <button onClick={handleAddBook}>Ajouter un livre</button>
      <ul>
        {Array.isArray(books) && books.length > 0 ? (  // Vérifiez que books est un tableau non vide
          books.map((book) => (
            <li key={book.id}>
              {book.title} par {book.author} - {book.genre}
              <button onClick={() => handleDelete(book.id)}>Supprimer</button>
            </li>
          ))
        ) : (
          <li>Aucun livre disponible</li>
        )}
      </ul>
    </div>
  );
}

export default BooksList;
