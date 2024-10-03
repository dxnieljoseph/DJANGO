import React, { useState, useEffect } from 'react';
import { getUsers, deleteUser } from './api';

function UsersList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    async function fetchUsers() {
      const usersData = await getUsers();
      setUsers(usersData);
    }
    fetchUsers();
  }, []);

  const handleDelete = async (userId) => {
    await deleteUser(userId);
    setUsers(users.filter((user) => user.id !== userId));
  };

  return (
    <div>
      <h1>Liste des Utilisateurs</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.username} ({user.email})
            <button onClick={() => handleDelete(user.id)}>Supprimer</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UsersList;
