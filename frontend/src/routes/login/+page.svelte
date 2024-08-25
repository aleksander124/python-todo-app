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
        window.location.href = '/todo';
      } else {
        const error = await response.json();
        message = `Error: ${error.detail}`;
      }
    } catch (error) {
      message = 'An error occurred while trying to login.';
    }
  };

  const redirectToRegister = () => {
    window.location.href = '/registration';
  };

  const goToMainMenu = () => {
    window.location.href = '/'; // Redirect to the main menu
  };
</script>

<style>
  @import '../../styles/login.css';
</style>

<div class="container">
  <h1>Login</h1>
  <form on:submit|preventDefault={handleLogin}>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} placeholder="Enter your username"/>

    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} placeholder="Enter your password"/>

    <button type="submit">Login</button>
  </form>

  <button class="button-secondary" on:click={redirectToRegister}>
    Don't have an account? Register
  </button>

  <button class="button-tertiary" on:click={goToMainMenu}>
    Back to Main Menu
  </button>

  {#if message}
    <div class="message">{message}</div>
  {/if}
</div>