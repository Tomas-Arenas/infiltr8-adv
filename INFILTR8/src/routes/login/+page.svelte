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

	// Redirect authenticated users to the main route
	onMount(async () => {
		await checkSession(); // Ensure session is up-to-date
		if ($session.logged_in) {
			goto('/'); // Redirect if user is already authenticated
		}
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

	// Re-enable autocomplete when modals are closed and reset modal states
	function handleModalClose() {
		showCreateAccountModal = false;
		showForgotPasswordModal = false;

		// Reset Create Account modal state
		createUsername = '';
		createPassword = '';
		createErrorMessage = '';
		createSuccessMessage = '';
		recoveryKey = ''; // Clear recovery key display

		// Reset Forgot Password modal state
		keyProvided = true;
		accountKey = '';
		forgotUsername = '';

		autocomplete = 'on';
	}

	async function loginUser() {
		const response = await fetch('/flask-api/login', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username, password })
		});

		if (response.ok) {
			const result = await response.json();
			console.log(result.status); // "Login successful"
			await checkSession(); // Update session store
			goto('/dashboard');
		} else {
			errorMessage = 'Failed to login';
		}
	}

	async function createUser() {
		createErrorMessage = '';
		createSuccessMessage = '';
		recoveryKey = ''; // Reset recovery key each time the form is submitted

		const payload = {
			username: createUsername,
			password: createPassword
		};

		try {
			const response = await fetch('/flask-api/create_user', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			const data = await response.json();

			if (response.status === 201) {
				createSuccessMessage = 'User created successfully!';
				recoveryKey = data.recovery_key; // Capture the recovery key
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

	// Function to submit forgot password request based on account key or username
	function submitForgotPassword() {
		if (keyProvided) {
			console.log('Verifying account key:', accountKey); // Placeholder for key verification logic
		} else {
			console.log('Requesting admin password reset for username:', forgotUsername); // Placeholder for admin reset request
		}
		handleModalClose(); // Close modal after submission
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
			>
				Login
			</button>

			<div class="mt-4 text-center text-sm text-gray-500 dark:text-gray-400">
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
				<!-- Username Field -->
				<input
					type="text"
					id="create-username"
					bind:value={createUsername}
					placeholder="Username"
					required
					class="w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
				/>

				<!-- Password Field -->
				<input
					type="password"
					id="create-password"
					bind:value={createPassword}
					placeholder="Password"
					required
					class="w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
				/>

				<!-- Create Account Button -->
				<button
					type="submit"
					class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700"
					>Create Account</button
				>
			</form>

			<!-- Display the Recovery Key if Available -->
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
				{#if keyProvided}
					Enter your account key to reset your password.
				{:else}
					Enter your username to request an admin reset.
				{/if}
			</p>

			{#if keyProvided}
				<!-- Account Key Input -->
				<input
					type="text"
					id="account-key"
					bind:value={accountKey}
					placeholder="Enter your account key"
					class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
				/>
				<p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
					Lost your account key?
					<button
						class="cursor-pointer text-indigo-600 hover:underline"
						on:click={() => (keyProvided = false)}>Click here</button
					>
				</p>
			{:else}
				<!-- Username Input for Admin Reset -->
				<input
					type="text"
					id="forgot-username"
					bind:value={forgotUsername}
					placeholder="Enter your username"
					class="mt-4 w-full rounded-md bg-gray-100 p-2 dark:bg-gray-700"
				/>
			{/if}

			<div class="mt-4">
				<!-- Submit Button -->
				<button
					class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-700"
					on:click={submitForgotPassword}>Submit</button
				>
			</div>

			<div class="mt-4">
				<!-- Close Button -->
				<button
					class="w-full rounded-lg bg-gray-200 px-4 py-2 text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:bg-gray-600 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-gray-700"
					on:click={handleModalClose}>Close</button
				>
			</div>
		</div>
	</Modal>
</div>
