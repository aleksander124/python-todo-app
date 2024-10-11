import React from 'react';
import '../styles/main.css'; // Adjust the path if necessary

const MainPage = () => {
  // Functions to handle navigation
  const goToLogin = () => {
    window.location.href = '/login';
  };

  const goToTodo = () => {
    window.location.href = '/todo';
  };

  const goToRegister = () => {
    window.location.href = '/registration';
  };

  const goToUserManagement = () => {
    window.location.href = '/users-management'; // Adjust the URL as needed
  };

  return (
    <div className="main-container">
      <h1>Welcome</h1>
      <p>Choose where you want to go:</p>

      <div className="button-container">
        <button className="button login" onClick={goToLogin}>Login</button>
        <button className="button register" onClick={goToRegister}>Registration</button>
        <button className="button todo" onClick={goToTodo}>Todo Application</button>
        <button className="button user-management" onClick={goToUserManagement}>User Management</button>
      </div>
    </div>
  );
};

export default MainPage;
