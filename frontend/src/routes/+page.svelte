<script>
  // Functions to handle navigation
  const goToLogin = () => {
    window.location.href = '/login';
  };

  const goToTodo = () => {
    window.location.href = '/todo';
  };

  const goToRegister = () => {
    window.location.href = '/registration';
  };

  const goToUserManagement = () => {
    window.location.href = '/users-management'; // Adjust the URL as needed
  };
</script>

<style>
    @import '../styles/main.css';
</style>

<div class="main-container">
  <h1>Welcome</h1>
  <p>Choose where you want to go:</p>

  <div class="button-container">
    <button class="button login" on:click={goToLogin}>Login</button>
    <button class="button register" on:click={goToRegister}>Registration</button>
    <button class="button todo" on:click={goToTodo}>Todo Application</button>
    <button class="button user-management" on:click={goToUserManagement}>User Management</button>
  </div>
</div>
