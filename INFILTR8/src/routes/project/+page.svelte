<script>
    import IP from '$lib/IP.js';
    import { Card, Button, ButtonGroup, Listgroup, ListgroupItem, P } from 'flowbite-svelte';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { get } from 'svelte/store';
    import { ipsAllowed, ipsDisallowed } from "$lib/stores.js"; // Import stores
    import { projectName, fileId } from '$lib/CurrentProject';


    let selectedProject = null;
    let selectedProjectName = null;
    let allIps = [];
    let selectedIps = [];
    let showModal = false; 
    let newIP = "";
    let files = []
    $: selected = 1

    
    let exploitsAllowed = [
        { id: 1, name: 'SQL Injection', selected: true },
        { id: 2, name: 'DDOS Attack', selected: true },
        { id: 3, name: 'Default Credentials', selected: true },
        { id: 4, name: 'Missing Encryption', selected: true },
        { id: 5, name: 'Unauthenticated Port Bypass', selected: true },
        { id: 6, name: 'Weak Passwords', selected: true }
    ];

    async function fetchFiles() {
        try {
            const response = await fetch('/flask-api/file-count');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`)
            }
            let totalFiles, currentFileId
            const data = await response.json()
            totalFiles = data.data
            console.log(data.currentFile)
            currentFileId = data.currentFile
            console.log(totalFiles)
            for(let i=1;i<=totalFiles;i++) {
                files.push({id:i, file: i})
                files = [...files]
            }
            console.log(files)
            selected = files[currentFileId - 1];
        } catch (error) {
            console.error("Failed to get file amount", error);
        }
    }

    async function changeFile() {
        let message
        console.log('in the change ',selected.file)
        try {
            const response = await fetch("/flask-api/change-selected-file", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({fileId: selected.file}),
                credentials: "include"
            });

        if (response.ok) {
            message = `File selected with`;
            fileId.set(selected.file)
            console.log(message);
            fetchProjectInfo(); 
        } else {
            message = "Couldn't change file";
            console.error("Couldn't change file", response.status);
        }
      } catch (error) {
          message = "Error: " + error.message;
          console.error("Error during file change:", error);
      }
    }

    async function fetchProjectInfo(){
        try {
            const response = await fetch('/flask-api/current-project-info-many-test');
        
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            selectedProjectName = data.data.projectName
            selectedIps = data.data.ips 
            allIps = data.data.ips
            selectedProject = data.data;
            console.log(selectedProject);
            const allowedIPInstances = selectedIps.map(ipAddress => new IP(ipAddress));
            ipsAllowed.set(allowedIPInstances);
            projectName.set(selectedProjectName)
            fileId.set(data.fileId)
        } catch (error) {
            console.error("Failed to fetch current project info", error);
        }
    }

    function toggleIpSelection(ip) {
        if (selectedIps.includes(ip)) {
            // If already selected, remove it
            selectedIps = selectedIps.filter(selectedIp => selectedIp !== ip);
        } else {
            // If not selected, add it
            selectedIps = [...selectedIps, ip];
        }
        const allowedIPInstances = selectedIps.map(ipAddress => new IP(ipAddress));
        const disallowedIPInstances = allIps
        .filter(ipAddress => !selectedIps.includes(ipAddress))
        .map(ipAddress => new IP(ipAddress));

        ipsAllowed.set(allowedIPInstances);
        ipsDisallowed.set(disallowedIPInstances);

        console.log("Selected IPs for scope:", selectedIps);
        console.log("Disallowed IPs:", disallowedIPInstances.map(ip => ip.ip));
    }

    function addIP(data) {
        if (Array.isArray(data)) {
        data.forEach(ipString => {
            let tempIp = new IP(ipString);
            allIps = [...allIps, tempIp.ip]; 
            selectedIps = [...selectedIps, tempIp.ip];
        });
        } else {
            // Handle the case where data is not an array (if needed)
            let tempIp = new IP(data);
            allIps = [...allIps, tempIp.ip]; 
            selectedIps = [...selectedIps, tempIp.ip];
        }

    }


    function isValidIPv4(ip) {
        const ipv4Regex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9][0-9]?)\.(25[0-5]|2[0-4][0-9][0-9]?)$/;
        return ipv4Regex.test(ip);
    }

    function handleAddIP() {
        if (newIP) {
            addIP(newIP);
            newIP = ""; 
            showModal = false; 
        }
    }

    function handleImportIPs() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function(event) {
                const fileContent = event.target.result;
                const importedIPs = fileContent.split(/\r?\n/).filter(ip => ip.trim() !== '');
                addIP(importedIPs);
            };

            reader.onerror = function(event) {
                console.error("File could not be read! Code " + event.target.error.code);
            };

            reader.readAsText(file);
        } else {
            console.log("No file selected.");
        }
    }

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

    // Update list for reactivity
    function updateList(list) {
        if (list === $ipsAllowed) {
            ipsAllowed.set([...list]);
        } else if (list === $ipsDisallowed) {
            ipsDisallowed.set([...list]);
        } else if (list === exploitsAllowed) {
            exploitsAllowed = [...list];
        }
    }

    async function startAnalysis() {
        console.log(selectedProject)
        console.log(selectedProject.projectId)
        if (!selectedProject || !selectedProject.file) {
            alert("Please select a project with a valid ID before starting testing.");
            return;
        }
        if (get(ipsAllowed).map(item => item.ip).length == 0) {
            ipsAllowed.set(selectedIps.map(ipAddress => new IP(ipAddress)));
        }
        console.log(get(ipsAllowed).map(item => item.ip))
        const selectedExploits = exploitsAllowed.filter(exp => exp.selected).map(exp => exp.name);
        try {
            const response = await fetch('/flask-api/process-nessus' ,{
               method:'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify({
                projectId: selectedProject.projectId,
                disallowedIps: get(ipsAllowed).map(item => item.ip),
                archetypes: exploitsAllowed
               }) 
            });
            
            // Check if the response is OK (status 200)
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            
            // Parse the JSON response
            const data = await response.json();
            
            // Handle the response data
            console.log(data.message);  // or update the UI as needed  
            console.log("process-nessus called and sent disallowed ips:",get(ipsDisallowed).map(item => item.ip));
        } catch (error) {
            console.error('Error calling /flask-api/process-nessus:', error);
        }
        goto('/analysis')
    }

    async function deleteProject() {
        if (!selectedProject || !selectedProject.fileId) {
            alert("Please select a project with a valid ID before deleting project.");
            return;
        }
        try {
            const response = await fetch('/flask-api/delete-current-project');
            
            // Check if the response is OK (status 200)
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            
            // Parse the JSON response
            const data = await response.json();
            
            // Handle the response data
            console.log(data.message);  // or update the UI as needed
            alert(data.message)
        } catch (error) {
            console.error('Error calling /flask-api/delete-current-project:', error);
        }
        goto('/dashboard')
    }

    async function logButtonClick(detail) {
        console.log("Button clicked with detail:", detail);  // For debugging
        try {
            const response = await fetch('/flask-api/log-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: 'DummyUser',
                    action: 'Project click',
                    details: detail
                })
            });

            if (!response.ok) {
                throw new Error('Failed to log action');
            }
            const result = await response.json();
            console.log('Action logged:', result);
        } catch (error) {
            console.error('Failed to log button click:', error);
        }
    }

    onMount(() => {
        fetchProjectInfo()
        fetchFiles()
        //getIPsFromBackend();

    });
</script>

<!-- Outer wrapper to center everything -->
<div class="min-h-screen flex flex-col items-center justify-center">
    {#if selectedProjectName === null}
    <h1 class="text-2xl font-bold mb-6 text-red-700"> No Project Selected </h1>
    {:else}
    <h1 class="text-2xl font-bold mb-6 text-white"> {selectedProjectName} - File {selectedProject.fileId}</h1>
    <div class="mb-1 align-middle">
        <p class="mb-1 text-center"><strong>Select a File</strong></p>
        <select 
        bind:value={selected}
        on:click={changeFile}
        class="w-half p-2 rounded-lg bg-gray-700 text-white border border-gray-500"
        placeholder={"Selected a issue type"}>
        {#each files as file}
            <option value={file}>
            File {file.file}
            </option>
        {/each}
        </select>
    </div>
    {/if}
	<!-- Main container with cards -->
	<Card class="flex min-w-fit flex-row gap-5 rounded-lg bg-gray-100 p-5 shadow-md dark:bg-gray-800"> 
        <!-- Show current IP list -->
        <Card class="flex-1 rounded-lg bg-white p-5 shadow-md">
            <h2 class="mb-4 text-lg font-semibold text-center">Current Project IPS</h2>
            <Listgroup class="border-none">
                {#each allIps as ip, index}
                    <ListgroupItem class="flex items-center gap-3 justify-between rounded-lg bg-gray-100 p-4 shadow dark:bg-gray-800 mb-4">
                        <input type="checkbox" checked on:change={() => toggleIpSelection(ip)} />
                        <span>{ip}</span>
                    </ListgroupItem>
                {/each}
            </Listgroup>
            
            <div class="mt-4 flex flex-col items-start">
                <div class="flex justify-between w-full">
                    <button on:click={() => showModal = true} class="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600">
                        Add IP
                    </button>
                    <button on:click={handleImportIPs} class="bg-green-500 text-white rounded-lg px-4 py-2 hover:bg-green-600">
                        Import IPs
                    </button>
                </div>
                <div class="mt-2">
                    <label for="fileInput" class="block text-gray">
                        Select .txt to import IPs
                    </label>
                    <input type="file" id="fileInput" accept=".txt" class="mt-1" />
                </div>
            </div>
        </Card>

        {#if showModal}
            <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
                <div class="bg-white rounded-lg p-5 shadow-md">
                    <h3 class="mb-4 text-lg font-semibold">Add IP Address</h3>
                    <input 
                        type="text" 
                        placeholder="Enter IP address" 
                        bind:value={newIP} 
                        class="border p-2 rounded w-full mb-4"
                    />
                    <div class="flex justify-end">
                        <button on:click={handleAddIP} class="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600">
                            Add
                        </button>
                        <button on:click={() => showModal = false} class="ml-2 bg-gray-300 text-black rounded-lg px-4 py-2 hover:bg-gray-400">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        {/if}


        <Card class="flex-1 rounded-lg bg-white p-5 shadow-md">
            <h2 class="mb-4 text-lg font-semibold text-center">Archetypes Allowed</h2>           
                <Listgroup class="border-none">
                    {#each exploitsAllowed as exploit, index}
                        <ListgroupItem class="flex items-center gap-3 justify-between rounded-lg bg-gray-100 p-4 shadow dark:bg-gray-800 mb-4">                  
                            <input type="checkbox" bind:checked={exploit.selected} />
                            <span>{exploit.name}</span>
                            <ButtonGroup class="*:!ring-primary-700">
                                <Button size="sm mr-2" on:click={() => moveUp(exploitsAllowed, index)}>⬆</Button>
                                <Button size="sm mr-2" on:click={() => moveDown(exploitsAllowed, index)}>⬇</Button>             
                            </ButtonGroup >						
                        </ListgroupItem>
                    {/each}
                </Listgroup>

        </Card>
    </Card>

	<!-- Start Testing button placed below the layout -->
    <div class="flex justify-between w-1/2">
        <button
            class="mt-6 rounded-lg bg-red-600 px-6 py-3 font-semibold text-white hover:bg-red-700"
            on:click={deleteProject}>Delete Project</button>
        <button
        class="mt-6 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
        on:click={startAnalysis}>Start Analysis</button>
    </div>
</div>
