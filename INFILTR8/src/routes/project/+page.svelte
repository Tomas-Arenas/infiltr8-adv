<script>
    let scopeIPs = [
        { id: 1, ip: '192.168.2.15', selected: false },
        { id: 2, ip: '192.168.2.15', selected: false },
        { id: 3, ip: '192.168.8.43', selected: false },
        { id: 4, ip: '192.168.5.5', selected: false }
    ];

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

    function moveUp(list, index) {
        if (index > 0) {
            const temp = list[index];
            list[index] = list[index - 1];
            list[index - 1] = temp;
        }
    }

    function moveDown(list, index) {
        if (index < list.length - 1) {
            const temp = list[index];
            list[index] = list[index + 1];
            list[index + 1] = temp;
        }
    }

    function loadProject(project) {
        console.log(`Project ${project.name} loaded.`);
    }
</script>

<style>
    .container {
        display: flex;
        justify-content: space-between;
        padding: 20px;
        gap: 20px;
    }
    .section {
        flex: 1;
        background-color: #f8f8f8;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .arrows {
        display: flex;
        gap: 5px;
    }
    button {
        background-color: white;
        border: none;
        cursor: pointer;
        font-size: 18px;
    }
    button:hover {
        color: blue;
    }
    .start-button {
        background-color: blue;
        color: white;
        padding: 15px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
    }
    .start-button:hover {
        background-color: #0056b3;
    }
    .load-project-section {
        flex: 0.3;
    }
    .project-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .project-item:hover {
        background-color: #e6e6e6;
    }
    .project-name {
        display: flex;
        flex-direction: column;
    }
    .project-size {
        color: gray;
        font-size: 12px;
    }
</style>

<div class="container">
    <div class="section">
        <h2>Current project folder</h2>
        <div>
            <h3>Scope IP List</h3>
            {#each scopeIPs as ip, index}
                <div class="item">
                    <div>
                        <input type="checkbox" bind:checked={ip.selected} />
                        <span>{ip.ip}</span>
                    </div>
                    <div class="arrows">
                        <button on:click={() => moveUp(scopeIPs, index)}>⬆</button>
                        <button on:click={() => moveDown(scopeIPs, index)}>⬇</button>
                    </div>
                </div>
            {/each}
        </div>
        <div>
            <h3>Exploits Allowed</h3>
            {#each exploitsAllowed as exploit, index}
                <div class="item">
                    <div>
                        <input type="checkbox" bind:checked={exploit.selected} />
                        <span>{exploit.name}</span>
                    </div>
                    <div class="arrows">
                        <button on:click={() => moveUp(exploitsAllowed, index)}>⬆</button>
                        <button on:click={() => moveDown(exploitsAllowed, index)}>⬇</button>
                    </div>
                </div>
            {/each}
        </div>
        <button class="start-button" on:click={() => console.log("Start Testing")}>Start Testing</button>
    </div>

    <!-- Load Project Section -->
    <div class="section load-project-section">
        <h3>Load Project</h3>
        {#each projects as project}
            <div class="project-item" on:click={() => loadProject(project)}>
                <div class="project-name">
                    <span>{project.name}</span>
                    <span class="project-size">{project.items} items • {project.size}</span>
                </div>
                <div>
                    <span>⋮</span>
                </div>
            </div>
        {/each}
    </div>
</div>
