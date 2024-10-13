import { writable } from "svelte/store";

//Menu Stuff
export const menuOpen = writable(false);

//scope stuff(info store in project route)
export const ipsAllowed = writable([]);
export const ipsDisallowed = writable([]);

export const userSession = writable({loggedIn: false, username: ''});