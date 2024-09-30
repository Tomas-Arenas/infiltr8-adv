<script>
  import { ThumbsUpSolid, ThumbsDownSolid } from 'flowbite-svelte-icons';
  import { Card } from 'flowbite-svelte'
 
  let username = '';
  let password = '';
  let errorMessage = '';
 
  function handleSubmit() {
    if (!username || !password) {
      errorMessage = 'Please enter both username and password.';
      return;
    }
 
    // Placeholder for authentication logic
    console.log(`Username: ${username}, Password: ${password}`);
    // Clear fields after submission (optional)
    username = '';
    password = '';
    errorMessage = '';
  }
 

</script>
 
 
<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
  }
 
  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    text-align: center;
    background: var(--background-color);
    transition: background 0.3s ease;
    position: relative;
  }
 
  .login-form {
    background-color: var(--form-background);
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 350px;
  }
 
  h1.brand {
    margin-bottom: 20px;
    font-size: 36px;
    color: var(--brand-color);
  }
 
  h2 {
    margin-bottom: 20px;
    font-size: 24px;
    color: var(--text-color);
  }
 
  .form-group {
    margin-bottom: 15px;
  }
 
  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: var(--label-color);
  }
 
  .form-group input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    border: 1px solid var(--input-border);
    border-radius: 4px;
    background: var(--input-background);
    color: var(--input-text);
  }
 
  .form-group input:focus {
    border-color: var(--input-focus-border);
    outline: none;
  }
 
  .error-message {
    color: var(--error-color);
    margin-bottom: 15px;
  }
 
  .submit-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    background-color: var(--button-background);
    color: var(--button-text);
    border: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }
 
  .submit-button:hover {
    background-color: var(--button-hover-background);
  }
 
  .forgot-password {
    display: block;
    margin-top: 15px;
    font-size: 14px;
    color: var(--forgot-password-color);
    text-decoration: none;
  }
 
  .forgot-password:hover {
    text-decoration: underline;
  }
 
  .dark-mode-toggle {
    position: absolute;
    top: 20px;
    right: 20px;
    cursor: pointer;
    font-size: 18px;
  }
 
  /* Light mode styles */
  :global(:root) {
    --background-color: #f5f5f5;
    --form-background: white;
    --brand-color: #007bff;
    --text-color: #333;
    --label-color: #666;
    --input-background: #fff;
    --input-border: #ddd;
    --input-focus-border: #007bff;
    --input-text: #333;
    --error-color: red;
    --button-background: #007bff;
    --button-text: white;
    --button-hover-background: #0056b3;
    --forgot-password-color: #007bff;
  }
 
  /* Dark mode styles */
  .dark-mode {
    --background-color: #121212;
    --form-background: #1e1e1e;
    --brand-color: #1e90ff;
    --text-color: #e0e0e0;
    --label-color: #e0e0e0;
    --input-background: #2e2e2e;
    --input-border: #444;
    --input-focus-border: #1e90ff;
    --input-text: #e0e0e0;
    --error-color: #ff4c4c;
    --button-background: #1e90ff;
    --button-text: white;
    --button-hover-background: #1c86ee;
    --forgot-password-color: #1e90ff;
  }
</style>
 
<div class='login-container'>
  <Card><h1>SUP BRUH</h1></Card>
<h1 class="brand">INFILTR8</h1>
<div class="login-form">
<h2>Login</h2>
    {#if errorMessage}
<div class="error-message">{errorMessage}</div>
    {/if}
<div class="form-group">
<label for="username">Username</label>
<input type="text" id="username" bind:value={username} placeholder="Enter your username" />
</div>
<div class="form-group">
<label for="password">Password</label>
<input type="password" id="password" bind:value={password} placeholder="Enter your password" />
</div>
<a href="/forgot-password" class="forgot-password">Forgot password?</a>
<button class="submit-button" on:click={handleSubmit}>Login</button>
</div>
</div>