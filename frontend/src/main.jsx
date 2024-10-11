import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './components/MainPage.jsx'; // Main page component
import TodoApp from './components/TodoApp.jsx'; // Todo app component
import Login from './components/Login.jsx'; // Login component
import Registration from './components/Registration.jsx'; // Registration component
import UserManagement from './components/UserManagement.jsx'; // Import UserManagement component
import './styles/main.css'; // Import your CSS files here

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/todo" element={<TodoApp />} />
      <Route path="/login" element={<Login />} />
      <Route path="/registration" element={<Registration />} />
      <Route path="/users-management" element={<UserManagement />} /> {/* Add this route */}
    </Routes>
  </Router>
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
