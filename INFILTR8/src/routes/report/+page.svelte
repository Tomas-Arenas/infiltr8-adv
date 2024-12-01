<script>
	import { onMount } from 'svelte';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell
	} from 'flowbite-svelte';
	import { Heading, Button } from 'flowbite-svelte';

	let rows = [];
	let headers = [];
	let currentAPI = '/flask-api/ranked-entry-points';

	let severityMin = 0.0;
	let severityMax = 1.0;
	let ipFilter = '';
	let portFilter = '';
	let pluginFilter = '';
	let minVulCount = 0;
	let maxVulCount = 100;

	$: severityMin = Math.max(0, Math.min(severityMin, 1));
	$: severityMax = Math.max(0, Math.min(severityMax, 1));

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

	async function fetchCSVData() {
		try {
			const response = await fetch(currentAPI);
			if (!response.ok) throw new Error(`Failed to fetch data: ${response.statusText}`);
			const jsonResponse = await response.json();
			const { data } = jsonResponse;
			headers = data[0] || [];
			rows = data.slice(1).map((row, index) => {
				return headers.reduce(
					(acc, header, colIndex) => {
						acc[header] = row[colIndex] || 'N/A';
						return acc;
					},
					{ id: index }
				);
			});
		} catch (error) {
			console.error('Error fetching or parsing CSV data:', error);
			rows = [];
			headers = [];
		}
	}

	function changeAPI(endpoint) {
		currentAPI = endpoint;
		fetchCSVData();
	}

	onMount(fetchCSVData);
</script>

<main class="container mx-auto min-h-screen p-6">
	<div class="mb-4">
		<Heading tag="h1" class="text-left text-xl font-bold dark:text-white">REPORTS</Heading>
	</div>

	<div class="mb-4">
		<label for="data-select" class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
			>Select Dataset:</label
		>
		<select
			id="data-select"
			class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
			on:change={(event) => changeAPI(event.target.value)}
		>
			<option value="/flask-api/ranked-entry-points" selected>Ranked Entry Points</option>
			<option value="/flask-api/data-with-exploits">Data with Exploits</option>
			<option value="/flask-api/entry-most-info">Entry Most Info</option>
			<option value="/flask-api/port-0-entries">Port 0 Entries</option>
		</select>
	</div>

	<!-- Filters -->
	<div class="filters mb-6 grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
		<!-- Severity Range Filter -->
		<div>
			<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
				>Severity Score (0.0 - 1.0)</label
			>
			<div class="flex gap-2">
				<input
					type="number"
					step="0.01"
					min="0"
					max="1"
					bind:value={severityMin}
					class="block w-full rounded-md border px-3 py-2"
					placeholder="Min"
				/>
				<input
					type="number"
					step="0.01"
					min="0"
					max="1"
					bind:value={severityMax}
					class="block w-full rounded-md border px-3 py-2"
					placeholder="Max"
				/>
			</div>
		</div>

		<!-- IP Filter -->
		<div>
			<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
				>IP Address</label
			>
			<input
				type="text"
				bind:value={ipFilter}
				class="block w-full rounded-md border px-3 py-2"
				placeholder="e.g., 192.168.1.1"
			/>
		</div>

		<!-- Port Filter -->
		<div>
			<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Port</label>
			<input
				type="number"
				bind:value={portFilter}
				class="block w-full rounded-md border px-3 py-2"
				placeholder="e.g., 443"
			/>
		</div>

		<!-- Plugin Name Filter -->
		<div>
			<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
				>Plugin Name</label
			>
			<input
				type="text"
				bind:value={pluginFilter}
				class="block w-full rounded-md border px-3 py-2"
				placeholder="Search plugin name"
			/>
		</div>

		<!-- Vulnerability Count Filter -->
		<div>
			<label class="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300"
				>Vulnerability Count</label
			>
			<div class="flex gap-2">
				<input
					type="number"
					bind:value={minVulCount}
					class="block w-full rounded-md border px-3 py-2"
					placeholder="Min"
				/>
				<input
					type="number"
					bind:value={maxVulCount}
					class="block w-full rounded-md border px-3 py-2"
					placeholder="Max"
				/>
			</div>
		</div>
	</div>

	<!-- Filtered Data Table -->
	<div class="report-container mb-2 mt-2 rounded-lg bg-white shadow-md dark:bg-gray-800">
		<div class="table-container">
			<Table noborder={false} style="text-align: center">
				<TableHead style="bg-gray-100 dark:bg-gray-850 text-gray-700">
					{#if headers.length > 0}
						{#each headers as header}
							{#if header === 'ip' || header === 'port' || header === 'severity_score' || header === 'pluginName' || header === 'vulnerability_count'}
								<TableHeadCell>{header.toUpperCase()}</TableHeadCell>
							{/if}
						{/each}
					{:else}
						<TableHeadCell>No Headers Available</TableHeadCell>
					{/if}
				</TableHead>
			</Table>
			<div class="table-body-scroll">
				<Table noborder={true}>
					<TableBody>
						{#if filteredRows.length > 0}
							{#each filteredRows as row (row.id)}
								<TableBodyRow>
									{#each Object.entries(row) as [key, value]}
										{#if key === 'ip' || key === 'port' || key === 'severity_score' || key === 'pluginName' || key === 'vulnerability_count'}
											<TableBodyCell>{value}</TableBodyCell>
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
</main>

<style>
	.filters input {
		border: 1px solid #ccc;
		border-radius: 5px;
		padding: 0.5rem;
	}

	.table-body-scroll {
		max-height: 490px;
		overflow-y: auto;
	}
</style>
