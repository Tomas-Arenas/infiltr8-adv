<script>
    import { SystemInfo } from '../../lib/SystemInfo.js'
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
    import { Label, Select, Button } from 'flowbite-svelte';
    import { onMount } from 'svelte';
    import { session, checkSession } from '$lib/stores/session.js';

    onMount(() => {
        checkSession(); // Check session on page load
    });

    const sysInfo = new SystemInfo()
    let selectedColorMode = "Normal";
    const colorModes = [
      {value: 'normal', name: "Normal"},
      {value: 'red-green', name: "Red-Green"},
      {value: 'blue-yellow', name: "Blue-Yellow"},
      {value: 'monochrome', name: "Monochrome"},
    ];

    let selectedFonzSize = "Regular";
    const fontSizes = [
      {value: 'small', name: "Small"},
      {value: 'regular', name: "Regular"},
      {value: 'large', name: "Large"},
    ];

    let selectedTheme = "Light";
    const themes = [
      {value: 'light', name: "Light"},
      {value: 'dark', name: "Dark"},
    ];
   
</script>

<!-- whole page -->
<main>
    <h1 class="font-bold text-xl dark:text-white">Accessibility Options</h1>
    <div>
        <div id="left" class="float-left  w-9/12 h-flex ">
            <div id="table" class="my-6">
                <Table noborder={true}>
                    <TableHead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-900 dark:text-gray-400 ">
                      <TableHeadCell>Setting</TableHeadCell>
                      <TableHeadCell>Description</TableHeadCell>
                      <TableHeadCell class="text-right px-6" style="width: 30%;">Option</TableHeadCell>
                    </TableHead>
                    <TableBody>
                    <TableBodyRow class=" " on:click>
                        <TableBodyCell>Color mode: </TableBodyCell>
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
                          <Select items={fontSizes} bind:value={selectedFonzSize} />
                        </Label>
                      </TableBodyCell>
                    </TableBodyRow>
                    <TableBodyRow>
                      <TableBodyCell>Theme:</TableBodyCell>
                      <TableHeadCell>Light mode or dark mode</TableHeadCell>
                      <TableBodyCell class="text-right px-6" style="width: 30%;">
                        <Label>
                          Select an option
                          <Select items={themes} bind:value={selectedTheme} />
                        </Label>
                      </TableBodyCell>
                    </TableBodyRow>
                    </TableBody>
                </Table>
              </div>    
        </div>
    </div> 
    <div class="mt-5">
    </div>
    <Button class="mt-5" color="primary">Save</Button>
    <Button class="mt-5" color="danger">Reset</Button>
</main>
