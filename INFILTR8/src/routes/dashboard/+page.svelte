<script>
    import { Heading, P, Span, GradientButton } from 'flowbite-svelte';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
    import { onMount } from 'svelte';
    
    let nessusFile;
    let message = "";
    let projectInfo = null;
    let projects = [];
    
    async function fetchProjects() {
        try {
            const response = await fetch('http://localhost:5000/flask-api/all-projects', {
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                projects = data.data; 
            } else {
                message = "Failed to fetch projects";
                console.error("Fetch error:", response.status);
            }
        } catch (error) {
            message = "Error fetching projects";
            console.error("Error fetching projects:", error);
        }
    }

    onMount(() => {
        fetchProjects();
    });

    const handleChange = (event) => {
        const target = event.target;
        const files = target?.files;
    
        if (files && files.length > 0) {
            const file = files[0];
            const fileExtension = file.name.split('.').pop()?.toLowerCase();
    
            if (fileExtension === 'nessus') {
                nessusFile = file;
                console.log("File selected:", nessusFile);
                uploadNessusFile();
            } else {
                console.error('Invalid file type. Please upload a .nessus file.');
            }
        }
    };

    async function uploadNessusFile() {
        if (!nessusFile) {
            message = "Please select a file to upload.";
            return;
        }

        const formData = new FormData();
        formData.append("file", nessusFile);

        try {
            const uploadResponse = await fetch("http://localhost:5000/flask-api/nessus-upload", {
                method: "POST",
                body: formData,
            });

            if (uploadResponse.ok) {
                const result = await uploadResponse.json();
                message = "File uploaded successfully: " + result.status;
            } else {
                message = "File upload failed. Please try again.";
            }
        } catch (error) {
            message = "Upload error: " + error.message;
        }
    }

    async function createProject() {
        if (!nessusFile) {
            message = "Upload a .nessus file first.";
            return;
        }

        const projectData = {
            folderName: nessusFile.name,
        };

        try {
            const response = await fetch("http://localhost:5000/flask-api/create-project", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(projectData),
                credentials: "include"
            });

            if (response.ok) {
                const data = await response.json();
                projectInfo = { id: data.projectId, name: nessusFile.name };
                message = `Project created successfully with ID: ${data.projectId}`;
                console.log(message);
                fetchProjects(); // Refresh project list after creating a new project
            } else {
                message = "Failed to create project.";
            }
        } catch (error) {
            message = "Error: " + error.message;
        }
    }
</script>

<div class="flex flex-col items-center min-h-screen w-full p-6">
    <Heading tag="h1" class="mb-4 text-3xl font-extrabold text-center md:text-5xl lg:text-6xl">
        <Span gradient>WELCOME TO INFILTR8</Span>
    </Heading>
    <P class="text-center mb-8">Please select from the following to get started on your project.</P>

    <input type="file" accept=".nessus" on:change="{handleChange}" class="border p-2 rounded mb-6" />

    <div class="flex flex-col items-center mb-8 w-full">
        <GradientButton class="mb-2" color="green">Discard All</GradientButton>
        <GradientButton on:click={createProject}>Create Project</GradientButton>
    </div>

    <div class="w-full">
        <h2 class="text-2xl font-semibold mb-4 text-center">Project List</h2>
        
        {#if projects.length > 0}
            <Table hoverable={true} class="w-full">
                <TableHead>
                    <TableHeadCell>Project Name</TableHeadCell>
                    <TableHeadCell>Project ID</TableHeadCell>
                    <TableHeadCell>IPs</TableHeadCell>
                    <TableHeadCell>Exploits</TableHeadCell>
                </TableHead>
                <TableBody>
                    {#each projects as project}
                        <TableBodyRow>
                        <TableBodyCell>{project.projectname}</TableBodyCell>
                        <TableBodyCell>{project.projectId}</TableBodyCell>
                        <TableBodyCell>{project.ips ? project.ips.join(', ') : ''}</TableBodyCell>
                        <TableBodyCell>
                          {#if Array.isArray(project.exploits)}
                              {project.exploits.join(', ')}
                          {:else}
                              {project.exploits} <!-- Displays the string if it's not an array -->
                          {/if}
                      </TableBodyCell> 
                      </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        {:else if message}
            <p class="text-center text-red-500">{message}</p>
        {:else}
            <p class="text-center">Loading projects...</p>
        {/if}
    </div>
</div>
