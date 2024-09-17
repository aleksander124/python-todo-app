<style>
  @import '../../styles/users-management.css';
</style>

<script lang="ts">
  import { onMount } from 'svelte';

  interface User {
    id: number;
    username: string;
    email: string;
    is_superuser: boolean;
    is_active: boolean;
  }

  let users: User[] = [];
  let error: string = '';
  let isEditing: boolean = false;
  let isAdding: boolean = false;  // New state for adding user
  let selectedUser: User | null = null;
  let newUsername: string = '';
  let newEmail: string = '';
  let newPassword: string = '';
  let isSuperuser: boolean = false;
  let isActive: boolean = false;

  // Function to start adding a new user
  function startAdding() {
    resetForm();
    isAdding = true;
  }

  function redirectToHome() {
    window.location.href = '/'; // Adjust this path to match your home route
  }

  // Function to delete a user
  async function deleteUser(userId: number) {
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
      users = users.filter(user => user.id !== userId);
    } catch (e) {
      console.error('Error deleting user:', e);
      error = `Failed to delete user. ${e.message}`;
    }
  }

  // Function to start editing a user
  function startEditing(user: User) {
    selectedUser = user;
    newUsername = user.username;
    newEmail = user.email;
    newPassword = '';
    isSuperuser = user.is_superuser;
    isActive = user.is_active;
    isEditing = true;
    isAdding = false;  // Ensure adding state is false
  }

  // Function to cancel editing or adding
  function cancelEditing() {
    resetForm();
    isEditing = false;
    isAdding = false;
  }

  // Function to reset the form fields
  function resetForm() {
    selectedUser = null;
    newUsername = '';
    newEmail = '';
    newPassword = '';
    isSuperuser = false;
    isActive = false;
  }

  // Function to update a user
  async function updateUser(userId: number) {
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
        is_active: isActive
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
      users = users.map(user => user.id === userId ? updatedUser : user);
      cancelEditing();
    } catch (e) {
      console.error('Error updating user:', e);
      error = `Failed to update user. ${e.message}`;
    }
  }

  // Function to create a new user
  async function createUser() {
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
        is_active: isActive
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
      users = [...users, newUser];
      cancelEditing();  // Exit the add user mode
    } catch (e) {
      console.error('Error creating user:', e);
      error = `Failed to create user. ${e.message}`;
    }
  }

  // Fetch users on component mount
  onMount(async () => {
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

      users = await response.json();
    } catch (e) {
      console.error('Error fetching data:', e);
      error = `Failed to load users. ${e.message}`;
    }
  });
</script>

<main>
  <h1>User Management</h1>

  <div class="button-container-wrapper">
    <!-- Button to add new user -->
    <button class="add-user-btn" type="button" on:click={startAdding}>Add New User</button>
    <!-- Button to redirect to the home page -->
    <button class="home-btn" type="button" on:click={redirectToHome}>Home</button>
  </div>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  {#if users.length === 0 && !error}
    <p class="loading">Loading...</p>
  {/if}

  {#if users.length > 0}
    <ul class="user-list">
      {#each users as user}
        <li class="user-item">
          {user.username}[{user.email}]
          <div class="button-container">
            <button type="button" class="edit-btn" on:click={() => startEditing(user)}>Edit</button>
            <button type="button" class="delete-btn" on:click={() => deleteUser(user.id)}>Delete</button>
          </div>
        </li>
      {/each}
    </ul>
  {/if}

  <!-- Popup for editing/adding user -->
  {#if isEditing || isAdding}
    <div class="overlay" role="button" tabindex="0" aria-label="Cancel editing" on:click={cancelEditing} on:keydown={(e) => e.key === 'Enter' && cancelEditing()}></div>
    <div class="popup" role="dialog" aria-labelledby={isEditing ? 'edit-user' : 'add-user'}>
      <h2 id={isEditing ? 'edit-user' : 'add-user'}>
        {isEditing ? `Edit User: ${selectedUser.username}` : 'Add New User'}
      </h2>

      <form on:submit|preventDefault={isEditing ? () => updateUser(selectedUser.id) : createUser}>
        <label for="username">Username</label>
        <input id="username" type="text" bind:value={newUsername} />

        <label for="email">Email</label>
        <input id="email" type="email" bind:value={newEmail} />

        <label for="password">Password {isEditing ? '(leave blank to keep current)' : ''}</label>
        <input id="password" type="password" bind:value={newPassword} />

        <label for="superuser">Is Superuser</label>
        <input id="superuser" type="checkbox" bind:checked={isSuperuser} />

        <label for="active">Is Active</label>
        <input id="active" type="checkbox" bind:checked={isActive} />

        <button type="submit">{isEditing ? 'Save' : 'Add User'}</button>
        <button type="button" on:click={cancelEditing}>Cancel</button>
      </form>
    </div>
  {/if}
</main>