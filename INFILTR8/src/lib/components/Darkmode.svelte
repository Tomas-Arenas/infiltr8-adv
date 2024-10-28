<script>
  import { SunSolid, MoonSolid } from 'flowbite-svelte-icons';
  import { onMount } from 'svelte';

  export let darkMode = false;  // Allow external binding for dark mode state
  export let showIcon = true;   // Control whether to show the icon, default to true

  // On component mount, load dark mode preference from localStorage
  onMount(() => {
    if (typeof window !== 'undefined' && localStorage.getItem('color-theme') === 'dark') {
      darkMode = true;
      document.documentElement.classList.add('dark');
    } else {
      darkMode = false;
      document.documentElement.classList.remove('dark');
    }
  });

  // Apply dark mode settings reactively and save to localStorage and cookies when darkMode changes
  $: if (typeof window !== 'undefined') {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('color-theme', 'dark');
      document.cookie = 'color-theme=dark; max-age=31536000; path=/';
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('color-theme', 'light');
      document.cookie = 'color-theme=light; max-age=31536000; path=/';
    }
  }

  // Function to toggle dark mode state
  const toggleDarkMode = () => {
    darkMode = !darkMode;
  };
</script>

{#if showIcon}
  <button on:click={toggleDarkMode}>
    {#if darkMode}
      <SunSolid color='white' class="h-7 w-7 pointer-events-none" /> <!-- Dark mode icon -->
    {:else}
      <MoonSolid class="h-7 w-7 pointer-events-none" /> <!-- Light mode icon -->
    {/if}
  </button>
{/if}
