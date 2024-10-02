import { writable } from "svelte/store";

//Menu Stuff
export const menuOpen = writable(true);

//scope stuff(info store in project route)
export const ipsAllowed = writable([]);
export const ipsDisallowed = writable([]);


