// src/components/Login.jsx
import React, { useState } from 'react';
import '../styles/login.css'; // Import your CSS styles

const apiUrl = import.meta.env.VITE_API_URL;

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent form submission

    const formData = new URLSearchParams({
      grant_type: 'password',
      username: username,
      password: password,
      scope: '',
      client_id: 'your_client_id',  // Replace with actual client ID if necessary
      client_secret: 'your_client_secret'  // Replace with actual client secret if necessary
    });

    try {
      const response = await fetch(`${apiUrl}/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token); // Store token in local storage
        setMessage('Login successful!');
        window.location.href = '/todo'; // Redirect to the todo page
      } else {
        const error = await response.json();
        setMessage(`Error: ${error.detail}`);
      }
    } catch (error) {
      setMessage('An error occurred while trying to login.');
    }
  };

  const redirectToRegister = () => {
    window.location.href = '/registration';
  };

  const goToMainMenu = () => {
    window.location.href = '/'; // Redirect to the main menu
  };

  return (
      <div className="login-page"> {/* Unique class added */}
        <h1>Login</h1>
        <form onSubmit={handleLogin}>
          <label htmlFor="username">Username:</label>
          <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
          />

          <label htmlFor="password">Password:</label>
          <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
          />

          <button type="submit">Login</button>
        </form>

        <button className="button-secondary" onClick={redirectToRegister}>
          Don't have an account? Register
        </button>

        <button className="button-tertiary" onClick={goToMainMenu}>
          Back to Main Menu
        </button>

        {message && <div className="message">{message}</div>}
      </div>
  );
};

export default Login;
