<style>
  @import '../../styles/todo.css';
</style>

<script lang="ts">
  import { onMount } from 'svelte';

  interface Item {
    id: number;
    title: string;
    description: string;
    completed: boolean;
  }

  let items: Item[] = [];
  let error: string = '';
  let isEditModalOpen = false;
  let isNewModalOpen = false;
  let currentItem: Item | null = null;
  let newItem: Item = { id: 0, title: '', description: '', completed: false };

  onMount(async () => {
    const token = localStorage.getItem('token');

    // Redirect to login if no token is found
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/my/items/', {
        headers: {
          'Authorization': `Bearer ${token}`, // Include the token in the request
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          // If unauthorized, redirect to login
          window.location.href = '/login';
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      items = await response.json();
    } catch (e) {
      console.error('Error fetching data:', e);
      error = 'Failed to load data. Please check the console for details.';
    }
  });

  function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
  }

  function goToMainMenu() {
    window.location.href = '/';
  }

  async function toggleCompleted(id: number): Promise<void> {
    let itemIndex = items.findIndex(item => item.id === id);
    if (itemIndex > -1) {
      items[itemIndex].completed = !items[itemIndex].completed;
      items = [...items];

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
          body: JSON.stringify({ completed: items[itemIndex].completed }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (e) {
        console.error('Error updating data:', e);
        items[itemIndex].completed = !items[itemIndex].completed;
        items = [...items];
      }
    }
  }

  async function deleteItem(id: number): Promise<void> {
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
      items = items.filter(item => item.id !== id);
    } catch (e) {
      console.error('Error deleting data:', e);
      error = 'Failed to delete the item. Please try again later.';
    }
  }

  function openEditModal(item: Item): void {
    currentItem = { ...item };
    isEditModalOpen = true;
  }

  function closeEditModal(): void {
    isEditModalOpen = false;
    currentItem = null;
  }

  async function saveEdit(): Promise<void> {
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
          body: JSON.stringify({
            title: currentItem.title,
            description: currentItem.description,
            completed: currentItem.completed,
          }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        items = items.map(item =>
          item.id === currentItem!.id ? currentItem! : item
        );
        closeEditModal();
      } catch (e) {
        console.error('Error updating data:', e);
      }
    }
  }

  function openNewModal(): void {
    newItem = { id: 0, title: '', description: '', completed: false };
    isNewModalOpen = true;
  }

  function closeNewModal(): void {
    isNewModalOpen = false;
  }

  async function saveNewItem(): Promise<void> {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/items/', {
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
      items = [...items, savedItem];
      closeNewModal();
    } catch (e) {
      console.error('Error creating new item:', e);
    }
  }
</script>

<main>
  <h1>Items List</h1>

  <!-- Navigation Buttons -->
  <div class="navigation-buttons">
    <button class="main-menu-button" on:click={goToMainMenu}>Back to Main Menu</button>
    <button class="logout-button" on:click={logout}>Logout</button>
  </div>

  {#if error}
    <p class="error">{error}</p>
  {/if}
  {#if items.length === 0 && !error}
    <p class="loading">Loading...</p>
  {/if}
  {#if items.length > 0}
    {#each items as item (item.id)}
      <div class="item-card" class:completed={item.completed}>
        <input
          type="checkbox"
          class="checkbox"
          checked={item.completed}
          on:change={() => toggleCompleted(item.id)}
        />
        <div class="item-content">
          <div class="item-title">{item.title}</div>
          <div class="item-description">{item.description}</div>
        </div>
        <button class="edit-button" on:click={() => openEditModal(item)}>Edit</button>
        <button class="delete-button" on:click={() => deleteItem(item.id)}>Delete</button>
      </div>
    {/each}
  {/if}

  <button class="create-button" on:click={openNewModal}>
    <span class="create-icon">+</span>
  </button>

  {#if isEditModalOpen}
    <div class="modal">
      <div class="modal-content">
        <div class="modal-header">Edit Item</div>
        <input
          type="text"
          class="modal-input"
          bind:value={currentItem.title}
          placeholder="Title"
        />
        <textarea
          class="modal-input"
          bind:value={currentItem.description}
          placeholder="Description"
          rows="4"
        ></textarea>
        <div class="modal-actions">
          <button class="modal-cancel" on:click={closeEditModal}>Cancel</button>
          <button class="modal-save" on:click={saveEdit}>Save</button>
        </div>
      </div>
    </div>
  {/if}

  {#if isNewModalOpen}
    <div class="modal">
      <div class="modal-content">
        <div class="modal-header">Create New Item</div>
        <input
          type="text"
          class="modal-input"
          bind:value={newItem.title}
          placeholder="Title"
        />
        <textarea
          class="modal-input"
          bind:value={newItem.description}
          placeholder="Description"
          rows="4"
        ></textarea>
        <div class="modal-actions">
          <button class="modal-cancel" on:click={closeNewModal}>Cancel</button>
          <button class="modal-save" on:click={saveNewItem}>Save</button>
        </div>
      </div>
    </div>
  {/if}
</main>
