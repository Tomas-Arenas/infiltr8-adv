<script>
  import { EyeSolid } from 'flowbite-svelte-icons';
  import { onMount } from 'svelte';

  export let colorblindMode = "normal"; // Allow external binding
  export let showIcon = true; // Control whether to show the icon, default to true

  onMount(() => {
    if (typeof window !== 'undefined' && localStorage.getItem('colorblind-mode')) {
      colorblindMode = localStorage.getItem('colorblind-mode');
    }
    applyColorblindFilter();
  });

  const applyColorblindFilter = () => {
    const root = document.documentElement;
    if (colorblindMode === 'normal') {
      root.style.filter = 'none';
    } else if (colorblindMode === 'protanopia') {
      root.style.filter = 'url(#protanopia-filter)';
    } else if (colorblindMode === 'deuteranopia') {
      root.style.filter = 'url(#deuteranopia-filter)';
    }
  };

  // Update colorblind mode and save to localStorage
  $: if (typeof window !== 'undefined') {
    localStorage.setItem('colorblind-mode', colorblindMode);
    applyColorblindFilter();
  }

  const toggleColorblindMode = () => {
    colorblindMode = colorblindMode === 'normal' ? 'protanopia' :
                     colorblindMode === 'protanopia' ? 'deuteranopia' :
                     'normal';
  };
</script>

<!-- SVG Filters for colorblind simulation -->
<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
  <filter id="protanopia-filter">
    <feColorMatrix type="matrix" values="0.56667 0.43333 0 0 0 0.55833 0.44167 0 0 0 0 0.24167 0.75833 0 0 0 0 0 1 0"></feColorMatrix>
  </filter>
  <filter id="deuteranopia-filter">
    <feColorMatrix type="matrix" values="0.625 0.375 0 0 0 0.7 0.3 0 0 0 0 0.3 0.7 0 0 0 0 0 1 0"></feColorMatrix>
  </filter>
</svg>

<!-- Conditionally render the icon if showIcon is true -->
{#if showIcon}
  <button on:click={toggleColorblindMode}>
    {#if colorblindMode === 'normal'}
      <EyeSolid color='black' class="h-7 w-7 pointer-events-none" /> <!-- Normal mode icon -->
    {:else if colorblindMode === 'protanopia'}
      <EyeSolid color='#ff4c4c' class="h-7 w-7 pointer-events-none" /> <!-- Protanopia mode icon -->
    {:else if colorblindMode === 'deuteranopia'}
      <EyeSolid color='#4caf50' class="h-7 w-7 pointer-events-none" /> <!-- Deuteranopia mode icon -->
    {/if}
  </button>
{/if}

