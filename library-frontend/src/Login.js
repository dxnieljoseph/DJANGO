// src/Login.js (ou un fichier similaire)

import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        email: email,
        password: password
      });
      
      // Vérifiez si la réponse contient un token JWT
      const token = response.data.access;  // La clé 'access' contient le JWT
      localStorage.setItem('access_token', token);  // Stocke le token dans le localStorage
      console.log('Connexion réussie, token stocké dans localStorage:', token);  // Vérification
      
      // Rediriger l'utilisateur ou effectuer d'autres actions après connexion
      window.location.href = '/dashboard';  // Redirige l'utilisateur

    } catch (error) {
      console.error('Erreur lors de la connexion:', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <label>Email:</label>
      <input 
        type="email" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <label>Mot de passe:</label>
      <input 
        type="password" 
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Se connecter</button>
    </form>
  );
};

export default Login;
