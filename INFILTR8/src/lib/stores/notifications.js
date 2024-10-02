// src/lib/stores/notificationStore.js
import { writable } from 'svelte/store';

export const notifications = writable([]);

let currentPage = 0;
const pageSize = 20;

// Fetch the most recent notifications from Neo4j
export async function loadNotificationsFromDB(username) {
    const skip = currentPage * pageSize;
    const dbNotifications = await getUserNotifications(username, skip, pageSize); // Fetch with pagination from Neo4j
    notifications.update(n => [...n, ...dbNotifications.map(notification => ({
        ...notification,
        new: false, // Mark notifications from the DB as not new
    }))]);
    currentPage++; // Increment for pagination
}

// Add new notification (new notifications during session)
export function addNewNotification(notification) {
    notifications.update(n => [...n, { ...notification, new: true }]);
}

// Mark notification as old (after being shown in Toast)
export function markNotificationAsOld(id) {
    notifications.update(n => n.map(notification =>
        notification.id === id ? { ...notification, new: false } : notification
    ));
}

// Remove notification (used for temporary notifications)
export function removeNotification(id, type) {
    notifications.update(n => n.filter(notification => notification.id !== id));
    // Optionally call backend to remove notification from Neo4j if it's temporary
}
