import './App.css';
import React from 'react';
import BooksList from './BooksList';
import UsersList from './UsersList'

function App() {
  return (
    <div className="App">
      <h1>Tableau de Bord Admin</h1>
      <BooksList />
      <UsersList />
    </div>
  );
}

export default App;
