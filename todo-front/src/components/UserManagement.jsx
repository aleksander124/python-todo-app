import React, { useState, useEffect } from 'react';
import '../styles/users-management.css';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newUsername, setNewUsername] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [isSuperuser, setIsSuperuser] = useState(false);
  const [isActive, setIsActive] = useState(false);

  // Fetch users on component mount
  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem('token');

      // Redirect to login if no token is found
      if (!token) {
        window.location.href = '/login'; // Redirect to login page
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/auth/users/', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
        }

        const data = await response.json();
        setUsers(data);
      } catch (e) {
        console.error('Error fetching data:', e);
        setError(`Failed to load users. ${e.message}`);
      }
    };

    fetchUsers();
  }, []);

  // Function to start adding a new user
  const startAdding = () => {
    resetForm();
    setIsAdding(true);
  };

  const redirectToHome = () => {
    window.location.href = '/'; // Adjust this path to match your home route
  };

  // Function to delete a user
  const deleteUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`http://localhost:8000/auth/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
      }

      // Remove the deleted user from the users array
      setUsers(users.filter(user => user.id !== userId));
    } catch (e) {
      console.error('Error deleting user:', e);
      setError(`Failed to delete user. ${e.message}`);
    }
  };

  // Function to start editing a user
  const startEditing = (user) => {
    setSelectedUser(user);
    setNewUsername(user.username);
    setNewEmail(user.email);
    setNewPassword('');
    setIsSuperuser(user.is_superuser);
    setIsActive(user.is_active);
    setIsEditing(true);
    setIsAdding(false); // Ensure adding state is false
  };

  // Function to cancel editing or adding
  const cancelEditing = () => {
    resetForm();
    setIsEditing(false);
    setIsAdding(false);
  };

  // Function to reset the form fields
  const resetForm = () => {
    setSelectedUser(null);
    setNewUsername('');
    setNewEmail('');
    setNewPassword('');
    setIsSuperuser(false);
    setIsActive(false);
  };

  // Function to update a user
  const updateUser = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const body = {
        username: newUsername,
        email: newEmail,
        password: newPassword,
        is_superuser: isSuperuser,
        is_active: isActive,
      };

      const response = await fetch(`http://localhost:8000/auth/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
      }

      // Update the user in the users array
      const updatedUser = await response.json();
      setUsers(users.map(user => (user.id === userId ? updatedUser : user)));
      cancelEditing();
    } catch (e) {
      console.error('Error updating user:', e);
      setError(`Failed to update user. ${e.message}`);
    }
  };

  // Function to create a new user
  const createUser = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token found');
      }

      const body = {
        username: newUsername,
        email: newEmail,
        password: newPassword,
        is_superuser: isSuperuser,
        is_active: isActive,
      };

      const response = await fetch('http://localhost:8000/auth/create-user/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);
      }

      // Add the new user to the users array
      const newUser = await response.json();
      setUsers([...users, newUser]);
      cancelEditing(); // Exit the add user mode
    } catch (e) {
      console.error('Error creating user:', e);
      setError(`Failed to create user. ${e.message}`);
    }
  };

  return (
    <main>
      <h1>User Management</h1>

      <div className="button-container-wrapper">
        {/* Button to add new user */}
        <button className="add-user-btn" type="button" onClick={startAdding}>
          Add New User
        </button>
        {/* Button to redirect to the home page */}
        <button className="home-btn" type="button" onClick={redirectToHome}>
          Home
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      {users.length === 0 && !error && <p className="loading">Loading...</p>}
      {users.length > 0 && (
        <ul className="user-list">
          {users.map(user => (
            <li className="user-item" key={user.id}>
              <div className="user-info">
                <span className="username">{user.username}</span>
                <span className="email">{user.email}</span>
              </div>
              <div className="button-container">
                <button type="button" className="edit-btn" onClick={() => startEditing(user)}>
                  Edit
                </button>
                <button type="button" className="delete-btn" onClick={() => deleteUser(user.id)}>
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {/* Popup for editing/adding user */}
      {(isEditing || isAdding) && (
        <div className="overlay" role="button" onClick={cancelEditing} tabIndex={0} aria-label="Cancel editing" />
      )}
      {(isEditing || isAdding) && (
        <div className="popup" role="dialog" aria-labelledby={isEditing ? 'edit-user' : 'add-user'}>
          <h2 id={isEditing ? 'edit-user' : 'add-user'}>
            {isEditing ? `Edit User: ${selectedUser.username}` : 'Add New User'}
          </h2>

          <form onSubmit={e => { e.preventDefault(); isEditing ? updateUser(selectedUser.id) : createUser(); }}>
            <label htmlFor="username">Username</label>
            <input id="username" type="text" value={newUsername} onChange={e => setNewUsername(e.target.value)} />

            <label htmlFor="email">Email</label>
            <input id="email" type="email" value={newEmail} onChange={e => setNewEmail(e.target.value)} />

            <label htmlFor="password">Password {isEditing ? '(leave blank to keep current)' : ''}</label>
            <input id="password" type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} />

            <label htmlFor="superuser">Is Superuser</label>
            <input id="superuser" type="checkbox" checked={isSuperuser} onChange={e => setIsSuperuser(e.target.checked)} />

            <label htmlFor="active">Is Active</label>
            <input id="active" type="checkbox" checked={isActive} onChange={e => setIsActive(e.target.checked)} />

            <button type="submit">{isEditing ? 'Update User' : 'Create User'}</button>
            <button type="button" onClick={cancelEditing}>Cancel</button>
          </form>
        </div>
      )}
    </main>
  );
};

export default UserManagement;
