<script>
    // Drag and drop
    import { Dropzone } from 'flowbite-svelte';
    import { Progressbar } from 'flowbite-svelte';
    import { Listgroup } from 'flowbite-svelte';
    import { Alert } from 'flowbite-svelte';
    import { Input } from 'flowbite-svelte';
    import { InfoCircleSolid } from 'flowbite-svelte-icons';
    import { Heading, P, Span, GradientButton } from 'flowbite-svelte';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
    import { getArchetypesForProject, getIPsForProject } from '$lib/stores.js'
	import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    
    let simpleList = ['Test1'];
    let folderName = '';
    
    let nessusFile;
    let message = "";
    let isLoading = true
    let ipList = []
    let allIpList = []
    let allArchetypesList = []
    let projectInfo = null;
    let possibleEntryPoints = [];
    let validEntryPoints = [];
    let projects = [];
    let resetRequests = [];
    let errorMessage = '';
    let upLoadDone = false;
    
    // Initialize the array to hold file names
    let value = [];
    let currentUser = ''
    // gets username
    async function checkSession(){
        try{
            const response = await fetch('/flask-api/check_session',{
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok){
                const sessionData = await response.json();
                if (sessionData.logged_in){
                    currentUser = sessionData.username;
                }else{
                    console.error("User is not logged in");
                }
            } else{
                console.error("Failed to fetch session data");
            }

        }catch (error){
            console.error("Error checking session:", error);
        }
    }
    
    // Handle file drop
    const dropHandle = (event) => {
      console.log("File drop detected");
      event.preventDefault();
      if (event.dataTransfer && event.dataTransfer.files.length > 0) {
        nessusFile = event.dataTransfer.files[0];
        console.log("File selected:", nessusFile);
        uploadNessusFile();
      }
    };

    // Function to parse Nessus XML content
    function parseNessusFile(content) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(content, "application/xml");
      possibleEntryPoints = [];

      // Example of extracting IP and port info
      const hosts = xmlDoc.getElementsByTagName("ReportHost");
      possibleEntryPoints = [];
      for (let host of hosts) {
        const ip = host.getAttribute("name");
        const reportItems = host.getElementsByTagName("ReportItem");
        for (let item of reportItems) {
          const port = item.getAttribute("port");
          const severity = item.getAttribute("severity"); // Example attribute, might need adjustment based on your Nessus file
          const pluginID = item.getAttribute("pluginID");
          const service = item.getAttribute("svc_name");

          // Collect only relevant data, e.g., open ports and severity levels
          possibleEntryPoints.push({ ip, port, severity, pluginID, service });
        }
      }
      // console.log("Parsed entry points:", possibleEntryPoints);
    }

    // Function to validate entry points based on open ports or severity levels
    function validateEntryPoints() {
      validEntryPoints = possibleEntryPoints.filter(point => {
        // Logic: Only include entries with high severity (severity level 3 or more)
        const severityThreshold = 3; // Example threshold: 3 = medium, 4 = high, 5 = critical
        const isHighSeverity = parseInt(point.severity) >= severityThreshold;

        // Logic: Only include open ports (you might need to adjust based on Nessus data for open/closed port status)
        const isValidPort = point.port > 0;

        // Combine both conditions
        return isHighSeverity && isValidPort;
      });
    }
    async function handleResetRequest(username, action) {
    try {
        const response = await fetch("/flask-api/approve-password-reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,  // Ensure `username` is set
                action: action       // Ensure `action` is set (e.g., 'approve' or 'deny')
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data.message); // Log success message
            fetchResetRequests()
            console.log(resetRequests)
        } else {
            const error = await response.json();
            console.error("Error:", error);
        }
    } catch (error) {
        console.error("Error in handleResetRequest:", error);
    }
}


    
    // Handle input change for file upload
    async function fetchResetRequests() {
        try {
            const response = await fetch('/flask-api/get-password-reset-requests', {
                method: 'GET',
                credentials: 'include'  // Ensure cookies are included in the request
            });
            if (response.status === 403) {
                errorMessage = 'Access denied. Admins only.';
            } else if (response.ok) {
                const data = await response.json();
                resetRequests = data.requests;
    
            } else {
                errorMessage = 'Failed to fetch reset requests';
            }
        } catch (error) {
            errorMessage = 'An error occurred while fetching reset requests';
            console.error(error);
        }
    }
    async function checkRequestStatus() {
        console.log("Checking request status...");  // Debug: Initial log to confirm function call

        if (!checkUsername) {
            console.error("No username provided.");  // Debug: Log if username is missing
            alert("Please enter your username.");
            return;
        }

        try {
            const response = await fetch("/flask-api/password-reset-status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: checkUsername })
            });

            console.log("Response status:", response.status);  // Debug: Log response status

            if (response.ok) {
                const data = await response.json();
                console.log("Password reset request status:", data);  // Debug: Log successful response data
                requestStatusMessage = `Your request status: ${data.status}, Timestamp: ${new Date(data.timestamp).toLocaleString()}`;
            } else {
                const error = await response.json();
                console.error("Error response:", error);  // Debug: Log error response from server
                requestStatusMessage = error.error || "Failed to check request status.";
            }
        } catch (error) {
            console.error("Error in checkRequestStatus:", error);  // Debug: Log any unexpected errors
            alert("An error occurred while checking the password reset request status.");
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
                message = "Failed to fetch projects";
                console.error("Fetch error:", response.status);
            }
        } catch (error) {
            message = "No Projects";
            console.error("Error fetching projects:", error);
        }
    }

    onMount(() => {
        fetchResetRequests();
        fetchProjects();
        checkSession()
    });

    const handleChange = (event) => {
        const target = event.target;
        const files = target?.files;
        let nessusContent
    
        if (files && files.length > 0) {
            let temp
            console.log(files.length)
            for (let i=0;i<files.length;i++) {
                temp = files[i];
                console.log("File selected in for loop:", temp);
                const file = files[i];
                const fileExtension = file.name.split('.').pop()?.toLowerCase();
        
                if (fileExtension === 'nessus') {
                    nessusFile = file;
                    // console.log("File selected:", nessusFile);
                    let fetchP = uploadNessusFile()
                    // fetchP.then((response) => {
                    //     // put error handle stuff here
                    //     console.log("in the fetch ",nessusFile.name)
                    //     ipList = getIPsForProject(nessusFile.name)
                    // })
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        nessusContent = e.target.result;
                        parseNessusFile(nessusContent);
                    };
                    reader.readAsText(file);
                } else {
                    console.error('Invalid file type. Please upload a .nessus file.');
                }
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

    async function uploadNessusFile() {
        if (!nessusFile) {
            message = "Please select a file to upload.";
            return;
        }

        const formData = new FormData();
        formData.append("file", nessusFile);
        console.log(nessusFile.name)
        try {
            const uploadResponse = await fetch("/flask-api/nessus-upload", {
                method: "POST",
                body: formData,
            });

            if (uploadResponse.ok) {
                const result = await uploadResponse.json();
                allIpList.push({"name": result.filename, "ips": getIPsForProject(result.filename)});
                allArchetypesList.push({"name": result.filename, "archetypes": getArchetypesForProject(result.filename)}); 
            } else {
                return message = "File upload failed. Please try again.";
            }
        } catch (error) {
            return message = "Upload error: " + error.message;
        }
    }

  async function createProject() {
      if (!nessusFile || document.getElementById("first_name").value === "") {
          message = "Upload a .nessus file first.";
          console.warn(message);
          return;
      }
      let fileInfo
      fileInfo = await Promise.all(allIpList)
      let fileInfoArchetypes;
      fileInfoArchetypes = await Promise.all(allArchetypesList.map(item => item.archetypes));
      console.log("Resolved archetypes:", fileInfoArchetypes);

      console.log('see length of list ', fileInfo.length)
      console.log(fileInfo[0]['ips'])
      let toSendIps = []
      let toSendArchetypes = fileInfoArchetypes
      let fileNames = []
      for (let i=0;i<fileInfo.length;i++){
        let ip
        await fileInfo[i]['ips'].then(function(result){ip = result})
        fileNames.push(fileInfo[i]['name'])
        toSendIps.push(ip)
      }
      console.log(toSendIps)
    //   let ips
    //   await fileInfo[0]['ips'].then(function(result){ips = result})
      const projectData = {
          fileName: fileNames,
          name: document.getElementById("first_name").value,
          ips: toSendIps,
          archetypes: toSendArchetypes
      };

        try {
            const response = await fetch("/flask-api/create-project", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(projectData),
                credentials: "include"
            });

        if (response.ok) {
            const data = await response.json();
            projectInfo = { id: data.projectId, name: nessusFile.name };

            message = `Project created successfully with ID: ${data.projectId} and archetypes = ${toSendArchetypes}`;
            console.log(message);
            fetchProjects(); 
        } else {
            message = "Failed to create project.";
            console.error("Project creation failed with status:", response.status);
        }
      } catch (error) {
          message = "Error: " + error.message;
          console.error("Error during project creation:", error);
      }
      goto('/project')
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
                    username: currentUser,  // Dummy username for now
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
        goto('/project')
    }

</script>
<!-- Password Reset Request Modal -->
{#if resetRequests.length > 0}
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-800 bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md dark:bg-gray-800 dark:text-white">
            <h2 class="text-xl font-semibold mb-4">Pending Password Reset Requests</h2>
            
            <!-- Scrollable container for the table -->
            <div class="overflow-y-auto max-h-64">
                <Table hoverable={true} class="shrink">
                    <TableHead>
                        <TableHeadCell>Username</TableHeadCell>
                        <TableHeadCell>Action</TableHeadCell>
                    </TableHead>
                    <TableBody>
                        {#each resetRequests as request}
                            <TableBodyRow>
                                <TableBodyCell>{request.username}</TableBodyCell>
                                <TableBodyCell>
                                    <button class="text-green-600 hover:underline mr-2" on:click={() => handleResetRequest(request.id, 'approve')}>Accept</button>
                                    <button class="text-red-600 hover:underline" on:click={() => handleResetRequest(request.id, 'deny')}>Deny</button>
                                </TableBodyCell>
                            </TableBodyRow>
                        {/each}
                    </TableBody>
                </Table>
            </div>
            <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600" on:click={() => resetRequests = []}>Close</button>
        </div>
    </div>
{/if}


<div class="flex flex-row items-start justify-between min-h-screen w-full">
    <div class="flex flex-col items-center mix-h-screen w-full p-6">
        <Heading tag="h1" class="mb-20 text-3xl font-extrabold text-center md:text-5xl lg:text-6xl">
            <Span gradient>WELCOME TO INFILTR8</Span>
        </Heading>
        <!-- wrapper for all items under title -->
        <div class="columns-2 gap-x-10">
            <!-- Dropzone component for file uploads -->
            <div class="self-center float-left justify-between w-full mt-4">
                <input type="file" accept=".nessus" on:change="{handleChange}" multiple/>
                <form>
                    <Input class="text-center" type="text" id="first_name" placeholder="Enter Project Name" required />
                </form>
                <div class="relative justify-between w-90 ml-8">
                    <p class="text-center dark:text-gray-50 mb-8">Please select from the following to get started on your project.</p>
                    <div class="flex columns-2 justify-center gap-x-6 mb-72 w-full">
                        <GradientButton color="green"on:click={() => logButtonClick('Discard All clicked')}>Discard All</GradientButton>
                        <GradientButton on:click={() => { logButtonClick('Create project clicked'); createProject(); }}>Create Project</GradientButton>           
                    </div>
                </div>
            </div>
            <!-- start of table div -->
            <div>
                <h3 class="text-2xl font-semibold dark:text-gray-50 mb-6 text-center">Project List</h3>
                {#if projects.length > 0}
                    <Table hoverable={true} class=" float-right">
                        <TableHead>
                            <TableHeadCell>Select</TableHeadCell> <!-- Added Select column -->
                            <TableHeadCell>Project Name</TableHeadCell>   
                        </TableHead>
                        <TableBody>
                            {#each projects as project}
                                <TableBodyRow>
                                    <!-- Add a radio button to each row -->
                                    <TableBodyCell>
                                        <input 
                                            type="radio" 
                                            name="project" 
                                            value={project.projectId} 
                                            on:change={() => setCurrentProject(project.projectId)} />
                                    </TableBodyCell>
                        
                                    <TableBodyCell>{project.projectName}</TableBodyCell>
                                </TableBodyRow>
                            {/each}
                        </TableBody>
                    </Table>
                {:else if message}
                    <p class="text-center text-red-500">{message}</p>
                {:else}
                    <p class="text-center">No projects.  Create a project!</p>
                {/if}
            </div>
                
            
        </div>
    </div>
</div>