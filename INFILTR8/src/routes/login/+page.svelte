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
  let showRequestAcceptedModal = false; // Modal to check the status of the password reset request

  // Create Account Form Variables
  let createUsername = '';
  let createPassword = '';
  let createErrorMessage = '';
  let createSuccessMessage = '';
  let recoveryKey = ''; // Store the recovery key to display

  // Forgot Password Form Variables
  let accountKey = '';
  let newPassword = ''; // Store the new password
  let forgotUsername = ''; // Username field for admin reset request
  let recoveryKeyError = '';
  let passwordResetMessage = '';
  let checkUsername = ''; // Username to check the status of the password reset request
  let showResetPasswordForm = false; // Show the password reset form if the request is accepted
  let requestStatusMessage = ''; // Message to display the status of the password reset request
  let adminResetMessage = ''; // Message for admin reset feedback
  let keyProvided = true; // Assume user has the account key initially
  let keyVerified = false; // Track if the recovery key has been verified

  // Reactive variable to control autocomplete
  $: autocomplete = 'on';

  // Redirect authenticated users to the main route
  onMount(async () => {
    await checkSession();
    if ($session.logged_in) {
      goto('/'); // Redirect if user is already authenticated
    }
  });

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

  // Disable autocomplete when modals are opened by changing the reactive variable
  function handleModalOpen(modalType) {
    autocomplete = 'off';
    if (modalType === 'createAccount') {
      showCreateAccountModal = true;
    } else if (modalType === 'forgotPassword') {
      showForgotPasswordModal = true;
    }
  }

  // Re-enable autocomplete when modals are closed and reset modal states
  function handleModalClose() {
    showCreateAccountModal = false;
    showForgotPasswordModal = false;

    // Reset Create Account modal state
    createUsername = '';
    createPassword = '';
    createErrorMessage = '';
    createSuccessMessage = '';
    recoveryKey = '';

    // Reset Forgot Password modal state
    keyProvided = true;
    accountKey = '';
    newPassword = '';
    forgotUsername = '';
    keyVerified = false;
    recoveryKeyError = '';
    passwordResetMessage = '';
    adminResetMessage = '';

    autocomplete = 'on';
  }

  async function loginUser() {
    const response = await fetch('/flask-api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (response.ok) {
      await checkSession();
      goto('/dashboard');
    } else {
      errorMessage = 'Failed to login';
    }
  }

  async function createUser() {
    createErrorMessage = '';
    createSuccessMessage = '';
    recoveryKey = '';

    const payload = { username: createUsername, password: createPassword };

    try {
      const response = await fetch('/flask-api/create_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.status === 201) {
        createSuccessMessage = 'User created successfully!';
        recoveryKey = data.recovery_key;
        createUsername = '';
        createPassword = '';
      } else if (response.status === 409) {
        createErrorMessage = data.error || 'Error: Username already exists';
      } else {
        createErrorMessage = data.error || 'Failed to create user';
      }
    } catch (error) {
      createErrorMessage = 'An error occurred: ' + error.message;
    }
  }

  async function verifyRecoveryKey() {
    recoveryKeyError = '';
    passwordResetMessage = '';

    const response = await fetch('/flask-api/verify_recovery_key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recovery_key: accountKey })
    });

    const data = await response.json();

    if (response.ok) {
      keyVerified = true;
      passwordResetMessage = 'Recovery key verified! Enter your new password below.';
    } else {
      recoveryKeyError = data.error || 'Invalid recovery key';
    }
  }

  async function resetPassword() {
    passwordResetMessage = '';
    recoveryKeyError = '';

    const response = await fetch('/flask-api/reset_password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ recovery_key: accountKey, new_password: newPassword })
    });

    const data = await response.json();

    if (response.ok) {
      passwordResetMessage =
        'Password reset successful! You can now log in with your new password.';
      keyVerified = false;
      accountKey = '';
      newPassword = '';
    } else {
      recoveryKeyError = data.error || 'Failed to reset password';
    }
  }

  function requestAdminReset() {
    adminResetMessage = '';

    // Placeholder for actual admin reset logic
    console.log('Requesting admin reset for username:', forgotUsername);

    // Simulate feedback for admin reset request
    if (forgotUsername) {
      adminResetMessage = `Admin reset request sent for ${forgotUsername}. Please contact support for further assistance.`;
    } else {
      adminResetMessage = 'Please enter a valid username for the admin reset request.';
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

<div class="flex min-h-screen items-center justify-center">
  <form on:submit|preventDefault={loginUser} class="w-full max-w-md">
    <Card size="lg">
      <h2 class="mb-3 text-xl font-bold">Login</h2>
      {#if errorMessage}
        <div class="text-red-600 dark:text-red-400">{errorMessage}</div>
      {/if}

      <div class="group relative z-0 mb-6 w-full">
        <input
          type="text"
          id="username"
          bind:value={username}
          placeholder=" "
          required
          {autocomplete}
          class="peer block w-full appearance-none border-0 border-b-2 border-gray-300 bg-transparent px-0 py-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0 dark:border-gray-600 dark:text-white dark:focus:border-blue-500"
        />
        <label
          for="username"
          class="absolute top-3 -z-10 origin-[0] -translate-y-6 scale-75 transform text-sm text-gray-500 duration-300 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 peer-focus:-translate-y-6 peer-focus:scale-75 dark:text-gray-400"
          >Username</label
        >
      </div>

      <div class="group relative z-0 mb-6 w-full">
        <input
          type="password"
          id="password"
          bind:value={password}
          placeholder=" "
          required
          {autocomplete}
          class="peer block w-full appearance-none border-0 border-b-2 border-gray-300 bg-transparent px-0 py-2.5 text-sm text-gray-900 focus:border-blue-600 focus:outline-none focus:ring-0 dark:border-gray-600 dark:text-white dark:focus:border-blue-500"
        />
        <label
          for="password"
          class="absolute top-3 -z-10 origin-[0] -translate-y-6 scale-75 transform text-sm text-gray-500 duration-300 peer-placeholder-shown:translate-y-0 peer-placeholder-shown:scale-100 peer-focus:-translate-y-6 peer-focus:scale-75 dark:text-gray-400"
          >Password</label
        >
      </div>

      <button
        type="submit"
        class="w-full rounded-lg bg-blue-600 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700"
        >Login</button
      >

      <div class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
        <a href="/" class="cursor-pointer hover:underline">Home</a>
        &nbsp;|&nbsp;
        <button
          type="button"
          class="cursor-pointer hover:underline"
          on:click={() => handleModalOpen('createAccount')}>Create Account</button
        >
        &nbsp;|&nbsp;
        <button
          class="cursor-pointer hover:underline"
          on:click={() => handleModalOpen('forgotPassword')}>Forgot Password</button
        >
      </div>
    </Card>
  </form>

  <!-- Create Account Modal -->
  <Modal open={showCreateAccountModal} on:close={handleModalClose}>
    <div class="p-4">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Create Account</h3>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        Enter your details to create a new account.
      </p>

      {#if createErrorMessage}
        <div class="mt-2 text-red-600 dark:text-red-400">{createErrorMessage}</div>
      {/if}
      {#if createSuccessMessage}
        <div class="mt-2 text-green-600 dark:text-green-400">{createSuccessMessage}</div>
      {/if}

      <form on:submit|preventDefault={createUser} class="mt-4 space-y-4">
        <input
          type="text"
          id="create-username"
          bind:value={createUsername}
          placeholder="Username"
          required
          class="w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
        />
        <input
          type="password"
          id="create-password"
          bind:value={createPassword}
          placeholder="Password"
          required
          class="w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
        />
        <button
          type="submit"
          class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700"
          >Create Account</button
        >
      </form>

      {#if recoveryKey}
        <div class="mt-4 rounded-lg bg-yellow-100 p-4 dark:bg-yellow-700">
          <h4 class="font-semibold text-yellow-800 dark:text-yellow-300">
            Important: Save Your Recovery Key
          </h4>
          <p class="mt-2 text-sm text-gray-700 dark:text-gray-200">
            This key is required to reset your password if needed. Please store it in a secure
            location.
          </p>
          <div
            class="mt-2 rounded-md bg-gray-50 p-2 font-mono text-lg text-gray-900 dark:bg-gray-800 dark:text-white"
          >
            {recoveryKey}
          </div>
        </div>
      {/if}

      <div class="mt-4">
        <button
          class="w-full rounded-lg bg-gray-200 px-4 py-2 text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-gray-700"
          on:click={handleModalClose}>Close</button
        >
      </div>
    </div>
  </Modal>

  <!-- Forgot Password Modal -->
  <Modal open={showForgotPasswordModal} on:close={handleModalClose}>
    <div class="p-4">
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Forgot Password</h3>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        {#if !keyVerified && keyProvided}
          Enter your recovery key to reset your password.
        {:else if !keyProvided}
        Enter your username to request an admin reset.
        {:else}
          Enter a new password to reset your account.
        {/if}
      </p>

      {#if recoveryKeyError}
        <div class="mt-2 text-red-600 dark:text-red-400">{recoveryKeyError}</div>
      {/if}
      {#if passwordResetMessage}
        <div class="mt-2 text-green-600 dark:text-green-400">{passwordResetMessage}</div>
      {/if}
      {#if adminResetMessage}
        <div class="mt-2 text-blue-600 dark:text-blue-400">{adminResetMessage}</div>
      {/if}

      {#if !keyVerified && keyProvided}
        <input
          type="text"
          id="account-key"
          bind:value={accountKey}
          placeholder="Enter your account key"
          class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
        />
        <button
          on:click={verifyRecoveryKey}
          class="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-white"
          >Verify Recovery Key</button
        >
      {:else if !keyProvided}
      <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
        <button
          class="cursor-pointer text-indigo-600 hover:underline"
          on:click={() => (showRequestAcceptedModal = true)}>Check Status of Your Request</button
        >
      </p>
        <input
          type="text"
          id="forgot-username"
          bind:value={forgotUsername}
          placeholder="Enter your username"
          class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
        />
        <button
        on:click={requestAdminReset}
        class="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-white"
        >Request Admin Reset</button
        >
      {:else}
        <input
          type="password"
          id="new-password"
          bind:value={newPassword}
          placeholder="Enter your new password"
          class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
        />
        <button
          on:click={resetPassword}
          class="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-white">Reset Password</button
        >
      {/if}

      <div class="mt-4">
        <button
          class="w-full rounded-lg bg-gray-200 px-4 py-2 text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-gray-700"
          on:click={handleModalClose}>Close</button
        >
        {#if keyProvided}
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Lost your account key?
            <button
              class="cursor-pointer text-indigo-600 hover:underline"
              on:click={() => (keyProvided = false)}>Click here</button
            >
          </p>
        {/if}
      </div>
    </div>
  </Modal>

  <!-- "Was Your Request Accepted?" Modal -->
  <Modal open={showRequestAcceptedModal} on:close={() => (showRequestAcceptedModal = false)}>
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
        class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
      />

      <!-- Check Status Button -->
      <div class="mt-4">
        <button
          class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          on:click={checkRequestStatus}
        >
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
            class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
          />

          <!-- Submit New Password Button -->
          <button
            class="mt-4 w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            on:click={submitNewPassword}
          >
            Reset Password
          </button>
        </div>
      {/if}
    </div>
  </Modal>
</div>