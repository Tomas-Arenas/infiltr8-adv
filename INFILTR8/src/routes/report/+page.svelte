<script>
	import { onMount } from 'svelte';
	import Papa from 'papaparse';
	import jsPDF from 'jspdf';
	import 'jspdf-autotable';
	import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
	import { Heading, Button } from 'flowbite-svelte';
	import { projectName, fileId } from '$lib/CurrentProject';

	let rows = [];
	let headers = [];
	let currentAPI = '/flask-api/ranked-entry-points';
	let isExportModalOpen = false;
	let selectedApis = [];
	let exportFormat = 'csv';
	let severityMin = 0.0;
	let severityMax = 1.0;
	let ipFilter = '';
	let portFilter = '';
	let pluginFilter = '';
	let minVulCount = 0;
	let maxVulCount = 100;

	$: severityMin = Math.max(0, Math.min(severityMin, 1));
	$: severityMax = Math.max(0, Math.min(severityMax, 1));

	const filterMapping = {
		'/flask-api/ranked-entry-points': ['ip', 'port', 'severity_score'],
		'/flask-api/data-with-exploits': ['ip', 'port', 'pluginName'],
		'/flask-api/entry-most-info': ['ip', 'port', 'vulnerability_count'],
		'/flask-api/port-0-entries': ['ip', 'port', 'pluginName'],
	};

	$: availableFilters = filterMapping[currentAPI] || [];

	$: filteredRows = rows.filter((row) => {
		const severity = parseFloat(row.severity_score || 0);
		const vulCount = parseInt(row.vulnerability_count || 0);
		return (
			severity >= severityMin &&
			severity <= severityMax &&
			(!ipFilter || row.ip.includes(ipFilter)) &&
			(!portFilter || row.port === portFilter) &&
			(!pluginFilter || row.pluginName.toLowerCase().includes(pluginFilter.toLowerCase())) &&
			vulCount >= minVulCount &&
			vulCount <= maxVulCount
		);
	});

	const apis = [
		{ name: 'Ranked Entry Points', endpoint: '/flask-api/ranked-entry-points' },
		{ name: 'Data with Exploits', endpoint: '/flask-api/data-with-exploits' },
		{ name: 'Entry Most Info', endpoint: '/flask-api/entry-most-info' },
		{ name: 'Port 0 Entries', endpoint: '/flask-api/port-0-entries' },
	];

	async function fetchCSVData() {
		try {
			const response = await fetch(currentAPI);
			if (!response.ok) throw new Error(`Failed to fetch data: ${response.statusText}`);
			const jsonResponse = await response.json();

			const { data } = jsonResponse;
			headers = data[0] || [];
			rows = data.slice(1).map((row, index) => {
				return headers.reduce((acc, header, colIndex) => {
					acc[header] = row[colIndex] || 'N/A';
					return acc;
				}, { id: index });
			});
		} catch (error) {
			console.error('Error fetching or parsing CSV data:', error);
			rows = [];
			headers = [];
		}
	}

	async function exportData() {
		if (selectedApis.length === 0) {
			alert('Please select at least one dataset to export.');
			return;
		}

		let combinedData = [];
		for (const api of selectedApis) {
			try {
				const response = await fetch(api.endpoint);
				const jsonResponse = await response.json();
				const { data } = jsonResponse;
				combinedData.push({ name: api.name, data });
			} catch (error) {
				console.error(`Error fetching data for ${api.name}:`, error);
			}
		}

		switch (exportFormat) {
			case 'csv':
				exportAsCSV(combinedData);
				break;
			case 'xml':
				exportAsXML(combinedData);
				break;
			case 'pdf':
				exportAsPDF(combinedData);
				break;
			default:
				alert('Invalid export format selected.');
		}
	}

	function exportAsCSV(combinedData) {
		try {
			const csvData = combinedData
				.map(({ name, data }) => `${name}\n${Papa.unparse(data)}`)
				.join('\n\n');
			const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
			triggerDownload(blob, 'selected_reports.csv');
		} catch (error) {
			console.error('Error generating CSV:', error);
		}
	}

	function exportAsXML(combinedData) {
		try {
			const sanitize = (value) =>
				String(value)
					.replace(/&/g, '&amp;')
					.replace(/</g, '&lt;')
					.replace(/>/g, '&gt;')
					.replace(/"/g, '&quot;')
					.replace(/'/g, '&apos;');

			const xmlData = combinedData
				.map(({ name, data }) => {
					const rows = data
						.map(
							(row) =>
								`<row>${Object.entries(row)
									.map(([key, value]) => `<${sanitize(key)}>${sanitize(value)}</${sanitize(key)}>`).join('')}</row>`
						).join('');
					return `<dataset name="${sanitize(name)}">${rows}</dataset>`;
				}).join('');
			const blob = new Blob([`<root>${xmlData}</root>`], { type: 'application/xml;charset=utf-8;' });
			triggerDownload(blob, 'selected_reports.xml');
		} catch (error) {
			console.error('Error generating XML:', error);
		}
	}

	async function exportAsPDF(combinedData) {
		try {
			const pdf = new jsPDF();
			let yOffset = 10;

			combinedData.forEach(({ name, data }) => {
				// Add dataset title
				pdf.text(name, 10, yOffset);
				yOffset += 10;

				// Generate table only if data exists
				if (data && data.length > 0) {
					const headers = Object.keys(data[0]);
					const rows = data.map((row) => Object.values(row));

					pdf.autoTable({
						startY: yOffset,
						head: [headers],
						body: rows,
					});

					yOffset = pdf.lastAutoTable.finalY + 10; // Update yOffset for next dataset
				}
			});

			// Save the PDF
			pdf.save('selected_reports.pdf');
		} catch (error) {
			console.error('Error generating PDF:', error);
		}
	}

	function triggerDownload(blob, filename) {
		const link = document.createElement('a');
		link.href = URL.createObjectURL(blob);
		link.setAttribute('download', filename);
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	function changeAPI(endpoint) {
		currentAPI = endpoint;
		fetchCSVData();
	}

	$: if (isExportModalOpen && selectedApis.length === 0) {
		selectedApis = [...apis];
	}
	onMount(fetchCSVData);

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
</script>

<main class="container mx-auto p-6">
	<!-- Title -->
	<div class="mb-4">
		<Heading tag="h1" class="font-bold text-xl dark:text-white text-center">
			REPORTS for {$projectName} File {$fileId}
		</Heading>
	</div>

	<!-- Dataset Selector -->
	<div class="mb-4">
		<label for="data-select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Select Dataset:</label>
		<select id="data-select" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:text-white"
			on:change={(event) => changeAPI(event.target.value)}>
			{#each apis as { name, endpoint }}
				<option value={endpoint} selected={currentAPI === endpoint}>{name}</option>
			{/each}
		</select>
	</div>

	<!-- Filters -->
	<div class="filters mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
		{#if availableFilters.includes('severity_score')}
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Severity Score (0.0 - 1.0)</label>
				<div class="flex gap-2">
					<input type="number" step="0.01" min="0" max="1" bind:value={severityMin} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="Min" />
					<input type="number" step="0.01" min="0" max="1" bind:value={severityMax} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="Max" />
				</div>
			</div>
		{/if}

		{#if availableFilters.includes('ip')}
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">IP Address</label>
				<input type="text" bind:value={ipFilter} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="e.g., 192.168.1.1" />
			</div>
		{/if}

		{#if availableFilters.includes('port')}
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Port</label>
				<input type="number" bind:value={portFilter} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="e.g., 443" />
			</div>
		{/if}

		{#if availableFilters.includes('pluginName')}
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Plugin Name</label>
				<input type="text" bind:value={pluginFilter} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="Search plugin name" />
			</div>
		{/if}

		{#if availableFilters.includes('vulnerability_count')}
			<div>
				<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Vulnerability Count</label>
				<div class="flex gap-2">
					<input type="number" bind:value={minVulCount} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="Min" />
					<input type="number" bind:value={maxVulCount} class="block w-full rounded-md border px-3 py-2 dark:bg-gray-800 dark:text-white" placeholder="Max" />
				</div>
			</div>
		{/if}
	</div>

	<!-- Filtered Data Table -->
	<div class="report-container mb-2 mt-2 rounded-lg bg-white shadow-md dark:bg-gray-800">
		<div class="table-container">
			<Table noborder={false} style="text-align: center">
				<TableHead style="bg-gray-100 dark:bg-gray-850 text-gray-700 text-align: center">
					{#if headers.length > 0}
						{#each headers as header}
							{#if header === 'ip' || header === 'port' || header === 'severity_score' || header === 'pluginName' || header === 'vulnerability_count'}
								<TableHeadCell style="text-align: center">{header.toUpperCase()}</TableHeadCell>
							{/if}
						{/each}
					{:else}
						<TableHeadCell>No Headers Available</TableHeadCell>
					{/if}
				</TableHead>
			</Table>
			<div class="table-body-scroll">
				<Table noborder={false} style="text-align: center">
					<TableBody style="text-align: center">
						{#if filteredRows.length > 0}
							{#each filteredRows as row (row.id)}
								<TableBodyRow style="text-align: center">
									{#each Object.entries(row) as [key, value]}
										{#if key === 'ip' || key === 'port' || key === 'severity_score' || key === 'pluginName' || key === 'vulnerability_count'}
											<TableBodyCell style="text-align: center">{value}</TableBodyCell>
										{/if}
									{/each}
								</TableBodyRow>
							{/each}
						{:else}
							<TableBodyRow>
								<TableBodyCell colspan={headers.length} class="text-center"
									>No Data Available</TableBodyCell
								>
							</TableBodyRow>
						{/if}
					</TableBody>
				</Table>
			</div>
		</div>
	</div>

		<!-- Export Button -->
		<div class="flex justify-end mt-4">
			<Button on:click={() => {logButtonClick("export button clicked"); isExportModalOpen = true}} color="primary" class="text-lg">
				Export
			</Button>
		</div>
	
		<!-- Export Modal -->
		{#if isExportModalOpen}
		<div class="modal-backdrop">
			<div class="modal-container dark:bg-gray-800 bg-white">
				<Heading tag="h4" class="mb-4">Select Datasets and Format</Heading>
				<div class="flex flex-col gap-2 dark:text-gray-300">
					{#each apis as api}
						<label class="inline-flex items-center">
							<input
								type="checkbox"
								value={api.endpoint}
								checked={selectedApis.includes(api)}
								on:change={(e) => {
									if (e.target.checked) {
										selectedApis = [...selectedApis, api];
									} else {
										selectedApis = selectedApis.filter((a) => a.endpoint !== api.endpoint);
									}
								}}
							/>
							<span class="ml-2">{api.name}</span>
						</label>
					{/each}
				</div>
				<div class="mt-4">
					<label class="block mb-2 dark:text-gray-300">Select Export Format:</label>
					<select class="block w-full p-2 border dark:bg-gray-700 dark:text-white" bind:value={exportFormat}>
						<option value="csv">CSV</option>
						<option value="xml">XML</option>
						<option value="pdf">PDF</option>
					</select>
				</div>
				<div class="mt-4 flex justify-end gap-2">
					<Button on:click={() => {logButtonClick("cancel button clicked"); (isExportModalOpen = false)}} color="info" class="dark:text-gray-300">Cancel</Button>
					<Button on:click={() => { logButtonClick("export started"); isExportModalOpen = false; exportData(); }} color="primary">Export</Button>
				</div>
			</div>
		</div>
		{/if}
</main>

<style>
	.container {
		max-width: 1200px;
		min-height: 95vh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.report-container {
		padding: 1rem;
		margin-top: 1rem;
	}

	.table-body-scroll {
		max-height: 490px;
		overflow-y: auto;
	}

	.modal-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.modal-container {
		padding: 2rem;
		border-radius: 0.5rem;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		width: 400px;
	}
</style>
