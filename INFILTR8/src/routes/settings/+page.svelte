<script>
  import { SystemInfo } from '../../lib/SystemInfo.js';
  import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
  import { Label, Select, Button } from 'flowbite-svelte';
  import { onMount } from 'svelte';
  import { session, checkSession } from '$lib/stores/session.js';
  import Colorblind from '$lib/components/Colorblind.svelte';
  import Darkmode from '$lib/components/Darkmode.svelte';

  onMount(() => {
      checkSession(); // Check session on page load
      const savedFontSize = localStorage.getItem("font-size");
      if (savedFontSize) applyFontSize(savedFontSize); // Apply saved font size on page load
  });

  const sysInfo = new SystemInfo();
  let selectedColorMode = "normal"; // Default colorblind mode
  const colorModes = [
    { value: 'normal', name: "Normal" },
    { value: 'protanopia', name: "Protanopia" },
    { value: 'deuteranopia', name: "Deuteranopia" },
  ];

  let selectedFontSize = "Regular"; // Default font size
  const fontSizes = [
    { value: 'small', name: "Small" },
    { value: 'regular', name: "Regular" },
    { value: 'large', name: "Large" },
  ];

  let selectedTheme = "Light"; // Default theme selection
  let darkMode = false; // Initial dark mode state

  const themes = [
    { value: 'light', name: "Light" },
    { value: 'dark', name: "Dark" },
  ];

  // Function to update both selectedTheme and darkMode without cyclical dependency
  function updateTheme(theme) {
    selectedTheme = theme;
    darkMode = theme === "dark";
  }

  // Function to apply font size to the root element and save to localStorage
  function applyFontSize(size) {
    const root = document.documentElement;
    if (size === "small") {
      root.style.fontSize = "14px"; // Smaller font size
    } else if (size === "large") {
      root.style.fontSize = "18px"; // Larger font size
    } else {
      root.style.fontSize = "16px"; // Regular font size
    }
    localStorage.setItem("font-size", size); // Save preference
  }

  // Function to reset all settings to their defaults
  function resetSettings() {
    // Reset dropdown selections
    selectedColorMode = "normal";
    selectedFontSize = "Regular";
    selectedTheme = "Light";
    darkMode = false;

    // Clear saved preferences in localStorage
    localStorage.removeItem("font-size");
    localStorage.removeItem("color-theme");

    // Apply default font size and theme
    applyFontSize("Regular");
    updateTheme("Light");
  }

  // Reactively update font size when selectedFontSize changes
  $: applyFontSize(selectedFontSize);
</script>

<main>
  <h1 class="font-bold text-xl dark:text-white">Accessibility Options</h1>
  <div>
      <div id="left" class="float-left w-9/12 h-flex ">
          <div id="table" class="my-6">
              <Table noborder={true}>
                  <TableHead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-900 dark:text-gray-400 ">
                    <TableHeadCell>Setting</TableHeadCell>
                    <TableHeadCell>Description</TableHeadCell>
                    <TableHeadCell class="text-right px-6" style="width: 30%;">Option</TableHeadCell>
                  </TableHead>
                  <TableBody>
                      <TableBodyRow>
                          <TableBodyCell>Color mode:</TableBodyCell>
                          <TableHeadCell>Colorblind options</TableHeadCell>
                          <TableBodyCell class="text-right px-6" style="width: 30%;">
                            <Label>
                              Select an option
                              <Select items={colorModes} bind:value={selectedColorMode} />
                            </Label>
                          </TableBodyCell>
                      </TableBodyRow>
                      <TableBodyRow>
                        <TableBodyCell>Text size:</TableBodyCell>
                        <TableHeadCell>Size of the font on the website</TableHeadCell>
                        <TableBodyCell class="text-right px-6" style="width: 30%;">
                          <Label>
                            Select an option
                            <Select items={fontSizes} bind:value={selectedFontSize} on:change={() => applyFontSize(selectedFontSize)} />
                          </Label>
                        </TableBodyCell>
                      </TableBodyRow>
                      <TableBodyRow>
                        <TableBodyCell>Theme:</TableBodyCell>
                        <TableHeadCell>Light mode or dark mode</TableHeadCell>
                        <TableBodyCell class="text-right px-6" style="width: 30%;">
                          <Label>
                            Select an option
                            <Select items={themes} bind:value={selectedTheme} on:change={() => updateTheme(selectedTheme)} />
                          </Label>
                        </TableBodyCell>
                      </TableBodyRow>
                  </TableBody>
              </Table>
          </div>    
      </div>
  </div> 
  <Button class="mt-5" color="danger" on:click={resetSettings}>Reset</Button>

  <Colorblind bind:colorblindMode={selectedColorMode} showIcon={false} />
  <Darkmode bind:darkMode={darkMode} showIcon={false} />
</main>