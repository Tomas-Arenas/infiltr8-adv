<script>
    import { SystemInfo } from '../../lib/SystemInfo.js';
    import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
    import { Chart, Card, A, Button, Dropdown, DropdownItem, Popover, Tooltip, Progressbar } from 'flowbite-svelte';
    import { InfoCircleSolid, ArrowDownToBracketOutline, ChevronDownOutline, ChevronRightOutline, PenSolid, DownloadSolid, ShareNodesSolid, ShareNodesOutline } from 'flowbite-svelte-icons';
    import { onMount, onDestroy } from 'svelte';
    import { projectName, fileId } from '$lib/CurrentProject.js';
	import { goto } from '$app/navigation';

    let tableData = [];
    let series = [0, 0, 0]; 
    let latestProject = null;
    let username = "";
    
    async function checkSession(){
        try{
            const response = await fetch('/flask-api/check_session',{
                method: 'GET',
                credentials: 'include'
            });
            if (response.ok){
                const sessionData = await response.json();
                if (sessionData.logged_in){
                    username = sessionData.username;
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

    onMount(() => {
        getTableData();
    
        const initialize = async () => {
            await checkSession();
            setInterval(async () => {
                await getTableData();
            }, 1000);
        }
        initialize();
    });


    async function logButtonClick(detail) {
        console.log("Button clicked with detail:", detail);  // For debugging
        try {
            const response = await fetch('/flask-api/log-action', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username || 'Anonymous',  // Dummy username for now
                    action: 'ButtonClick',
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

    async function downloadLogs() {
        const date = getFormattedDate(); 
        try {
            const response = await fetch(`/flask-api/download-logs/${date}`);
            if (!response.ok) {
                throw new Error('Failed to download logs');
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `logs_${date}.log`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } catch (error) {
            console.error('Failed to download logs:', error);
        }
    }

    async function reportHandler(projectNameIn, fileIdIn) {
        console.log(projectNameIn + ' ' + fileIdIn)
        projectName.set(projectNameIn)
        fileId.set(fileIdIn)
        try {
            const response = await fetch('/flask-api/set-current-project-and-file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    projectNameJ: projectNameIn,
                    fileIdJ: fileIdIn
                })
            });

            if (!response.ok) {
                throw new Error('Failed to move on to report page');
            }

            const result = await response.json();
            console.log('session vars changed', result);
            goto("http://localhost:5173/report")
        } catch (error) {
            console.error('Failed to change info and goto report button click:', error);
        }
    }

    async function getTableData() {
        try {
            // Check for cached data
            const cachedData = localStorage.getItem("tableData");
            const cachedTimestamp = localStorage.getItem("tableDataTimestamp");

            // Use cached data if it exists and is recent ( within 1 sec )
            const cacheValid = cachedData && cachedTimestamp && 
                (Date.now() - parseInt(cachedTimestamp) < 1000);

            if (cacheValid) {
                const data = JSON.parse(cachedData);
                processTableData(data);
                return;
            }

            const response = await fetch("/flask-api/get-all-project-info-many", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();

            localStorage.setItem("tableData", JSON.stringify(data));
            localStorage.setItem("tableDataTimestamp", Date.now().toString());

            processTableData(data);
        } catch (error) {
            console.error("There was an error retrieving data from the backend:", error);
        }
    }

    function processTableData(data) {
        tableData = Object.values(data).flatMap(Object.values);
        tableData = tableData.filter(row => row.status != null);
        series = [0, 0, 0];
        tableData.forEach(row => {
            if (row.status === "completed") {
                series[2]++;
            } else if (row.status === "created") {
                series[0]++;
            } else {
                series[1]++;
            }
        });

        // Get the latest project by date
        if (tableData.length > 0) {
            latestProject = tableData.reduce((latest, current) =>
                new Date(current.creation) > new Date(latest.creation) ? current : latest
            );
        }
    }


    function getFormattedDate() {
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    const sysInfo = new SystemInfo()
    var timestamp = sysInfo.getCurrentTimestamp()
    var date =  sysInfo.getFormattedDate()

</script>

<main>
    
    <h1 class="font-bold text-xl dark:text-white mb-4 text-center">Analysis</h1>
    
        <div class="flex flex-wrap w-full gap-6">
            
            <!-- start of the left column -->   
            <div id="left" class="flex-grow w-8/12 p-6 bg-white rounded-lg shadow-md dark:bg-gray-900">
                <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-gray-400 mb-4">Projects</h5>

                <div id="table" class="my-6 bg-gray-800 rounded-lg overflow-hidden shadow-md">
                    <Table noborder={true}>
                        <TableHead class="text-xs text-gray-700 uppercase bg-gray-100 dark:bg-gray-700 dark:text-gray-400">
                        <TableHeadCell>Date</TableHeadCell>
                        <TableHeadCell>Project Name</TableHeadCell>
                        <TableHeadCell>File</TableHeadCell>
                        <TableHeadCell>File Size</TableHeadCell>
                        <TableHeadCell>Status</TableHeadCell>
                    </TableHead>
                    <TableBody class="bg-gray-800">
                        {#if tableData.length > 0}
                        {#each tableData as row}
                            <TableBodyRow>
                            <TableBodyCell>{row.creation}</TableBodyCell>
                            <TableBodyCell>{row.projectName}</TableBodyCell>
                            <TableBodyCell>{row.fileId}</TableBodyCell>
                            <TableBodyCell>{row.fileSize}</TableBodyCell>
                            <TableBodyCell>
                                {#if typeof row.status === 'number'}
                                <Progressbar progress={row.status} labelInside />
                                {:else if typeof row.status === 'completed' || row.status === 'reports' }
                                <button on:click={() => {logButtonClick("clicked report button"); reportHandler(row.projectName, row.fileId)}} class="border-2 py-2 px-2 shadow-md rounded-lg">{row.status} </button>
                                {:else }
                                <button on:click={() => window.location.href = "http://localhost:5173/dashboard"}  class="border-2 py-2 px-2 shadow-md rounded-lg">{row.status} </button>
                                {/if}
                            </TableBodyCell>
                            </TableBodyRow>
                        {/each}
                        {:else}
                        <TableBodyRow>
                            <TableBodyCell colspan="4" class="text-center">
                            No existing projects
                            </TableBodyCell>
                        </TableBodyRow>
                        {/if}
                    </TableBody>
                    </Table>
                </div>
            </div>

            <!-- Right Column -->
            <div id="right" class="flex flex-col w-3/12 gap-6">
                <!-- Analysis Progress -->
                <div id="topChart" class="p-6 bg-white rounded-lg shadow-md dark:bg-gray-900">
                <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-gray-400 mb-4">Analysis Progress</h5>
                <Chart
                    options={{
                    chart: { type: 'donut', height: 280, width: '100%' },
                    series: series,
                    colors: ['#1C64F2', '#16BDCA', '#FDBA8C'],
                    stroke: { colors: ['transparent'] },
                    plotOptions: { pie: { donut: { labels: { show: true, total: { showAlways: true } } } } },
                    labels: ['Created', 'Completed', 'Analyzing'],
                    legend: { position: 'bottom' },
                    dataLabels: { enabled: false },
                    }}
                    class="py-6"
                />
                </div>

                <!-- Current Project Settings -->
                <div id="bottomSettings" class="p-6 bg-white rounded-lg shadow-md dark:bg-gray-900">
                <h5 class="text-xl font-bold leading-none text-gray-900 dark:text-gray-400 mb-4">Current Test</h5>

                {#if latestProject}
                    <div class="dark:text-white">
                    <p>Project Name: {latestProject.projectName}</p>
                    <p>Analyst: {latestProject.user}</p>
                    <p>File Size: {latestProject.fileSize}</p>
                    <p>Status: {latestProject.status}</p>
                    <p>Time Started: {latestProject.creation}</p>
                    <button 
                        on:click={() => {logButtonClick("user downloaded logs"); downloadLogs}} 
                        class="w-full mt-4 bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        Download Logs
                    </button>
                    </div>
                {:else}
                    <p class="text-center">No current test available.</p>
                {/if}
                </div>
            </div>

            <div id="middle" class="w-full p-6 min-h-[40vh]"></div>

        </div>


</main>