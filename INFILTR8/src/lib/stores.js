import { writable, get } from "svelte/store";
import { IP } from "$lib/IP.js"

//Menu Stuff
export const menuOpen = writable(false);

//scope stuff(info store in project route)
export const ipsAllowed = writable([]);
export const ipsDisallowed = writable([]);


// Function to send store data to the backend
export const sendIPSToBackend = async () => {
    const data = get(ipsDisallowed);  
    try {
      const response = await fetch('/flask-api/get-ips', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      console.log('Data sent to backend:', result);
    } catch (error) {
      console.error('Error sending data:', error);
    }
};

  //should be ran once a nessus file is uploaded
  export async function getIPsFromBackend(fileName) {
    const ipData = get(ipsDisallowed).map(ipInstance => ipInstance.ip);  // Assuming IP has an `ip` property
    const payload = {
        project_id: 1, // Or dynamically assign this based on the project
        ips: ipData.join(","), // Convert array to comma-separated string
        exploits: ["SQL Injection", "DDOS Attack"] // Example exploit types
    };
    try {
        const response = await fetch('/flask-api/get-ips', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        console.log('Data sent to backend:', result);
    } catch (error) {
        console.error('Error sending data:', error);
    }
};

  function addIPstoStore(data) {
    const ipInstances = data.map(ipAddress => new IP(ipAddress)); // Create IP instances
    console.log(ipInstances)
    ipsDisallowed.set(ipInstances); // Update the store with IP instances
}

// DARK MODE LOGIC
// Load dark mode preference from localStorage, defaulting to 'light' mode
const savedTheme = (typeof window !== 'undefined' && localStorage.getItem("color-theme")) || "light";

// Create a writable store for dark mode state based on saved preference
export const darkMode = writable(savedTheme === "dark");

// Subscribe to darkMode store to watch for changes and sync with localStorage
darkMode.subscribe((value) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("color-theme", value ? "dark" : "light");
    document.documentElement.classList.toggle("dark", value);
  }
});