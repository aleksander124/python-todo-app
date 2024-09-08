<script>
  let username = '';
  let email = '';
  let password = '';
  let message = '';
  let messageType = ''; // To manage message type (success or error)

  const handleRegister = async () => {
    const formData = JSON.stringify({
      username: username,
      email: email,
      password: password
    });

    try {
      const response = await fetch('http://localhost:8000/auth/create-user/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: formData
      });

      if (response.ok) {
        message = 'Registration successful! You can now login.';
        messageType = 'success'; // Set message type to success
        window.location.href = '/login'; // Redirect to login page
      } else {
        const error = await response.json();
        message = `Error: ${error.detail}`;
        messageType = 'error'; // Set message type to error
      }
    } catch (error) {
      message = 'An error occurred during registration.';
      messageType = 'error'; // Set message type to error
    }
  };

  const redirectToLogin = () => {
    window.location.href = '/login'; // Redirect to login page
  };

  const goToMainMenu = () => {
    window.location.href = '/'; // Redirect to the main menu
  };
</script>

<style>
  @import '../../styles/register.css';

  .message {
    color: green; /* Set text color to green for success messages */
  }

  .message.error {
    color: red; /* Set text color to red for error messages */
  }
</style>

<div class="container">
  <h1>Register</h1>
  <form on:submit|preventDefault={handleRegister}>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} placeholder="Enter your username"/>

    <label for="email">Email:</label>
    <input id="email" type="email" bind:value={email} placeholder="Enter your email"/>

    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} placeholder="Enter your password"/>

    <button type="submit">Register</button>
  </form>

  <button class="button-secondary" on:click={redirectToLogin}>
    Already have an account? Login
  </button>

  <button class="button-tertiary" on:click={goToMainMenu}>
    Back to Main Menu
  </button>

  {#if message}
    <div class={`message ${messageType}`}>{message}</div>
  {/if}
</div>
