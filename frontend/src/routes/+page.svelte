<script>
  import { onMount } from 'svelte';

  let items = [];
  let error = '';

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
  }

  .item-title {
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #333;
  }

  .item-description {
    font-size: 1em;
    color: #555;
  }

  .loading {
    font-size: 1.2em;
    color: #888;
  }

  .error {
    color: red;
    font-weight: bold;
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
    {#each items as item}
      <div class="item-card">
        <div class="item-title">{item.title}</div>
        <div class="item-description">{item.description}</div>
      </div>
    {/each}
  {/if}
</main>
