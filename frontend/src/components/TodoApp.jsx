import React, { useEffect, useState } from 'react';
import '../styles/todo.css'; // Import your CSS file here
const apiUrl = import.meta.env.VITE_API_URL;

const TodoApp = () => {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  const [isEditModalOpen, setEditModalOpen] = useState(false);
  const [isNewModalOpen, setNewModalOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);
  const [newItem, setNewItem] = useState({ title: '', description: '', completed: false });

  useEffect(() => {
    const token = localStorage.getItem('token');

    // Redirect to login if no token is found
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const fetchData = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/my/items/`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            window.location.href = '/login';
          } else {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
        }

        const data = await response.json();
        setItems(data);
      } catch (e) {
        console.error('Error fetching data:', e);
        setError('Failed to load data. Please check the console for details.');
      }
    };

    fetchData();
  }, []);

  const logout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  const toggleCompleted = async (id) => {
    const itemIndex = items.findIndex(item => item.id === id);
    if (itemIndex > -1) {
      const updatedItems = [...items];
      updatedItems[itemIndex].completed = !updatedItems[itemIndex].completed;
      setItems(updatedItems);

      const token = localStorage.getItem('token');
      if (!token) {
        window.location.href = '/login';
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/api/items/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ completed: updatedItems[itemIndex].completed }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (e) {
        console.error('Error updating data:', e);
        updatedItems[itemIndex].completed = !updatedItems[itemIndex].completed; // Rollback
        setItems(updatedItems);
      }
    }
  };

  const deleteItem = async (id) => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/items/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setItems(items.filter(item => item.id !== id));
    } catch (e) {
      console.error('Error deleting data:', e);
      setError('Failed to delete the item. Please try again later.');
    }
  };

  const openEditModal = (item) => {
    setCurrentItem(item);
    setEditModalOpen(true);
  };

  const closeEditModal = () => {
    setEditModalOpen(false);
    setCurrentItem(null);
  };

  const saveEdit = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    if (currentItem) {
      try {
        const response = await fetch(`http://localhost:8000/api/items/${currentItem.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(currentItem),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        setItems(items.map(item => (item.id === currentItem.id ? currentItem : item)));
        closeEditModal();
      } catch (e) {
        console.error('Error updating data:', e);
      }
    }
  };

  const openNewModal = () => {
    setNewItem({ title: '', description: '', completed: false });
    setNewModalOpen(true);
  };

  const closeNewModal = () => {
    setNewModalOpen(false);
  };

  const saveNewItem = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      const response = await fetch(`${apiUrl}/api/items/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newItem),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const savedItem = await response.json();
      setItems([...items, savedItem]);
      closeNewModal();
    } catch (e) {
      console.error('Error creating new item:', e);
    }
  };

  return (
    <main className="todo-container">
      <h1>Items List</h1>

      <div className="navigation-buttons">
        <button className="main-menu-button" onClick={() => window.location.href = '/'}>Back to Main Menu</button>
        <button className="logout-button" onClick={logout}>Logout</button>
      </div>

      {error && <p className="error">{error}</p>}
      {items.length === 0 && !error && <p className="loading">Loading...</p>}
      {items.length > 0 && items.map(item => (
        <div key={item.id} className={`item-card ${item.completed ? 'completed' : ''}`}>
          <input
            type="checkbox"
            className="checkbox"
            checked={item.completed}
            onChange={() => toggleCompleted(item.id)}
          />
          <div className="item-content">
            <div className="item-title">{item.title}</div>
            <div className="item-description">{item.description}</div>
          </div>
          <div className="item-buttons">
            <button className="edit-button" onClick={() => openEditModal(item)}>Edit</button>
            <button className="delete-button" onClick={() => deleteItem(item.id)}>Delete</button>
          </div>
        </div>
      ))}
      <button className="create-button" onClick={openNewModal}>
        <span className="create-icon">+</span>
      </button>

      {/* Edit Modal */}
      {isEditModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <div className="modal-header">Edit Item</div>
            <input
              type="text"
              className="modal-input"
              value={currentItem.title}
              onChange={(e) => setCurrentItem({ ...currentItem, title: e.target.value })}
              placeholder="Title"
            />
            <textarea
              className="modal-input"
              value={currentItem.description}
              onChange={(e) => setCurrentItem({ ...currentItem, description: e.target.value })}
              placeholder="Description"
              rows="4"
            />
            <div className="modal-actions">
              <button className="modal-cancel" onClick={closeEditModal}>Cancel</button>
              <button className="modal-save" onClick={saveEdit}>Save</button>
            </div>
          </div>
        </div>
      )}

      {/* New Item Modal */}
      {isNewModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <div className="modal-header">Create New Item</div>
            <input
              type="text"
              className="modal-input"
              value={newItem.title}
              onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
              placeholder="Title"
            />
            <textarea
              className="modal-input"
              value={newItem.description}
              onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
              placeholder="Description"
              rows="4"
            />
            <div className="modal-actions">
              <button className="modal-cancel" onClick={closeNewModal}>Cancel</button>
              <button className="modal-save" onClick={saveNewItem}>Save</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
};

export default TodoApp;
