<script>
  let username = '';
  let password = '';
  let message = '';

  const handleLogin = async () => {
    const formData = new URLSearchParams({
      grant_type: 'password',
      username: username,
      password: password,
      scope: '',
      client_id: 'string',  // Use actual client ID if necessary
      client_secret: 'string'  // Use actual client secret if necessary
    });

    try {
      const response = await fetch('http://localhost:8000/auth/token', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: formData.toString()
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token); // Store token in local storage
        message = 'Login successful!';
        // Handle successful login (e.g., redirect, save token)
      } else {
        const error = await response.json();
        message = `Error: ${error.detail}`;
      }
    } catch (error) {
      message = 'An error occurred while trying to login.';
    }
  };
</script>

<style>
  :global(body) {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f9;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
  }

  h1 {
    text-align: center;
    margin-bottom: 1rem;
    color: #333;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
  }

  button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #0056b3;
  }

  .message {
    margin-top: 1rem;
    text-align: center;
    color: red;
  }
</style>

<div class="container">
  <h1>Login</h1>
  <form on:submit|preventDefault={handleLogin}>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} placeholder="Enter your username" />

    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} placeholder="Enter your password" />

    <button type="submit">Login</button>

    {#if message}
      <div class="message">{message}</div>
    {/if}
  </form>
</div>
