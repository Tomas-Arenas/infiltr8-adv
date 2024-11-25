<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Darkmode from '$lib/components/Darkmode.svelte';
	import Colorblind from '$lib/components/Colorblind.svelte';
	import { menuOpen, darkMode } from '$lib/stores.js';
	import Toast from '$lib/components/Toast.svelte';
	import Notifications from '$lib/components/Notifications.svelte';
	import { session, checkSession } from '$lib/stores/session.js';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	// Ensure dark mode class is applied on client-side only
	onMount(() => {
		darkMode.subscribe((value) => {
			if (value) {
				document.documentElement.classList.add('dark');
			} else {
				document.documentElement.classList.remove('dark');
			}
		});

		// Check session state when the component mounts
		checkSession();
	});
</script>

<svelte:head>
	<title>INFILTR8</title>
</svelte:head>

<!-- Toast notifications for temporary alerts -->
{#if $session.logged_in}
	<Toast />
{/if}

<div class="fixed right-0 z-50 flex items-center justify-items-center gap-3 pr-3 pt-2">
	<!-- Notifications Bell -->
	{#if $session.logged_in}
		<Notifications />
	{/if}
	<!-- Darkmode Toggle -->
	<Darkmode showIcon={true} />
	<!-- Colorblind Toggle -->
	<Colorblind showIcon={true} />
</div>

<div
	class="app relative flex max-h-full overflow-hidden bg-white bg-gradient-to-r dark:from-gray-700 dark:to-slate-800"
>
	<!-- Moving Light Effect -->
	<div
		class="animate-movingLight pointer-events-none absolute inset-0 z-0 bg-gradient-to-r from-transparent dark:via-fuchsia-700 to-transparent opacity-10"
	></div>

	<Navbar />
	<div
		class={`relative z-10 flex-1 p-4 transition-all duration-300 ${$session.logged_in && $menuOpen ? 'ml-64' : ''} ${$session.logged_in && $page.route.id != '/login' && $page.route.id != '/' ? 'mt-10' : ''}`}
	>
		<main>
			<slot />
		</main>
	</div>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: fit-content;
	}
</style>
