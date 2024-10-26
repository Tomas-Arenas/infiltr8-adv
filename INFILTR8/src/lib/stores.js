import { writable, get } from "svelte/store";

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