<script>
    // Drag and drop
    import { Dropzone } from 'flowbite-svelte';
    import { Heading, P, Span } from 'flowbite-svelte';
    import { GradientButton } from 'flowbite-svelte';
    import { Progressbar } from 'flowbite-svelte';

    
    // Initialize the array to hold file names
    let value = [];
    
    // Handle file drop
    const dropHandle = (event) => {
      value = [];
      event.preventDefault();
    
      if (event.dataTransfer && event.dataTransfer.items) {
        [...event.dataTransfer.items].forEach((item) => {
          if (item.kind === 'file') {
            const file = item.getAsFile();
            if (file) {
              value.push(file.name);
            }
          }
        });
      } else if (event.dataTransfer && event.dataTransfer.files) {
        [...event.dataTransfer.files].forEach((file) => {
          value.push(file.name);
        });
      }
      value = [...value]; // Ensure reactivity
    };
    
    // Handle input change for file uploads
    const handleChange = (event) => {
      const target = event.target;
      const files = target?.files;
    
      if (files && files.length > 0) {
        const file = files[0];
        const fileExtension = file.name.split('.').pop()?.toLowerCase();
    
        if (fileExtension === 'nessus') {
          // If the file is a .nessus file, add its name to the value array
          value.push(file.name);
          value = [...value]; // Ensure reactivity in Svelte
        } else {
          console.error('Invalid file type. Please upload a .nessus file.');
        }
      }
    };
    
    // Display the uploaded files
    const showFiles = (files) => {
      if (files.length === 1) return files[0];
      let concat = '';
      files.forEach((file) => {
        concat += file + ', ';
      });
    
      if (concat.length > 40) concat = concat.slice(0, 40);
      concat += '...';
      return concat;
    };
    </script>
  <div class="flex flex-col items-center justify-center min-h-screen max-w-fit">
    <Heading tag="h1" class="mb-4" customSize="text-3xl text-center font-extrabold  md:text-5xl lg:text-6xl">
      <Span gradient>WELCOME TO INFILTR8</Span>
    </Heading>
    <P>Please select from the follwing to get started on your project.</P>
  
    <!-- Dropzone component for file uploads -->
    <Dropzone
      id="dropzone"
      class='w-96'
      on:drop={dropHandle}
      on:dragover={(event) => {
        event.preventDefault();
      }}
      on:change={handleChange}>
      <svg aria-hidden="true" class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
      </svg>
      {#if value.length === 0}
        <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
        <p class="text-xs text-gray-500 dark:text-gray-400">Only .NESSUS files allowed</p>
      {:else}
        <p>{showFiles(value)}</p>
      {/if}
    </Dropzone>
    <div class="flex flex-col mr-80">

    <GradientButton class = "mb-2" color="green">Discard All</GradientButton>
    <GradientButton color="purple">Create Project</GradientButton>
    </div>
    <div class="mb-1 text-base font-medium dark:text-white">Gray</div>
    <Progressbar progress="50" color="gray" />
</div>
<div class="my-4">
    <div class="mb-1 text-base font-medium text-blue-700 dark:text-blue-500">Blue</div>
    <Progressbar progress="50" color="blue" />
  </div>
  
  <div class="my-4">
    <div class="mb-1 text-base font-medium text-red-700 dark:text-red-500">Red</div>
    <Progressbar progress="50" color="red" />
  </div>
  
  <div class="my-4">
    <div class="mb-1 text-base font-medium text-green-700 dark:text-green-500">Green</div>
    <Progressbar progress="50" color="green" />
  </div>
  
  <div class="mb-1 text-base font-medium text-yellow-700 dark:text-yellow-500">Yellow</div>
  <div class="my-4">
    <Progressbar progress="50" color="yellow" />
  </div>
  
  <div class="mb-1 text-base font-medium text-indigo-700 dark:text-indigo-400">Indigo</div>
  <div class="my-4">
    <Progressbar progress="50" color="indigo" />
  </div>
  
  <div class="mb-1 text-base font-medium text-purple-700 dark:text-purple-400">Purple</div>
  <div class="my-4">
    <Progressbar progress="50" color="purple" />
  </div>
    <div>

  </div>

    