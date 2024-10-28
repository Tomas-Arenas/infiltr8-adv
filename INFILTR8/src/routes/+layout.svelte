<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Darkmode from '$lib/components/Darkmode.svelte';
	import Colorblind from '$lib/components/Colorblind.svelte';
	import { menuOpen } from '$lib/stores.js';
	import Toast from '$lib/components/Toast.svelte';
	import Notifications from '$lib/components/Notifications.svelte';
	import { darkMode } from '$lib/stores.js'; // Import dark mode store
	import { onMount } from 'svelte'; // Import onMount to handle client-side only logic
  
	// Ensure dark mode class is applied on client-side only
	onMount(() => {
	  darkMode.subscribe((value) => {
		if (value) {
		  document.documentElement.classList.add('dark');
		} else {
		  document.documentElement.classList.remove('dark');
		}
	  });
	});
  </script>
  
  <svelte:head>
	<title>INFILTR8</title>
  </svelte:head>
  
  <!-- Toast notifications for temporary alerts -->
  <Toast />
  
  <div class="fixed right-0 z-50 flex justify-items-center items-center gap-3 pr-3 pt-2">
	<!-- Notifications Bell -->
	<Notifications />
	<!-- Darkmode Toggle -->
	<Darkmode showIcon={true} />
	<!-- Colorblind Toggle -->
	<Colorblind showIcon={true} />
  </div>
  
  <div class="app flex h-screen bg-gray-50 dark:bg-gray-600">
	<Navbar />
	<div class={`flex-1 bg-gray-50 p-4 dark:bg-gray-600 ${$menuOpen ? 'ml-64' : ''} mt-10`}>
	  <main>
		<slot />
	  </main>
	</div>
  </div>
  
  <style>
	.app {
	  display: flex;
	  flex-direction: column;
	  min-height: 300vh;
	}
  </style>
  