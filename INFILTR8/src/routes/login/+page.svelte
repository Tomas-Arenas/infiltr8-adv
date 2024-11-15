<script>
  import { onMount } from 'svelte';
  import { Card, Modal } from 'flowbite-svelte';
  import { goto } from '$app/navigation';
  import { session, checkSession } from '$lib/stores/session';

  let username = '';
  let password = '';
  let errorMessage = '';

  let showCreateAccountModal = false;
  let showForgotPasswordModal = false;

  // Create Account Form Variables
  let createUsername = '';
  let createPassword = '';
  let createErrorMessage = '';
  let createSuccessMessage = '';
  let recoveryKey = ''; // Store the recovery key to display

  // Forgot Password Form Variables
  let accountKey = '';
  let forgotUsername = '';
  let keyProvided = true; // Assume user has the account key initially

  // Reactive variable to control autocomplete
  let autocomplete = 'on';

  let showRequestAcceptedModal = false; // Modal state for checking request status
  let checkUsername = '';               // Username to check request status
  let requestStatusMessage = ''; 
  let showResetPasswordForm = false; // New variable to control form visibility
  let newPassword = '';

  onMount(() => {
    checkSession(); // Check session on page load
  });

  // Disable autocomplete when modals are opened by changing the reactive variable
  function handleModalOpen(modalType) {
    if (modalType === 'createAccount') {
      showCreateAccountModal = true;
    } else if (modalType === 'forgotPassword') {
      showForgotPasswordModal = true;
    }

    // Disable autocomplete while modals are open
    autocomplete = 'off';
  }

  // Re-enable autocomplete when modals are closed and reset forgot password modal state
  function handleModalClose() {
    showCreateAccountModal = false;
    showForgotPasswordModal = false;
    keyProvided = true; // Reset to default state
    autocomplete = 'on';
  }
  async function submitNewPassword() {
    if (!newPassword) {
        alert("Please enter a new password.");
        return;
    }

    try {
        const response = await fetch("http://localhost:5173/flask-api/reset-password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: checkUsername, newPassword })
        });

        if (response.ok) {
            alert("Password reset successfully.");
            showResetPasswordForm = false; // Hide the form after successful reset
            requestStatusMessage = "Your password has been reset. You may now log in with your new password.";
        } else {
            const error = await response.json();
            alert("Failed to reset password. Please try again.");
        }
    } catch (error) {
        console.error("Error in submitNewPassword:", error);
        alert("An error occurred while resetting the password.");
    }
}


async function checkRequestStatus() {
    if (!checkUsername) {
      alert("Please enter your username.");
      return;
    }

    try {
      const response = await fetch("/flask-api/password-reset-status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: checkUsername })
      });

      if (response.ok) {
        const data = await response.json();
        requestStatusMessage = `Your request status: ${data.status}`;
        showResetPasswordForm = data.status === "approved";  // Show form only if approved
      } else {
        const error = await response.json();
        requestStatusMessage = error.error || "Failed to check request status.";
        showResetPasswordForm = false;
      }
    } catch (error) {
      console.error("Error in checkRequestStatus:", error);
      alert("An error occurred while checking the password reset request status.");
    }
  }


  async function loginUser() {
    const response = await fetch('/flask-api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }, 
      body: JSON.stringify({ username, password })
    });

    if (response.ok) {
      const result = await response.json();
      console.log(result.status); // should be admin or user
      await checkSession(); // Update session store
      goto('/dashboard');
    } else {
      errorMessage = 'Failed to login';
    }
  }

  async function createUser() {
    createErrorMessage = '';
    createSuccessMessage = '';
    recoveryKey = '';  // Reset recovery key each time the form is submitted

    const payload = {
      username: createUsername,
      password: createPassword,
    };

    try {
      const response = await fetch('/flask-api/create_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        createSuccessMessage = 'User created successfully!';
        recoveryKey = data.recovery_key;  // Capture the recovery key
        createUsername = '';
        createPassword = '';
      } else {
        createErrorMessage = data.error || 'Failed to create user';
      }
    } catch (error) {
      createErrorMessage = 'An error occurred: ' + error.message;
    }
  }

  async function submitForgotPassword() {
      if (!forgotUsername) {
        alert('Please enter your username.');
        return;
      }

      try {
        const response = await fetch('/flask-api/request-password-reset', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: forgotUsername }), // Send username to backend
        });

        if (response.ok) {
          const data = await response.json();
          console.log('Password reset request sent:', data);
          alert('Your password reset request has been sent to the admin.');
        } else {
          const error = await response.json();
          console.error('Error requesting password reset:', error);
          alert('Failed to send password reset request. Please try again.');
        }
      } catch (error) {
        console.error('Error submitting password reset request:', error);
        alert('An error occurred while sending the password reset request.');
      } finally {
        handleModalClose(); // Close the modal after submission
      }
    }


</script>

<div class="flex items-center justify-center min-h-screen">
  <form on:submit|preventDefault={loginUser} class="w-full max-w-md">
    <Card size='lg'>
      <h2 class="text-xl font-bold mb-3">Login</h2>
      {#if errorMessage}
        <div class="text-red-600 dark:text-red-400">{errorMessage}</div>
      {/if}

      <div class="relative z-0 w-full mb-6 group">
        <input type="text" id="username" bind:value={username} placeholder=" " required {autocomplete} 
          class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" />
        <label for="username" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Username</label>
      </div>

      <div class="relative z-0 w-full mb-6 group">
        <input type="password" id="password" bind:value={password} placeholder=" " required {autocomplete}
          class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer" />
        <label for="password" class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Password</label>
      </div>

      <button type="submit" class="w-full py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700">
        Login
      </button>

      <div class="mt-4 text-sm text-center text-gray-500 dark:text-gray-400">
        <button type="button" class="cursor-pointer hover:underline" on:click={() => handleModalOpen('createAccount')}>Create Account</button>
        &nbsp;|&nbsp;
        <button class="cursor-pointer hover:underline" on:click={() => handleModalOpen('forgotPassword')}>Forgot Password</button>
      </div>
    </Card>
  </form>

  <!-- Create Account Modal -->
  <Modal open={showCreateAccountModal} on:close={handleModalClose}>
    <div class="p-4">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Create Account</h3>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">Enter your details to create a new account.</p>
  
      {#if createErrorMessage}
        <div class="text-red-600 dark:text-red-400 mt-2">{createErrorMessage}</div>
      {/if}
      {#if createSuccessMessage}
        <div class="text-green-600 dark:text-green-400 mt-2">{createSuccessMessage}</div>
      {/if}
  
      <form on:submit|preventDefault={createUser} class="mt-4 space-y-4">
        <!-- Username Field -->
        <input type="text" id="create-username" bind:value={createUsername} placeholder="Username" required
          class="w-full p-2 bg-gray-100 dark:bg-gray-700 rounded-md" />
  
        <!-- Password Field -->
        <input type="password" id="create-password" bind:value={createPassword} placeholder="Password" required
          class="w-full p-2 bg-gray-100 dark:bg-gray-700 rounded-md" />
  
        <!-- Create Account Button -->
        <button type="submit" class="w-full px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700">Create Account</button>
      </form>

      <!-- Display the Recovery Key if Available -->
      {#if recoveryKey}
        <div class="mt-4 p-4 bg-yellow-100 dark:bg-yellow-700 rounded-lg">
          <h4 class="font-semibold text-yellow-800 dark:text-yellow-300">Important: Save Your Recovery Key</h4>
          <p class="mt-2 text-sm text-gray-700 dark:text-gray-200">
            This key is required to reset your password if needed. Please store it in a secure location.
          </p>
          <div class="mt-2 text-lg font-mono text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-800 p-2 rounded-md">
            {recoveryKey}
          </div>
        </div>
      {/if}
  
      <div class="mt-4">
        <button class="w-full px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-gray-700" on:click={handleModalClose}>Close</button>
      </div>
    </div>
  </Modal>

  <!-- Forgot Password Modal -->
  <Modal open={showForgotPasswordModal} on:close={handleModalClose}>
  <div class="p-4">
    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Forgot Password</h3>
    <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
      {#if keyProvided}
        Enter your account key to reset your password.
      {:else}
        Enter your username to request an admin reset or check if your request was accepted.
      {/if}
    </p>

    {#if keyProvided}
      <!-- Account Key Input -->
      <input type="text" id="account-key" bind:value={accountKey} placeholder="Enter your account key" class="w-full p-2 mt-4 bg-gray-100 dark:bg-gray-700 rounded-md"/>
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
        Lost your account key? 
        <button class="text-indigo-600 cursor-pointer hover:underline" on:click={() => keyProvided = false}>Click here</button>
      </p>
    {:else}
      <!-- Username Input for Admin Reset -->
      <input type="text" id="forgot-username" bind:value={forgotUsername} placeholder="Enter your username" class="w-full p-2 mt-4 bg-gray-100 dark:bg-gray-700 rounded-md"/>
      
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
        <button class="text-indigo-600 cursor-pointer hover:underline" on:click={() => showRequestAcceptedModal = true}>Was your request accepted?</button>
      </p>
      
      <!-- Submit Button -->
      <div class="mt-4">
        <button class="w-full px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700" on:click={submitForgotPassword}>Submit</button>
      </div>
    {/if}
    
    <div class="mt-4">
      <!-- Close Button -->
      <button class="w-full px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-gray-700" on:click={handleModalClose}>Close</button>
    </div>
  </div>
  {#if showResetPasswordForm}
    <div class="mt-4">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Reset Password</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">Enter a new password for your account.</p>
        
        <input type="password" id="new-password" bind:value={newPassword} placeholder="Enter new password" class="w-full p-2 mt-4 bg-gray-100 dark:bg-gray-700 rounded-md"/>
        
        <button class="w-full px-4 py-2 mt-4 text-white bg-blue-600 rounded-lg hover:bg-blue-700" on:click={submitNewPassword}>Reset Password</button>
    </div>
{/if}

</Modal>

<!-- "Was Your Request Accepted?" Modal -->
<Modal open={showRequestAcceptedModal} on:close={() => showRequestAcceptedModal = false}>
  <div class="p-4">
    <!-- Modal Title -->
    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Check Request Status</h3>
    <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
      Enter your username to check the status of your password reset request.
    </p>

    <!-- Username Input -->
    <input
      type="text"
      id="check-username"
      bind:value={checkUsername}
      placeholder="Enter your username"
      class="w-full p-2 mt-4 bg-gray-100 dark:bg-gray-700 rounded-md"
    />

    <!-- Check Status Button -->
    <div class="mt-4">
      <button
        class="w-full px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
        on:click={checkRequestStatus}>
        Check Status
      </button>
    </div>

    <!-- Display Request Status Message -->
    {#if requestStatusMessage}
      <p class="mt-4 text-center text-gray-600 dark:text-gray-300">{requestStatusMessage}</p>
    {/if}

    <!-- Password Reset Form if the request is accepted -->
    {#if showResetPasswordForm}
      <div class="mt-4">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Reset Password</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Enter a new password for your account.
        </p>

        <!-- New Password Input -->
        <input
          type="password"
          id="new-password"
          bind:value={newPassword}
          placeholder="Enter new password"
          class="w-full p-2 mt-4 bg-gray-100 dark:bg-gray-700 rounded-md"
        />

        <!-- Submit New Password Button -->
        <button
          class="w-full px-4 py-2 mt-4 text-white bg-blue-600 rounded-lg hover:bg-blue-700"
          on:click={submitNewPassword}
        >
          Reset Password
        </button>
      </div>
    {/if}
  </div>
</Modal>

  
</div>
