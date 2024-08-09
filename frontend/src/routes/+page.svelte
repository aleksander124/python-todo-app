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
  let currentItem: Item | null = null;

  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/api/items/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      items = await response.json();
    } catch (e) {
      console.error('Error fetching data:', e);
      error = 'Failed to load data. Please check the console for details.';
    }
  });

  async function toggleCompleted(id: number): Promise<void> {
    let itemIndex = items.findIndex(item => item.id === id);
    if (itemIndex > -1) {
      items[itemIndex].completed = !items[itemIndex].completed;
      items = [...items];

      try {
        const response = await fetch(`http://localhost:8000/api/items/${id}`, {
          method: 'PUT',
          headers: {
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
    try {
      const response = await fetch(`http://localhost:8000/api/items/${id}`, {
        method: 'DELETE',
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
    if (currentItem) {
      try {
        const response = await fetch(`http://localhost:8000/api/items/${currentItem.id}`, {
          method: 'PUT',
          headers: {
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
</script>

<style>
  /* Styles are the same as before with additional styles for the modal */
  main {
    font-family: 'Roboto', sans-serif;
    padding: 20px;
    max-width: 800px;
    margin: auto;
    background-color: #f0f4f8;
  }

  h1 {
    text-align: center;
    color: #333;
    font-size: 2em;
    margin-bottom: 30px;
  }

  .item-card {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }

  .item-card:hover {
    transform: translateY(-5px);
  }

  .item-content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    margin-right: 15px;
  }

  .item-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #1a202c;
  }

  .item-description {
    font-size: 1em;
    color: #4a5568;
  }

  .loading {
    font-size: 1.2em;
    color: #888;
    text-align: center;
  }

  .error {
    color: red;
    font-weight: bold;
    text-align: center;
  }

  .checkbox {
    margin-right: 15px;
  }

  .delete-button,
  .edit-button {
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-left: 5px;
  }

  .edit-button {
    background-color: #4caf50;
  }

  .delete-button:hover {
    background-color: #c53030;
  }

  .edit-button:hover {
    background-color: #388e3c;
  }

  .completed {
    background-color: #d4edda;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .modal-header {
    font-size: 1.5em;
    margin-bottom: 20px;
  }

  .modal-input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .modal-actions {
    display: flex;
    justify-content: flex-end;
  }

  .modal-actions button {
    padding: 10px 15px;
    margin-left: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
  }

  .modal-save {
    background-color: #4caf50;
    color: white;
  }

  .modal-cancel {
    background-color: #f44336;
    color: white;
  }

  .modal-save:hover {
    background-color: #388e3c;
  }

  .modal-cancel:hover {
    background-color: #d32f2f;
  }

  .footer {
    margin-top: 50px;
    text-align: center;
    font-size: 0.9em;
    color: #718096;
  }
</style>

<main>
  <h1>My Todo List</h1>
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
          aria-label="Mark as completed"
        />
        <div class="item-content">
          <div class="item-title">{item.title}</div>
          <div class="item-description">{item.description}</div>
        </div>
        <button
          class="edit-button"
          on:click={() => openEditModal(item)}
          aria-label="Edit item"
        >
          Edit
        </button>
        <button
          class="delete-button"
          on:click={() => deleteItem(item.id)}
          aria-label="Delete item"
        >
          Delete
        </button>
      </div>
    {/each}
  {/if}
  <div class="footer">
    &copy; 2024 My Todo App
  </div>

  {#if isEditModalOpen && currentItem}
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
</main>
