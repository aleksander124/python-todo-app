<script>
  let username = '';
  let email = '';
  let password = '';
  let message = '';

  const handleRegister = async () => {
    const formData = new URLSearchParams({
      username: username,
      email: email,
      password: password,
    });

    try {
      const response = await fetch('http://localhost:8000/auth/create-user', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: formData.toString()
      });

      if (response.ok) {
        message = 'Registration successful! You can now login.';
        window.location.href = '/login'; // Redirect to login page
      } else {
        const error = await response.json();
        message = `Error: ${error.detail}`;
      }
    } catch (error) {
      message = 'An error occurred during registration.';
    }
  };

  const redirectToLogin = () => {
    window.location.href = '/login'; // Redirect to login page
  };
</script>

<style>
  @import '../../styles/register.css';
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

  {#if message}
    <div class="message">{message}</div>
  {/if}
</div>
