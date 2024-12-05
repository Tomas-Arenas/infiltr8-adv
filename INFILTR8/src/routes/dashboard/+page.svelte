<script>
    // Drag and drop
    import { Dropzone } from 'flowbite-svelte';
    import { Input } from 'flowbite-svelte';
    import { Heading, Span, GradientButton } from 'flowbite-svelte';
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell
    } from 'flowbite-svelte';
    import { getArchetypesForProject, getIPsForProject } from '$lib/stores.js';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    let selectedFiles = [];
    let uploadInProgress = false;
    let allIpList = [];
    let allArchetypesList = [];
    let projects = [];
    let message = '';
    let resetRequests = [];
    let errorMessage = '';

    // Automatically handle file uploads after selection
    const handleDropzoneChange = async () => {
        if (selectedFiles.length > 0) {
            uploadInProgress = true;
            for (let file of selectedFiles) {
                await uploadNessusFile(file);
            }
            uploadInProgress = false;
        }
    };

    async function uploadNessusFile(file) {
        uploadInProgress = true;
        const formData = new FormData();
        formData.append('file', file);

        try {
            const uploadResponse = await fetch('/flask-api/nessus-upload', {
                method: 'POST',
                body: formData
            });

            if (uploadResponse.ok) {
                const result = await uploadResponse.json();
                allIpList.push({ name: result.filename, ips: getIPsForProject(result.filename) });
                allArchetypesList.push({
                    name: result.filename,
                    archetypes: getArchetypesForProject(result.filename)
                });
            } else {
                console.error('File upload failed:', uploadResponse.status);
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        } finally {
            uploadInProgress = false;
        }
    }

    async function fetchProjects() {
        try {
            const response = await fetch('/flask-api/all-projects', {
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                projects = data.data;
            } else {
                message = 'Failed to fetch projects';
                console.error('Fetch error:', response.status);
            }
        } catch (error) {
            message = 'No Projects';
            console.error('Error fetching projects:', error);
        }
    }

    async function fetchResetRequests() {
        try {
            const response = await fetch('/flask-api/get-password-reset-requests', {
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                resetRequests = data.requests;
            } else if (response.status === 403) {
                errorMessage = 'Access denied. Admins only.';
            } else {
                errorMessage = 'Failed to fetch reset requests.';
            }
        } catch (error) {
            errorMessage = 'An error occurred while fetching reset requests.';
            console.error(error);
        }
    }

    async function handleResetRequest(username, action) {
        try {
            const response = await fetch('/flask-api/approve-password-reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username,
                    action: action
                })
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data.message); // Log success message
                fetchResetRequests(); // Refresh the reset requests
            } else {
                const error = await response.json();
                console.error('Error:', error);
            }
        } catch (error) {
            console.error('Error in handleResetRequest:', error);
        }
    }

    async function createProject() {
        if (selectedFiles.length === 0 || document.getElementById('first_name').value === '') {
            message = 'Upload a .nessus file first.';
            console.warn(message);
            return;
        }

        let fileInfo = await Promise.all(allIpList);
        let fileInfoArchetypes = await Promise.all(allArchetypesList.map((item) => item.archetypes));
        let toSendIps = [];
        let toSendArchetypes = fileInfoArchetypes;
        let fileNames = [];

        for (let i = 0; i < fileInfo.length; i++) {
            let ip;
            await fileInfo[i]['ips'].then((result) => (ip = result));
            fileNames.push(fileInfo[i]['name']);
            toSendIps.push(ip);
        }

        const projectData = {
            fileName: fileNames,
            name: document.getElementById('first_name').value,
            ips: toSendIps,
            archetypes: toSendArchetypes
        };

        try {
            const response = await fetch('/flask-api/create-project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projectData),
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                message = `Project created successfully with ID: ${data.projectId}`;
                fetchProjects();
            } else {
                message = 'Failed to create project.';
                console.error('Project creation failed with status:', response.status);
            }
        } catch (error) {
            message = 'Error: ' + error.message;
            console.error('Error during project creation:', error);
        }
        goto('/project');
    }

    onMount(() => {
        fetchProjects();
        fetchResetRequests();
    });

    async function setCurrentProject(projectID) {
        try {
            const response = await fetch('/flask-api/set-currentProject', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ projectID })
            });

            if (!response.ok) {
                throw new Error('Failed to set current project');
            }

            const result = await response.json();
            console.log(result.message);
        } catch (error) {
            console.error('Error:', error);
        }
        goto('/project');
    }

    async function logButtonClick(detail) {
        console.log('Button clicked with detail:', detail); // For debugging
        try {
            const response = await fetch('/flask-api/log-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: 'DummyUser',
                    action: 'Dashboard click',
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
</script>

{#if resetRequests.length > 0}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md dark:bg-gray-800 dark:text-white">
            <h2 class="text-xl font-semibold mb-4">Pending Password Reset Requests</h2>
            <div class="overflow-y-auto max-h-64">
                <Table hoverable={true}>
                    <TableHead>
                        <TableHeadCell>Username</TableHeadCell>
                        <TableHeadCell>Action</TableHeadCell>
                    </TableHead>
                    <TableBody>
                        {#each resetRequests as request}
                            <TableBodyRow>
                                <TableBodyCell>{request.username}</TableBodyCell>
                                <TableBodyCell>
                                    <button
                                        class="text-green-600 hover:underline mr-2"
                                        on:click={() => handleResetRequest(request.id, 'approve')}
                                    >
                                        Accept
                                    </button>
                                    <button
                                        class="text-red-600 hover:underline"
                                        on:click={() => handleResetRequest(request.id, 'deny')}
                                    >
                                        Deny
                                    </button>
                                </TableBodyCell>
                            </TableBodyRow>
                        {/each}
                    </TableBody>
                </Table>
            </div>
            <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600" on:click={() => (resetRequests = [])}>
                Close
            </button>
        </div>
    </div>
{/if}

<div class="flex min-h-screen w-full flex-row items-start justify-between">
    <div class="mix-h-screen flex w-full flex-col items-center p-6">
        <Heading tag="h1" class="mb-16 text-center text-3xl font-extrabold md:text-5xl lg:text-6xl">
            <Span gradient>WELCOME TO INFILTR8</Span>
        </Heading>
        <div class="grid grid-cols-2 gap-10 w-full max-w-screen-lg mx-auto">
            <!-- Column 1: File Upload Section -->
            <div class="col-span-1">
                <div class="flex flex-col items-center">
                    <Dropzone
                        accept=".nessus"
                        multiple
                        bind:files={selectedFiles}
                        on:change={handleDropzoneChange}
                        class="mx-auto max-w-lg"
                    >
                        <p class="text-center text-gray-600 dark:text-gray-50">
                            Drag & drop your .nessus files here, or click to select files.
                        </p>
                    </Dropzone>
                    <div class="mt-4">
                        {#if selectedFiles.length > 0}
                            <h3 class="text-center text-lg font-semibold dark:text-gray-50">Selected Files</h3>
                            <ul class="mt-2 list-inside list-disc text-center dark:text-gray-300">
                                {#each selectedFiles as file}
                                    <li>{file.name}</li>
                                {/each}
                            </ul>
                        {:else}
                            <p class="text-center text-gray-500 dark:text-gray-400">No files selected.</p>
                        {/if}
                    </div>
                    <form class="mt-4 w-full">
                        <Input
                            class="text-center"
                            type="text"
                            id="first_name"
                            placeholder="Enter Project Name"
                            required
                        />
                    </form>
                    <div class="mt-4">
                        <p class="text-center dark:text-gray-50 mb-4">
                            Please select from the following to get started on your project.
                        </p>
                        <div class="flex justify-center gap-x-6">
                            <GradientButton color="green" on:click={() => logButtonClick('Discard All clicked')}>
                                Discard All
                            </GradientButton>
                            <GradientButton
                                on:click={() => {
                                    logButtonClick('Create Project clicked');
                                    createProject();
                                }}
                                disabled={uploadInProgress || selectedFiles.length === 0}
                            >
                                Create Project
                            </GradientButton>
                        </div>
                    </div>
                </div>
            </div>
        
            <!-- Column 2: Project List Section -->
            <div class="col-span-1">
                <h3 class="mb-4 text-center text-2xl font-semibold dark:text-gray-50">Project List</h3>
                {#if projects.length > 0}
                    <div class="max-h-96 w-full overflow-auto">
                        <Table hoverable={true} class="w-full">
                            <TableHead>
                                <TableHeadCell>Select</TableHeadCell>
                                <TableHeadCell>Project Name</TableHeadCell>
                            </TableHead>
                            <TableBody>
                                {#each projects as project}
                                    <TableBodyRow>
                                        <TableBodyCell>
                                            <input
                                                type="radio"
                                                name="project"
                                                value={project.projectId}
                                                on:change={() => setCurrentProject(project.projectId)}
                                            />
                                        </TableBodyCell>
                                        <TableBodyCell>{project.projectName}</TableBodyCell>
                                    </TableBodyRow>
                                {/each}
                            </TableBody>
                        </Table>
                    </div>
                {:else}
                    <p class="text-center">No projects. Create a project!</p>
                {/if}
            </div>
        </div>
    </div>
</div>
        