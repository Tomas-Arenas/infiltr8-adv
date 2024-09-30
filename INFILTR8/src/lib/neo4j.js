import neo4j from 'neo4j-driver';

// starts the driver and a session
const driver = neo4j.driver('neo4j+s://815ececb.databases.neo4j.io',neo4j.auth.basic('neo4j', 'B_bZrryeGChT2mXJO3TBhzJ4sfrSuqUhvM_zRcDukkw'));
const session = driver.session();

// runs a givne query and retuns the output as a map
export async function runQuery(query, params) {
    try {
        const result = await session.run(query, params);
        // cuts down information to only needed parts
        return result.records.map(record => record.toObject());
    } catch (error) {
        console.log('query error: ', error)
    }
}

// gets the server status
export async function serverStatus() {
  try {
    // Gets some server info will print to the terminal in the server
    const serverInfo = await driver.getServerInfo();
    console.log('Connected to Neo4j');
    console.log(serverInfo)
  } catch (error) {
    // Prints the error if fails to connect
    console.error('Failed to connect to Neo4j', error);
  }
}