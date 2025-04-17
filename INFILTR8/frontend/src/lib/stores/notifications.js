// src/lib/stores/notifications.js
import { writable } from 'svelte/store';

export const notifications = writable([]);

let currentPage = 0;
const pageSize = 20;

// Fetch notifications from the backend and append them to the store
export async function loadNotifications() {
    const skip = currentPage * pageSize;
    const limit = pageSize;

    try {
        const response = await fetch(`/flask-api/get-notifications?skip=${skip}&limit=${limit}`, {
            method: 'GET',
            credentials: 'include', // Ensure cookies with session info are included
        });
        const data = await response.json();
        if (data.notifications) {
            notifications.update(n => [...n, ...data.notifications.map(notification => ({
                ...notification,
                isNew: false, // Mark as old
                isPermanent: true // From DB, always permanent
            }))]);
            currentPage++; // Increment the page after successfully loading
        } else {
            console.error("No notifications returned from backend.");
        }
    } catch (error) {
        console.error("Error fetching notifications from backend:", error);
    }
}

// Add new notification (distinguish between temporary and permanent)
export function addNewNotification(notification) {
    notifications.update(n => [...n, {
        ...notification,
        isNew: true, // Mark as new (to be shown in the toast)
        isPermanent: notification.isPermanent ?? false // Default to false if not specified
    }]);
    console.log('New notification:', notification);
    
    // If it's permanent, sync it with the backend
    if (notification.isPermanent) {
        writeNotificationToBackend(notification); // A function to sync with the backend
    }
}

// Mark notification as old (after being shown in Toast, but no removal)
export function markNotificationAsOld(id) {
    notifications.update(n => n.map(notification =>
        notification.id === id ? { ...notification, isNew: false } : notification
    ));
}

// Remove notification (only temporary removal is handled in the notification section)
export function removeNotificationFromBackend(id) {
    console.log("Removing from backend:", id);
    // Your logic here to remove from the Neo4j backend (this will be handled in the future notification section)
}

async function writeNotificationToBackend(notification) {
    try {
        const response = await fetch('/flask-api/create-notification', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: notification.message,
                isPermanent: notification.isPermanent,
                timestamp: notification.timestamp || new Date().toISOString(),
            }),
            credentials: 'include' // Ensure cookies with session info are included
        });

        const data = await response.json();
        if (data.status === 'success') {
            console.log("Notification successfully written to backend:", data.notification);
        } else {
            console.error("Failed to write notification to backend:", data.error);
        }
    } catch (error) {
        console.error("Error writing notification to backend:", error);
    }
}
