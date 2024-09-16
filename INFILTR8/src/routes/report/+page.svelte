
<!--TODO: Add current project file?? -->
<!--TODO: Add ability to select multiple rows -->
<!--TODO: Visual improvements-->
<!--TODO: add Logging of Export request to the User Actions -->


<script>
    let data = [];
    async function testGet() {
        try {
            // Fetch data from database
            const response = await fetch('report/query/', {method: 'GET'});
            // Checks if a 200 is given
            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            // Parses the json
            data = await response.json();
            console.log(data)
            let output = ""
            let temp
            for (let i=0;i<data.length;i++) {
                temp = data[i]["p"]["start"]["properties"]["name"]+"\n"
                output = output + temp
            }
            output = output + ""
            alert(output)
        } catch (err) {
            console.log(err)
        }
    }

    function handleDataBaseTest() {
        testGet()
    }

    //figure out where we are getting our report data from, this is good placeholder for this deliverable
    let rows = [
        { id: 1, ipAddress: '38.241.13.107', device: 'Device 1', vulnerability: 'CVE-2024-0101 (SQL Injection in User Authentication)', status: 'Exploited', selected: false },
        { id: 2, ipAddress: '49.6.148.87', device: 'Device 2', vulnerability: 'CVE-2024-3033 (Buffer Overflow in File Upload Handler)', status: 'Exploited', selected: false },
        { id: 3, ipAddress: '22.146.141.10', device: 'Device 12', vulnerability: 'CVE-2024-2022 (Cross-Site Scripting in Profile Management)', status: 'Not Exploited', selected: false },
        { id: 4, ipAddress: '11.27.177.103',device: 'Device 42', vulnerability: 'CVE-2024-6066 (Remote Code Execution in API Endpoint)', status: 'Exploited', selected: false }
    ];

    let exportFormat = "Format to export";

    function toggleSelect(row) {
        row.selected = !row.selected;
    }

    function handleExportFormatChange(event) {
        exportFormat = event.target.value;
    }

    function handleExport() {
        if (exportFormat === "Format to export") {
            alert("Please select a format to export.");
            return;
        }
        //navigate to route after export???
        window.location.href = `/export?format=${exportFormat}`;
    }
</script>

<style>
    .report-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        text-align: center;
    }
    h1 {
        margin-bottom: 20px;
    }
    table {
        width: 80%;
        border-collapse: collapse;
    }
    th, td {
        padding: 8px;
        text-align: center;
    }
    th {
        background-color: #f2f2f2;
    }
    table, th, td {
        border: none;
    }
    td {
        padding: 12px 8px;
    }
    .dropdown-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
        width: 80%;
    }
    .dropdown {
        padding: 10px;
        font-size: 16px;
    }
    .export-button-container {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
        width: 80%;
    }
    .export-button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        background-color: Blue;
        color: white; 
        border: none; 
        border-radius: 4px; 
    }
    .test-button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        background-color: rgb(255, 4, 4);
        color: white; 
        border: none; 
        border-radius: 4px; 
    }
</style>

<div class="report-container">
    <h1>Report</h1>
    
    <table>
        <thead>
            <tr>
                <th></th>
                <th>IP Address</th>
                <th>Device</th>
                <th>Vulnerability</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {#each rows as row}
                <tr>
                    <td>
                        <input type="checkbox" bind:checked={row.selected} on:change={() => toggleSelect(row)}>
                    </td>
                    <td>{row.ipAddress}</td>
                    <td>{row.device}</td>
                    <td>{row.vulnerability}</td>
                    <td>{row.status}</td>
                </tr>
            {/each}
        </tbody>
    </table>

    <!-- Dropdown menu for export format -->
    <div class="dropdown-container">
        <select class="dropdown" on:change={handleExportFormatChange}>
            <option disabled selected value="Format to export">Format to export</option>
            <option value="word">Word Document (.docx)</option>
            <option value="pdf">PDF Document (.pdf)</option>
        </select>
    </div>

    <!-- Export button -->
    <div class="export-button-container">
        <button class="export-button" on:click={handleExport}>
            Export
        </button>
    </div>

    <!-- Database test button -->
    <div class="database-container">
        <button class="test-button" on:click={handleDataBaseTest}>
            Database Test
        </button>
    </div>
</div>
