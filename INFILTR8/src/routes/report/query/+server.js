import { json, error } from '@sveltejs/kit';
import { runQuery } from '$lib/neo4j';

// Will be used later to handle all types of request
async function processQuery(query, params) {
    try {
        const data = await runQuery(query, params)
        return data
    } catch (err) {
        throw new Error('Error in query: ', err.message)
    }
}

// Will only do one thing currently
export async function GET({ request }) {
    const query = 'MATCH (n:Person) RETURN n';
    const params = {};

    try {
        const data = await processQuery(query, params)
        return json(data);
    } catch (err) {
        return error(500, err.message)
    }
}