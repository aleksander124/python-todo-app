<script>
  // Functions to handle navigation
  const goToLogin = () => {
    window.location.href = '/login';
  };

  const goToTodo = () => {
    window.location.href = '/todo';
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
    <button class="button todo" on:click={goToTodo}>Todo Application</button>
  </div>
</div>
