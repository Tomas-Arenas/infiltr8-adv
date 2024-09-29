import { SystemInfo } from './SystemInfo.js';
import neo4j from 'neo4j-driver';

export class LogManager {
    constructor() {
        this.systemInfo = new SystemInfo();
        this.currentDate = this.systemInfo.getFormattedDate();
        this.driver = neo4j.driver('bolt://localhost:7687');
    }

    async logUserAction(username, action, details) {
        const logEntry = this._createLogEntry('User Action', action, details);
        await this._writeLog(username, logEntry);
    }

    async logSystemAction(username, action, details) {
        const logEntry = this._createLogEntry('System Action', action, details);
        await this._writeLog(username, logEntry);
    }

    async logSystemError(username, error, details) {
        const logEntry = this._createLogEntry('System Error', error, details);
        await this._writeLog(username, logEntry);
    }

    _createLogEntry(type, actionOrError, details) {
        return {
            type,
            message: actionOrError,
            details,
            timestamp: this.systemInfo.getCurrentTimestamp(),
            date: this.currentDate
        };
    }

    async _writeLog(username, logEntry) {
        const session = this.driver.session();
        try {
            await session.writeTransaction(tx =>
                tx.run(
                    `MERGE (p:Person {name: $username})
                     MERGE (d:Date {date: $date})
                     CREATE (d)-[:HAS_ENTRY]->(l:Log {type: $type, message: $message, details: $details, timestamp: $timestamp, user: $username})
                     MERGE (p)-[:HAS_LOG]->(d)`,
                    {
                        username,
                        date: logEntry.date,
                        type: logEntry.type,
                        message: logEntry.message,
                        details: logEntry.details,
                        timestamp: logEntry.timestamp
                    }
                )
            );
            console.log(`Log created for user ${username}: ${logEntry.type} - ${logEntry.message}`);
        } catch (error) {
            console.error('Error writing log entry:', error);
        } finally {
            await session.close();
        }
    }

    async close() {
        await this.driver.close();
    }
}

export default LogManager;
