import { writable, get } from "svelte/store";
import { IP } from "$lib/IP.js"
import { json } from "@sveltejs/kit";

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
    try {
        const response = await fetch("/flask-api/get-all-ips", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name: fileName})
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json(); // Parse JSON response
        console.log("IPs received from backend:", data);
        console.log(typeof(data))
        addIPstoStore(data); // Update the store with received IPs
        return data
    } catch (error) {
        console.error("There was an error retrieving IPs from the backend:", error);
    }
  };

  function addIPstoStore(data) {
    const ipInstances = data.map(ipAddress => new IP(ipAddress)); // Create IP instances
    console.log(ipInstances)
    ipsDisallowed.set(ipInstances); // Update the store with IP instances
}