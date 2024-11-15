<script>
	import { onMount } from 'svelte';
	import Papa from 'papaparse';
	import { Table, TableBody, TableBodyCell, TableBodyRow, TableHead, TableHeadCell } from 'flowbite-svelte';
	import { Heading, Button } from 'flowbite-svelte';

	let rows = [];
	let currentAPI = '/flask-api/ranked-entry-points'; // Default API endpoint
	let headers = []; // Separate headers to ensure they're shown even if rows are empty

	const apis = [
		{ name: 'Ranked Entry Points', endpoint: '/flask-api/ranked-entry-points' },
		{ name: 'Data with Exploits', endpoint: '/flask-api/data-with-exploits' },
		{ name: 'Entry Most Info', endpoint: '/flask-api/entry-most-info' },
		{ name: 'Port 0 Entries', endpoint: '/flask-api/port-0-entries' },
	];

	async function fetchCSVData() {
		try {
			const response = await fetch(currentAPI);
			if (!response.ok) {
				throw new Error(`Failed to fetch data: ${response.statusText}`);
			}
			const jsonResponse = await response.json();

			const { data } = jsonResponse;
			headers = data[0] || []; // Ensure headers are always populated
			const rowsData = data.slice(1);

			rows = rowsData.map((row, index) => {
				return headers.reduce((acc, header, colIndex) => {
					acc[header] = row[colIndex] || 'N/A';
					return acc;
				}, { id: index });
			});
		} catch (error) {
			console.error('Error fetching or parsing CSV data:', error);
			rows = [];
			headers = []; // Reset in case of error
		}
	}

	function exportToCSV() {
		const csvData = Papa.unparse(rows.map(row => ({ ...row })));
		const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
		const link = document.createElement("a");
		link.href = URL.createObjectURL(blob);
		link.setAttribute("download", "reports.csv");
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}

	function changeAPI(endpoint) {
		currentAPI = endpoint;
		fetchCSVData();
	}

	onMount(() => {
		fetchCSVData();
	});
</script>

<main class="container mx-auto p-6">
	<!-- Title -->
	<div class="mb-4">
		<Heading tag="h1" class="font-bold text-xl dark:text-white text-left">
			REPORTS
		</Heading>
	</div>

	<!-- Dropdown to switch between datasets -->
	<div class="mb-4">
		<label for="data-select" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Select Dataset:</label>
		<select id="data-select" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:text-white"
			on:change={(event) => changeAPI(event.target.value)}>
			{#each apis as { name, endpoint }}
				<option value={endpoint} selected={currentAPI === endpoint}>{name}</option>
			{/each}
		</select>
	</div>

	<!-- Table Container -->
	<div class="report-container dark:bg-gray-800 bg-white rounded-lg shadow-md mt-2 mb-2">
		<div class="table-container">
			<Table noborder={true}>
				<TableHead class="bg-gray-100 dark:bg-gray-900 text-gray-700 dark:text-gray-400">
					{#if headers.length > 0}
						{#each headers as header}
							<TableHeadCell>{header.toUpperCase()}</TableHeadCell>
						{/each}
					{:else}
						<TableHeadCell>No Headers Available</TableHeadCell>
					{/if}
				</TableHead>
			</Table>
			<div class="table-body-scroll">
				<Table noborder={true}>
					<TableBody>
						{#if rows.length > 0}
							{#each rows as row (row.id)}
								<TableBodyRow class="border-b dark:border-gray-700">
									{#each Object.values(row) as value}
										<TableBodyCell>{value}</TableBodyCell>
									{/each}
								</TableBodyRow>
							{/each}
						{:else}
							<TableBodyRow>
								<TableBodyCell colspan={headers.length} class="text-center">
									No Data Available
								</TableBodyCell>
							</TableBodyRow>
						{/if}
					</TableBody>
				</Table>
			</div>
		</div>
	</div>

	<!-- Export Button -->
	<div class="flex justify-end mt-1">
		<Button on:click={exportToCSV} color="primary" class="text-lg">
			Export
		</Button>
	</div>
</main>

<style>
	/* Existing styling */
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
		margin-bottom: 0.5rem;
	}
	.table-container {
		display: grid;
		grid-template-rows: auto 1fr;
	}
	.table-body-scroll {
		max-height: 490px;
		overflow-y: auto;
	}
	th {
		position: sticky;
		top: 0;
		background-color: inherit;
		z-index: 1;
	}
	.mt-1 {
		margin-top: 0.25rem;
	}
	select {
		width: 100%;
		padding: 0.5rem;
		font-size: 1rem;
	}
</style>