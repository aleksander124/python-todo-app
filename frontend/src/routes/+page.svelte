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
</script>

<style>
  main {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 800px;
    margin: auto;
  }

  .item-card {
    background: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: background-color 0.3s ease;
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
    color: #333;
    text-align: left;
  }

  .item-description {
    font-size: 1em;
    color: #555;
    text-align: left;
  }

  .loading {
    font-size: 1.2em;
    color: #888;
  }

  .error {
    color: red;
    font-weight: bold;
  }

  .checkbox {
    margin-right: 15px;
  }

  .delete-button {
    background-color: #ff4d4f;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px;
    cursor: pointer;
  }

  .delete-button:hover {
    background-color: #ff7875;
  }

  .completed {
    background-color: #d4edda;
  }
</style>

<main>
  <h1>Items List</h1>
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
        <button class="delete-button" on:click={() => deleteItem(item.id)}>Delete</button>
      </div>
    {/each}
  {/if}
</main>
