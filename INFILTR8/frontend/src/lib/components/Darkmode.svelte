<script>
  import { SunSolid, MoonSolid } from 'flowbite-svelte-icons';
  import { darkMode } from '$lib/stores.js';
  import { onMount } from 'svelte';

  export let showIcon = true;

  onMount(() => {
    if (typeof window !== 'undefined') {
      const savedTheme = localStorage.getItem('color-theme');
      if (savedTheme === 'dark') {
        darkMode.set(true);
      } else {
        darkMode.set(false);
      }
    }
  });

  // Apply dark mode settings reactively
  $: if (typeof window !== 'undefined') {
    darkMode.subscribe((value) => {
      if (value) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
      }
    });
  }

  const toggleDarkMode = () => {
    darkMode.update(n => !n);
  };
</script>

{#if showIcon}
  <button on:click={toggleDarkMode}>
    {#if $darkMode}
      <SunSolid color='white' class="h-7 w-7 pointer-events-none" />
    {:else}
      <MoonSolid class="h-6 w-6 pointer-events-none" />
    {/if}
  </button>
{/if}
