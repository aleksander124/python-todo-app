// src/Registration.jsx
import React, { useState } from 'react';
import '../styles/register.css'; // Import the registration styles
const apiUrl = import.meta.env.VITE_API_URL;

const Registration = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // To manage message type (success or error)

  const handleRegister = async (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = JSON.stringify({
      username,
      email,
      password
    });

    try {
      const response = await fetch(`${apiUrl}/auth/create-user/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: formData
      });

      if (response.ok) {
        setMessage('Registration successful! You can now login.');
        setMessageType('success'); // Set message type to success
        setTimeout(() => {
          window.location.href = '/login'; // Redirect to login page
        }, 2000); // Wait 2 seconds before redirecting
      } else {
        const error = await response.json();
        setMessage(`Error: ${error.detail}`);
        setMessageType('error'); // Set message type to error
      }
    } catch (error) {
      setMessage('An error occurred during registration.');
      setMessageType('error'); // Set message type to error
    }
  };

  const redirectToLogin = () => {
    window.location.href = '/login'; // Redirect to login page
  };

  const goToMainMenu = () => {
    window.location.href = '/'; // Redirect to the main menu
  };

  return (
    <div className="container">
      <h1>Register</h1>
      <form onSubmit={handleRegister}>
        <label htmlFor="username">Username:</label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter your username"
        />

        <label htmlFor="email">Email:</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
        />

        <label htmlFor="password">Password:</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter your password"
        />

        <button type="submit">Register</button>
      </form>

      <button className="button-secondary" onClick={redirectToLogin}>
        Already have an account? Login
      </button>

      <button className="button-tertiary" onClick={goToMainMenu}>
        Back to Main Menu
      </button>

      {message && (
        <div className={`message ${messageType}`}>{message}</div>
      )}
    </div>
  );
};

export default Registration;
