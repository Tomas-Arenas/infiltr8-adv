<!--TODO test stores -->
<!--visual planning-->

<script>
    import { Card } from 'flowbite-svelte';
    import { TrashBinSolid } from 'flowbite-svelte-icons';
    import { ipsAllowed } from '$lib/stores.js';
    import { ipsDisallowed } from '$lib/stores.js';

    let exploitsAllowed = [
        { id: 1, name: 'SQL Injection', selected: false },
        { id: 2, name: 'DDOS Attack', selected: false },
        { id: 3, name: 'Default Credentials', selected: false },
        { id: 4, name: 'Missing Encryption', selected: false },
        { id: 5, name: 'Unauthenticated Port Bypass', selected: false },
        { id: 6, name: 'Weak Passwords', selected: false }
    ];

    let projects = [
        { id: 1, name: 'Example 1', size: '1.42 GB', items: 49 },
        { id: 2, name: 'Example 2', size: '2.8 GB', items: 286 },
        { id: 3, name: 'Example 3', size: '84 MB', items: 52 },
        { id: 4, name: 'Example 4', size: '1.6 GB', items: 109 },
        { id: 5, name: 'Example 5', size: '1.15 GB', items: 76 },
        { id: 6, name: 'Example 6', size: '1.3 GB', items: 43 },
        { id: 7, name: 'Example 7', size: '1.6 GB', items: 109 }
    ];

    let selectedProject = null;

    function moveUp(list, index) {
        if (index > 0) {
            [list[index - 1], list[index]] = [list[index], list[index - 1]];
            updateList(list);
        }
    }

    function moveDown(list, index) {
        if (index < list.length - 1) {
            [list[index], list[index + 1]] = [list[index + 1], list[index]];
            updateList(list);
        }
    }
    
    function addItem(list, item){
        list.push(item)
        updateList(list)
    }

    function deleteItem(list, index) {
        list.splice(index, 1);
        updateList(list);      
    }

    // Ensure the list is updated to trigger reactivity
    function updateList(list) {
        if (list === $ipsAllowed) {
            $ipsAllowed = [...list];
        }  else if (list === $ipsDisallowed) {
            $ipsDisallowed = [...list]
        }  else if (list === exploitsAllowed) {
            exploitsAllowed = [...list];
        }
        
    }

    function loadProject(project) {
        selectedProject = project;
        console.log(`Project ${project.name} loaded.`);
    }
</script>

<!-- Outer wrapper to center everything -->
<div class="flex flex-col items-center justify-center">
	<!-- Main container with both cards -->
	<Card class="flex min-w-fit flex-row gap-5 rounded-lg bg-gray-100 p-5 shadow-md dark:bg-gray-800">
		<!-- Current Project Folder Card -->
		<Card class="flex-1 rounded-lg bg-white p-5 shadow-md">
			<h2 class="mb-4 text-lg font-semibold">Current Project Folder</h2>
			{#if selectedProject}
				<div class="flex items-center justify-between rounded-lg bg-gray-100 p-4 shadow">
					<div class="flex items-center gap-3">
						<!-- Font Awesome folder icon -->
						<i class="fas fa-folder text-lg"></i>
						<div>
							<span class="block font-medium">{selectedProject.name}</span>
							<span class="text-sm text-gray-500"
								>{selectedProject.items} items • {selectedProject.size}</span
							>
						</div>
					</div>
					<span class="text-gray-500">⋮</span>
				</div>
			{/if}

			<!-- Scope IP List -->
			<div class="mt-6">
				<h3 class="mb-2 text-lg font-semibold">Scope IP List</h3>
				{#each $ipsAllowed as ip, index}
					<div class="mb-2 flex items-center justify-between rounded-lg bg-gray-100 p-3 shadow">
						<div class="flex items-center gap-3">
							<input type="checkbox" bind:checked={ip.selected} />
							<span>{ip.ip}</span>
						</div>
						<div class="flex gap-2">
							<button class="text-lg" on:click={() => moveUp($ipsAllowed, index)}>⬆</button>
							<button class="text-lg" on:click={() => moveDown($ipsAllowed, index)}>⬇</button>
                            <div class="flex gap-2">
                                <button class="text-lg" on:click={() => deleteItem($ipsAllowed, index)}>
                                  <TrashBinSolid class="w-6 h-6 text-red-600" /> <!-- Trash Icon Here -->
                                </button>
                            </div>

							<i class="fas fa-bars cursor-pointer"></i>
						</div>
					</div>
				{/each}
			</div>
            <!-- Scope IP List -->
			<div class="mt-6">
				<h3 class="mb-2 text-lg font-semibold">Scope IP List</h3>
				{#each $ipsAllowed as ip, index}
					<div class="mb-2 flex items-center justify-between rounded-lg bg-gray-100 p-3 shadow">
						<div class="flex items-center gap-3">
							<input type="checkbox" bind:checked={ip.selected} />
							<span>{ip.ip}</span>
						</div>
						<div class="flex gap-2">
							<button class="text-lg" on:click={() => moveUp($ipsAllowed, index)}>⬆</button>
							<button class="text-lg" on:click={() => moveDown($ipsAllowed, index)}>⬇</button>
                            <div class="flex gap-2">
                                <button class="text-lg" on:click={() => deleteItem($ipsAllowed, index)}>
                                  <TrashBinSolid class="w-6 h-6 text-red-600" /> <!-- Trash Icon Here -->
                                </button>
                            </div>

							<i class="fas fa-bars cursor-pointer"></i>
						</div>
					</div>
				{/each}
			</div>

			<!-- Exploits Allowed -->
			<div class="mt-6">
				<h3 class="mb-2 text-lg font-semibold">Exploits Allowed</h3>
				{#each exploitsAllowed as exploit, index}
					<div class="mb-2 flex items-center justify-between rounded-lg bg-gray-100 p-3 shadow">
						<div class="flex items-center gap-3">
							<input type="checkbox" bind:checked={exploit.selected} />
							<span>{exploit.name}</span>
						</div>
						<div class="flex gap-2">
							<button class="text-lg" on:click={() => moveUp(exploitsAllowed, index)}>⬆</button>
							<button class="text-lg" on:click={() => moveDown(exploitsAllowed, index)}>⬇</button>
							<i class="fas fa-bars cursor-pointer"></i>
						</div>
					</div>
				{/each}
			</div>
		</Card>

		<!-- Load Project Card -->
		<Card class="flex-1 rounded-lg bg-white p-5 shadow-md">
			<h3 class="mb-4 text-lg font-semibold">Load Project</h3>
			{#each projects as project}
				<div
					class="mb-4 flex cursor-pointer items-center justify-between rounded-lg bg-gray-100 p-4 shadow"
					on:click={() => loadProject(project)}
				>
					<div class="flex items-center gap-3">
						<!-- Font Awesome folder icon -->
						<i class="fas fa-folder text-lg"></i>
						<div>
							<span class="block font-medium">{project.name}</span>
							<span class="text-sm text-gray-500">{project.items} items • {project.size}</span>
						</div>
					</div>
					<span class="text-gray-500">⋮</span>
				</div>
			{/each}
		</Card>
	</Card>

	<!-- Start Testing button placed below the layout -->
	<button
		class="mt-6 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
		on:click={() => console.log('Start Testing')}>Start Testing</button
	>
</div>